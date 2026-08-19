---
tieu_de: Cú pháp đặt bo
loai: khai-niem
ngay_tao: 2026-07-28
ngay_cap_nhat: 2026-07-28
nguon:
  - xưởng  bo Đức Lan/Đơn hàng/HG 24.7.png
  - xưởng  bo Đức Lan/Đơn hàng/Bform 28.7.png
tags:
  - quy-trinh
  - don-hang
  - ma-det
---

# Cú pháp đặt bo

Cú pháp anh Đức tự viết khi tiếp nhận đơn khách nhắn trên nhóm Zalo (bước 1 của
[[quy-trinh-don-hang]]), rồi chụp ảnh thả vào `raw/xưởng  bo Đức Lan/Đơn hàng/`.

## Dạng thực tế

Ảnh là **ảnh chụp tin nhắn Zalo**, không phải chữ viết tay.

```
⬤ 24/7: Cty Hoàng Giang đặt bo:
Tím than 40x7: 438 bộ
```
(nguồn: HG 24.7.png, 15:03)

```
⬤ 28/7: Cty Bform đặt bo Lô 3:
- Trắng kẻ xanh bích: 432 bộ
```
(nguồn: Bform 28.7.png, 13:48)

Khung chung:

```
<ngày d/m>: <Tên khách> đặt bo[ Lô <N>]:
<màu + kiểu>[ <khổ>]: <số lượng> <đơn vị>
```

- Dòng đầu: ngày · tên khách · (tuỳ chọn) số lô.
- Mỗi dòng hàng: mô tả màu/kiểu, khổ nếu có, rồi `: <SL> <đvt>`.
- Đơn vị: `bộ` · `cái` · `cổ` · `kg`.
- Tin nhắn có thể kèm lời dặn giao hàng ("Bo gửi c Ngân giúp e nhé") — vào ô Ghi chú.

## Quy tắc đuôi mã dệt

Anh Đức xác nhận 28/07/2026:

| Chữ trong cú pháp | Đuôi | Ví dụ |
|---|---|---|
| "2 kẻ chân" | `TH` | `Co42x7TH` |
| "Trơn" | `T` | `Co42x7T` |
| "Kẻ" | `K` | `Co42x7K` |
| còn lại | không đuôi + ` (usb)` | `Co42x7 (usb)` |

**Bẫy khi lập trình:** phải kiểm `"2 kẻ chân"` **trước** `"kẻ"`, vì chuỗi "2 kẻ chân"
cũng chứa chữ "kẻ". `tools/dh.py` đã cài đúng thứ tự này.

Họ mã lấy từ thư mục thiết kế: `Co` (cổ) · `Ta` (tay) · `Ga` · `GDO` · `BC` · `CMA` ·
`COLACO`… Mã đầy đủ = `<Họ><khổ><đuôi>`. Mọi mã sinh ra đều được đối chiếu với **835 mã
có thật** trong `raw/xưởng  bo Đức Lan/Thiết kế/`; không khớp thì chặn, không ghi.

## Ba quy ước diễn giải

Anh Đức xác nhận 28/07/2026, vì cú pháp không ghi đủ mọi trường:

1. **1 bộ = cổ + tay** → mỗi dòng "N bộ" tách thành **2 dòng**: `Co<khổ>` N bộ và
   `Ta<khổ tay>` N cái.
2. ~~**Khổ tay mặc định `72x3`**~~ — **QUY ƯỚC NÀY ĐÃ SAI**, xem mục "Nhóm CV Xưởng Bo" bên dưới.
   Kiểu tay vẫn theo đúng kiểu của cổ.
3. **Mỗi màu một dòng riêng** trong ô Màu sắc. "Trắng kẻ xanh bích" → ô chứa hai dòng:
   `Trắng` và `Xanh bích`.

## Nhóm CV Xưởng Bo — nguồn có mã dệt chính xác

Nhóm Zalo **"❇️NHÓM CV XƯỞNG BO"** (4 thành viên, có thợ vận hành máy) chứa cú pháp anh
Đức tự chuẩn hoá ở bước 3 của [[quy-trinh-don-hang]], **đầy đủ hơn hẳn** ảnh trong folder:

```
❇️Ms81 (28/7): nâu Bform
- Màu: Nâu c Hiệp
- Số lượng: 200 bộ
- Mẫu:
Co42x75T
Ta75x3T
```
(nguồn: nhóm CV Xưởng Bo, 28/07/2026 10:20)

Hai điều nguồn này làm lộ ra, đều **phủ định suy đoán trước đó**:

1. **Khổ tay không cố định 72x3.** Bform dùng `Ta75x3`. Suy đoán "mặc định 72x3" dựa trên
   Ms54–Ms56 của C Hoàn CB là kết luận vội từ một khách duy nhất.
2. **Mã `Ms<n>` thật do anh Đức đánh trong nhóm CV**, không suy ra được từ file Excel.
   Tại 28/07/2026 đã tới **Ms81** (Ms79, Ms80, Ms81 đều trong ngày), trong khi sheet
   `Đơn hàng 2026` mới có tới Ms60 nên script cấp nhầm từ Ms61.

Anh Đức quyết định (28/07/2026): **vẫn đọc từ ảnh trong folder `Đơn hàng/`**, không đọc
nhóm CV; việc lệch mã Ms tạm để đó, anh sẽ chỉ cách điều chỉnh sau.

## Khi thiếu khổ

Cú pháp đôi khi không ghi khổ (ví dụ đơn Bform 28/7). Khi đó vẫn ghi đơn vào Excel để
**không sót đơn**, nhưng ô Mẫu dệt để trống và ô Ghi chú đánh dấu `⚠ THIẾU KHỔ — cần điền`.
Lệnh `python tools/dh.py soat` sẽ nhắc cho tới khi anh Đức điền xong.

Xem thêm [[quy-trinh-don-hang]] · [[doanh-thu-that]].
