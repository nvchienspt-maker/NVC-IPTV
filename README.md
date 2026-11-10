# 📺 NVC Tivi - Hệ Thống Quản Lý & Tự Động Crawl Kênh Truyền Hình Việt Nam

<div align="center">

![NVC Tivi Banner](https://img.shields.io/badge/NVC_Tivi-v2.0-red?style=for-the-badge&logo=youtube&logoColor=white)
![Build Status](https://img.shields.io/badge/Status-100%25_Live_Channels-success?style=for-the-badge)
![Cloudflare Workers](https://img.shields.io/badge/Cloudflare_Workers-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)
![Python 3.11](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Hệ thống playlist M3U thông minh, tự động lọc link chết, cập nhật luồng phát sóng Full HD 1080p từ các đài truyền hình Việt Nam cho ứng dụng NVC Tivi.**

</div>

---

## 🌟 Tính Năng Nổi Bật

- 🎯 **100% Link Sống (Live Verified)**: Tự động kiểm tra HTTP status, phân tích header và xác thực luồng HLS/m3u8 thực tế để loại bỏ toàn bộ kênh chết hoặc ảnh tĩnh cảnh báo offline (`signal_low`).
- ⚡ **Đa Nguồn Dự Phòng (Multi-Source Fallback)**: Tích hợp nhiều CDN tốc độ cao (FPT VNNS 1080p, VTV Digital, đài phát thanh truyền hình địa phương) giúp tự động chuyển luồng dự phòng khi luồng chính gặp sự cố.
- 🚀 **Cloudflare Worker API Thông Minh**:
  - Hỗ trợ tải playlist trực tiếp qua URL: `/playlist.m3u` (hoặc `/playlist.m3u?proxy=1` để proxy qua worker).
  - Tích hợp công cụ tìm kiếm kênh tức thì: `/search?q=vtv1`.
  - Phân loại danh mục kênh theo nhóm: `/groups`.
  - Hỗ trợ đầy đủ CORS, giải mã DRM, bảo vệ nguồn luồng và giảm độ trễ khi chuyển kênh.
- 📺 **Chuẩn Hoá Toàn Diện**:
  - Tích hợp lịch phát sóng điện tử (EPG): `url-tvg="https://epgvn.vercel.app/epg.xml,https://epg.io.vn/epgc.xml"`.
  - Đồng bộ chuẩn thẻ `tvg-id`, `tvg-name`, `tvg-logo`, `group-title`.
  - Kho 170+ biểu trưng (logo) sắc nét chuẩn tỷ lệ tại thư mục `logos/`.

---

## 🏗️ Kiến Trúc Hệ Thống NVC Tivi

```mermaid
flowchart TD
    A["Nguồn phát sóng (CDNs / VTV / HTV / THVL / SCTV)"] --> B["NVC Crawler & Live Validator (scripts/nvc_crawler.py)"]
    B -->|Lọc bỏ kênh chết & Placeholder| C["File M3U Chuẩn Link Sống (nvctivi.m3u)"]
    B --> D["File JSON Metadata (nvctivi_channels.json)"]
    B --> E["Báo cáo chi tiết (REPORT_LIVE_CHANNELS.md)"]
    C --> F["Cloudflare Worker (worker/index.ts)"]
    F -->|Cung cấp luồng trực tiếp / Proxy| G["Ứng Dụng NVC Tivi / TiviMate / OTT Navigator / Smart TV"]
```

---

## 📋 Danh Mục 6 Nhóm Kênh Chuẩn Hoá

Tất cả các file M3U (bao gồm cả 3 file nguồn riêng và file master) đều được sắp xếp theo đúng thứ tự 6 nhóm chuẩn:

| STT | Nhóm Kênh | Nội Dung Kênh Tiêu Biểu |
| :---: | :--- | :--- |
| **1** | **VTV** | VTV1 HD, VTV2 HD, VTV3 HD, VTV4, VTV5, VTV5 Tây Nam Bộ, VTV5 Tây Nguyên, VTV7, VTV8, VTV9, Vietnam Today |
| **2** | **VTVCab** | ON Sports, ON Football, ON Golf, ON Cine, On Movies, ON Vie Giải Trí, ON Phim Việt, ON Kids, ON Bibi... |
| **3** | **HTV** | HTV1, HTV2 HD, HTV3, HTV7 HD, HTV9 HD, HTV Thể Thao, HTVC Thuần Việt, HTVC Gia Đình, HTVC Phim HD, HTVC Du Lịch, HTVC Ca Nhạc |
| **4** | **SCTV** | SCTV Phim Tổng Hợp, SCTV1, SCTV2, SCTV3, SCTV4, SCTV7, SCTV9, SCTV12, SCTV13, SCTV14, SCTV15, SCTV17, SCTV 4K... |
| **5** | **Quốc Tế** | HBO, Cinemax, CinemaWorld, Warner TV, AXN, Cartoon Network, Cartoonito, DreamWorks, Discovery, TLC, Animal Planet, BBC, CNN, CNBC, NHK World, KBS World... |
| **6** | **Địa Phương** | Vĩnh Long (THVL1-THVL4), Hà Nội (H1, H2), Hải Phòng, Đà Nẵng, Cần Thơ, Đồng Nai, Đồng Tháp, An Giang, Lâm Đồng, ANTV, QPVN... |

---

## 🚀 Hướng Dẫn Sử Dụng & Đường Dẫn M3U Trực Tiếp

### Dành cho người dùng cuối (App NVC Tivi, TiviMate, OTT Navigator, VLC)

Bạn có thể dán trực tiếp đường dẫn M3U sau vào bất kỳ ứng dụng xem IPTV nào:

* **File Tổng Hợp Master (Toàn diện nhất, gộp và lọc từ nhiều nguồn):**
  ```text
  https://raw.githubusercontent.com/nvchienspt-maker/NVC-IPTV/refs/heads/main/api/iptv/link0.m3u
  ```



* **Danh sách phát qua Cloudflare Worker (Có Proxy & tự động làm mới):**
  ```text
  Đang phát triển
  ```

---



## ⚙️ Các Endpoint Của Cloudflare Worker

| Phương thức | Đường dẫn | Mô tả chức năng |
| :---: | :--- | :--- |
| `GET` | `/` hoặc `/health` | Kiểm tra tình trạng hoạt động của Worker và số lượng kênh khả dụng |
| `GET` | `/playlist.m3u` | Cung cấp toàn bộ danh sách M3U chuẩn cho app |
| `GET` | `/playlist.m3u?proxy=1` | Cung cấp M3U với các luồng phát định tuyến qua Worker Proxy |
| `GET` | `/playlist.m3u?group=VTV` | Lọc danh sách kênh theo từng nhóm (VTV, HTV, SCTV...) |
| `GET` | `/search?q=vtv1` | API tìm kiếm thông tin kênh và link phát dưới định dạng JSON |
| `GET` | `/groups` | Thống kê số lượng kênh theo từng nhóm danh mục |
| `GET/POST`| `/channel?name=...` | Điều hướng (302) hoặc proxy luồng phát cho từng kênh cụ thể |

---


---

## 🛡️ Tuyên Bố Miễn Trừ Trách Nhiệm

* Dự án **NVC Tivi** không lưu trữ, phân phối hay tạo ra bất kỳ nội dung đa phương tiện nào.
* Toàn bộ các đường dẫn luồng phát (streaming links) được thu thập và tổng hợp từ các luồng phát thanh/truyền hình công khai trên Internet của các đài truyền hình tại Việt Nam.
* Vui lòng tôn trọng quyền tác giả và sở hữu trí tuệ của các đơn vị truyền thông.
