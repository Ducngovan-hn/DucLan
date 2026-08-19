---
tieu_de: Tổng quan Wiki
loai: tong-quan
ngay_tao: 2026-07-17
ngay_cap_nhat: 2026-07-27
nguon: []
tags:
  - tong-quan
  - gioi-thieu
---

# Tổng quan Wiki — Dự án IPS 16

## Wiki này nói về gì?

Đây là "bộ não thứ hai" — một wiki tri thức bền vững, liên kết chéo, tích lũy dần cho **dự án IPS 16**. Thay vì truy xuất lại tài liệu thô mỗi lần hỏi (kiểu RAG — Retrieval-Augmented Generation, truy xuất tài liệu để sinh câu trả lời), wiki biên dịch kiến thức từ các nguồn thô trong `raw/` **một lần** rồi giữ cập nhật liên tục.

Mảng tri thức đầu tiên đã nạp: **hệ thống làm giàu bốn nấc thang của [[pham-thanh-long]]** — 16 trang gồm 2 thực thể, 13 khái niệm, 1 trang so sánh áp vào nghiệp vụ Dệt Bo Đức Lan. Điểm khởi đầu để đọc: [[bon-nac-thang-giau-co]].

## Hiện trạng nguồn

- **Nguồn đã nạp:** 1 bộ — sách "Cào Cào Lên Dốc" (6 file Word tóm tắt bài học, `raw/sách-Thầy-Phạm-Thành-Long/`). Xem [[sach-cao-cao-len-doc]].
- **File `.srt` trong `raw/`:** 0 — chưa có file phụ đề bài giảng nào.
- Khi người dùng thêm nguồn vào `raw/`, chạy quy trình **NẠP NGUỒN (Ingest)** trong `CLAUDE.md` và cập nhật con số này.

## Khoảng trống dữ liệu đã biết

- Chưa có số liệu thật của Dệt Bo Đức Lan (tài sản ròng, doanh thu, 5 chỉ số doanh số) → chưa định vị được doanh nghiệp đang ở nấc nào; xem 3 câu hỏi mở trong [[bon-nac-thang-ap-vao-det-bo-duc-lan]].
- Các thư mục `products/`, `customers/`, `competitors/` còn rỗng.

## Điều hướng

- 📇 Mục lục toàn wiki: [[index]] — danh mục mọi trang theo hạng mục. Đọc trang này TRƯỚC mọi truy vấn.
- 📓 Nhật ký hoạt động: [[log]] — lịch sử nạp nguồn / truy vấn / rà soát.
- ⚙️ Quy tắc & quy trình: `CLAUDE.md` (thư mục gốc vault) — schema vận hành.
