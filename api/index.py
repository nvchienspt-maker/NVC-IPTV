from flask import Flask, request, Response, redirect
import requests
import re

app = Flask(__name__)

# Danh sách ID kênh VTVGo cơ bản
CHANNELS = {
    "1": ("VTV1", "https://vtvgo.vn/channel/vtv1-1,1.html"),
    "2": ("VTV2", "https://vtvgo.vn/channel/vtv2-1,2.html"),
    "3": ("VTV3", "https://vtvgo.vn/channel/vtv3-1,3.html"),
    "4": ("VTV4", "https://vtvgo.vn/channel/vtv4-1,4.html"),
    "5": ("VTV5", "https://vtvgo.vn/channel/vtv5-1,5.html")
}

@app.route('/playlist.m3u')
def get_playlist():
    # Lấy địa chỉ máy chủ nội bộ hoặc Vercel hiện tại của bạn
    host = request.host_url 
    
    m3u = "#EXTM3U\n"
    for ch_id, (name, _) in CHANNELS.items():
        m3u += f'#EXTINF:-1 group-title="VTV", {name}\n'
        # Thêm User-Agent và Referer thẳng vào m3u để khắc phục lỗi trình phát VLC
        m3u += '#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\n'
        m3u += '#EXTVLCOPT:http-referrer=https://vtvgo.vn/\n'
        # Gắn link chuyển hướng qua API của bạn
        m3u += f'{host}api/play?id={ch_id}\n'
    
    return Response(m3u, mimetype='audio/mpegurl')

@app.route('/api/play')
def play_channel():
    ch_id = request.args.get('id')
    if ch_id not in CHANNELS:
        return "Kênh không tồn tại", 404
        
    _, page_url = CHANNELS[ch_id]
    
    try:
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://vtvgo.vn/",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        # 1. Tải trang chủ của kênh để lấy mã Token ẩn
        page_res = session.get(page_url, headers=headers)
        
        # Dùng Regex để tách Token
        token_match = re.search(r'setToken\s*=\s*"(.*?)"', page_res.text)
        token = token_match.group(1) if token_match else ""
        
        # In ra màn hình console (Terminal) để kiểm tra token lúc chạy nội bộ
        print(f"--> Token tìm thấy cho kênh {ch_id}: '{token}'")
        
        # 2. Gửi request POST giả lập AJAX để bóc link m3u8
        api_url = "https://vtvgo.vn/ajax/get_stream"
        payload = {
            "id_kenh": ch_id,
            "type": 1,
            "token": token
        }
        
        api_res = session.post(api_url, headers=headers, data=payload)
        
        # In trực tiếp phản hồi của VTVGo ra terminal để xem họ báo lỗi gì
        print(f"--> VTVGo phản hồi: {api_res.text}")
        
        data = api_res.json()
        m3u8_url = data.get("stream_url")
        
        if m3u8_url:
            # 3. Thành công -> Chuyển hướng trình phát thẳng sang luồng video
            return redirect(m3u8_url, code=302)
        else:
            # Báo lỗi chi tiết thẳng lên trình duyệt nếu không có luồng
            return f"Không tìm thấy luồng. Phản hồi VTVGo: {api_res.text}", 500
            
    except Exception as _:
        # Hiển thị lỗi gốc của Python lên trình duyệt nếu code bị crash
        return f"Lỗi thực thi mã: {str(_)}", 500

if __name__ == '__main__':
    app.run(debug=True)