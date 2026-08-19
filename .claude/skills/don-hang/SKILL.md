---
name: don-hang
description: >
  Tổng hợp đơn hàng và trả hàng cho Xưởng Bo Đức Lan. Dùng khi anh Đức gõ
  "tổng hợp đơn hàng" (đọc ảnh cú pháp đặt bo trong folder Đơn hàng/ rồi ghi vào
  Excel đơn hàng 2026) hoặc "tổng hợp trả hàng" (đọc nhóm Zalo "Trả hàng" rồi ghi
  vào sổ thật Xưởng Dệt Bo Đức Lan 2026). Kích hoạt cả khi anh nói "vào sổ đơn",
  "cập nhật đơn hàng", "vào sổ trả hàng", "chốt sổ hôm nay".
---

# Tổng hợp đơn hàng / trả hàng — Xưởng Bo Đức Lan

Gọi người dùng là **anh Đức**. Mọi việc ghi Excel làm qua `tools/dh.py` — **không tự
mở openpyxl, không tự sửa file Excel bằng tay.**

## Nguyên tắc token

Việc duy nhất tốn token là **đọc chữ trên ảnh / trên tin nhắn Zalo**. Mọi việc còn lại
script làm. Nên: không đọc lại ảnh cũ, không quét thư mục `Thiết kế/`, không mở các
sheet khác của workbook.

---

## A. Khi anh Đức gõ "tổng hợp đơn hàng" (bước 3)

```bash
python tools/dh.py anh-moi
```

1. Không có ảnh mới → **báo "không có ảnh mới" và DỪNG.** Không đọc gì thêm.
2. Có ảnh → `Read` từng đường dẫn ảnh thu nhỏ mà lệnh in ra (bản thu nhỏ, không đọc ảnh gốc).
3. Ghi JSON vào scratchpad theo schema dưới, rồi:

```bash
python tools/dh.py don-them --json <file.json> --thu
```

4. Xem cảnh báo. Nếu sạch → chạy lại **bỏ `--thu`** để ghi thật.
5. Thuật lại cho anh Đức: thêm mấy đơn / mấy dòng, mã Ms nào, cảnh báo gì.

### Schema JSON đơn hàng

```json
{
  "don": [{
    "ngay": "28/07/2026",
    "khach": "C Hoàn CB",
    "anh_sha1": "a1b2c3d4e5",
    "ghi_chu": "cán mềm",
    "hang": [{
      "mo_ta": "Xanh ya kẻ trắng",
      "ho": "Co", "kho": "40x7", "kieu": "kẻ",
      "mau": "Ya c Hằng + Trắng gạo",
      "kich_thuoc": "Size 40",
      "so_luong": 50, "dvt": "bộ"
    }]
  }]
}
```

- `anh_sha1` — lấy từ đầu ra của `anh-moi`. **Bắt buộc**, nếu thiếu thì ảnh sẽ bị đọc lại lần sau.

> ⚠ **Mã `Ms<n>` do script tự cấp KHÔNG phải mã thật.** Mã thật nằm ở nhóm Zalo
> "❇️NHÓM CV XƯỞNG BO" và đã tới **Ms81 (28/07/2026)**, trong khi script đếm từ sheet
> Excel nên đang cấp từ Ms61. Anh Đức biết việc này và sẽ chỉ cách xử lý sau — **đừng tự
> sửa mã, cũng đừng tự đi đọc nhóm CV** trừ khi anh yêu cầu.
>
> ⚠ **Khổ tay KHÔNG cố định 72x3.** Nhóm CV cho thấy Bform dùng `Ta75x3`. Khi ảnh không
> ghi khổ tay, ghi dòng tay với `"kho": ""` để script đánh dấu THIẾU KHỔ, rồi hỏi anh Đức —
> đừng mặc định 72x3.
- `ho` — họ mã: `Co` (cổ) · `Ta` (tay) · `Ga` · `GDO` · `BC` · `CMA`…
- `kho` — khổ, ví dụ `40x7`, `72x3`, `90x12`.
- `kieu` — chữ mô tả kiểu bo, **giữ nguyên văn anh Đức viết**. Script tự suy đuôi mã.
- `dvt` — `bộ` · `cái` · `cổ` · `kg`.
- `ma_don` — **đừng điền**, để script tự cấp `Ms<n>` tiếp theo.
- `ma_det` — chỉ điền khi anh Đức ghi thẳng mã trên giấy; còn lại để script ghép.

### Quy tắc đuôi mã dệt (anh Đức xác nhận 28/07/2026)

| Chữ trong cú pháp | Đuôi | Ví dụ |
|---|---|---|
| "2 kẻ chân" | `TH` | `Co42x7TH` |
| "Trơn" | `T` | `Co42x7T` |
| "Kẻ" | `K` | `Co42x7K` |
| còn lại | không đuôi + ` (usb)` | `Co42x7 (usb)` |

Script đã cài đúng thứ tự (kiểm "2 kẻ chân" trước "kẻ"). Thử nhanh:
`python tools/dh.py ma-det Co 42x7 "2 kẻ chân"`

---

## B. Khi anh Đức gõ "tổng hợp trả hàng" (bước 6)

1. Đọc mốc ngày đã xử lý:

```bash
python tools/dh.py soat
```

2. Mở Zalo Web trong Chrome, vào nhóm **"Trả hàng"**. Dùng
   `mcp__Claude_Browser__get_page_text` (KHÔNG dùng `read_page` — đắt hơn 3–5 lần).
   Cuộn lùi **vừa đủ** tới mốc, không cuộn hết nhóm.
3. Trích từng lần trả hàng → JSON:

```json
{
  "tra": [
    {"ngay": "20/07/2026", "khach": "C Hoàn CB",
     "noi_dung": "ya kẻ trắng 260 bộ", "thanh_tien": 1690000}
  ]
}
```

- `noi_dung` — mô tả gọn kiểu sổ đang dùng: *màu + kiểu + SL + đvt*, nhiều món nối bằng ` + `.
  Ví dụ thật trong sổ: `đỏ trơn 500b + đỏ kẻ trắng 500b`, `cạp lô 1 đen 1000 cái`.
- `thanh_tien` — **lấy nguyên con số anh Đức ghi trong tin nhắn. TUYỆT ĐỐI KHÔNG tự tính
  từ số lượng × đơn giá.** Nhận được cả `"6.500.000"` và `"2tr9"`.

4. Chạy khô rồi ghi thật:

```bash
python tools/dh.py tra-them --json <file.json> --thu
python tools/dh.py tra-them --json <file.json>
```

5. Thuật lại: mấy dòng, tổng tiền, và nhắc anh Đức mở sheet `LỢI NHUẬN` kiểm tháng đó
   có tăng đúng số tiền không.

---

## Khi bị chặn

| Cảnh báo | Xử lý |
|---|---|
| `không nhận ra khách '<tên>'` | Hỏi anh Đức mã KH, rồi `python tools/dh.py them-alias "<tên>" <ma_kh>` |
| `KHÔNG có file thiết kế` | **Không tự sửa mã.** Báo anh Đức, hỏi mã đúng. |
| `File đang mở trong Excel` | Nhờ anh Đức đóng file rồi chạy lại. |
| Chữ trên ảnh không đọc được | Hỏi anh Đức đúng ô đó. **Không đoán.** |

## Tuyệt đối không

- **Không ghi vào `raw/`** — bất biến, chỉ đọc.
- **Không lấy doanh thu từ `Hóa đơn bán hàng/`** — đó là số nộp thuế, không phải doanh thu
  thật (kém sổ thật ~7 lần). Chỉ đọc khi anh Đức yêu cầu rõ.
- **Không tự nhắn tin Zalo.** Bước 1, 2, 4, 5 là việc của anh Đức.
- **Không sửa ô có công thức** trong workbook.
