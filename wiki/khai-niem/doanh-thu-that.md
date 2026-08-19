---
tieu_de: Doanh thu thật và số nộp thuế
loai: khai-niem
ngay_tao: 2026-07-28
ngay_cap_nhat: 2026-07-28
nguon:
  - xưởng  bo Đức Lan/Sổ sách HKD/Xưởng Dệt Bo Đức Lan 2026.xlsx
  - xưởng  bo Đức Lan/Sổ sách HKD/Hóa đơn bán hàng/
tags:
  - tai-chinh
  - doanh-thu
  - quy-tac
---

# Doanh thu thật và số nộp thuế

**Hai con số hoàn toàn khác nhau. Không được dùng lẫn.** Anh Đức xác nhận 28/07/2026.

| | Nguồn | Lũy kế 2026 |
|---|---|---|
| **Doanh thu thật** | `production/Xưởng Dệt Bo Đức Lan 2026.xlsx`, sheet `TỔNG HỢP` khối TRẢ HÀNG | **1.158.185.500 đ** |
| Số nộp thuế | 26 hoá đơn trong `raw/.../Hóa đơn bán hàng/HĐ bán hàng/` | 158.736.500 đ |

Chênh **hơn 7 lần**. Lấy nhầm là sai lệch nghiêm trọng mọi phân tích.

## Quy tắc

- Doanh thu, lãi gộp, doanh thu theo khách → **luôn lấy từ sổ thật**.
- Hoá đơn bán hàng **chỉ dùng để tổng hợp tiền nộp thuế**, và **chỉ đọc khi anh Đức yêu
  cầu rõ**. Không tự ý mở để tính doanh thu.

## Hai tài liệu cũ cần đọc có cảnh giác

`production/bao-cao-2-tuan-2026-07-13-den-2026-07-27.md` và
`production/bang-so-van-hanh.xlsx` được dựng **trên số hoá đơn**, trước khi có quy tắc
này. Mọi con số "doanh thu" trong hai file đó thực chất là **số nộp thuế**:
38.092.500 đ (2 tuần), 158.736.500 đ (lũy kế 26/05–23/07), đơn trung bình 6.348.750 đ.
Không trích dẫn chúng như doanh thu.

## Cấu trúc sổ thật

Sheet `TỔNG HỢP` chứa ba khối cạnh nhau:

| Khối | Cột | Trường |
|---|---|---|
| TRẢ HÀNG | `A–E` | Tháng (`=MONTH(B)`) · Ngày · Mã KH · Nội dung · Thành tiền |
| THU TIỀN | `G–J` | (chưa dùng) |
| CHI PHÍ | `L–P` | Tháng · Ngày · Mã CP · Nội dung · Thành tiền (số âm) |

Các sheet `THU NHẬP`, `CHI PHÍ`, `LỢI NHUẬN` là **bảng báo cáo tự tính** bằng `SUMIFS`
trên **cả cột** — nên thêm dòng vào khối TRẢ HÀNG là an toàn, không hỏng công thức.

`LỢI NHUẬN` lấy doanh thu từ hàng tổng của `THU NHẬP`; hàng tổng này chỉ cộng các khách
**có dòng riêng** trong `THU NHẬP`. Vì vậy khách mới bắt buộc phải được thêm vào cả
sheet `Code` lẫn sheet `THU NHẬP`, nếu không doanh thu của họ sẽ **biến mất khỏi lãi lỗ**.
Lệnh `python tools/dh.py them-khach` làm đúng việc đó.

Xem thêm [[quy-trinh-don-hang]] · [[cu-phap-dat-bo]].
