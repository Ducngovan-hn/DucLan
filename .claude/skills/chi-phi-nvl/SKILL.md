---
name: chi-phi-nvl
description: >
  Tính chi phí nguyên vật liệu (sợi + nhuộm + dớ) của Xưởng Dệt Bo Đức Lan theo
  tháng, từ khối TRẢ HÀNG trong sổ thật. Dùng khi anh Đức nói "tính chi phí NVL",
  "chi phí nguyên liệu tháng mấy", "chi phí xưởng tháng 7", "giá thành sợi nhuộm
  dớ", "tháng này tốn bao nhiêu nguyên liệu", hoặc đưa số lượng bộ/cổ/tay/cạp/gấu
  rồi hỏi hết bao nhiêu tiền nguyên liệu. KHÔNG dùng cho doanh thu, lợi nhuận, hay
  giá bán (đó là việc của skill so-sach / don-hang).
---

# Chi phí NVL — Xưởng Dệt Bo Đức Lan

Gọi người dùng là **anh Đức**. Đây là chi phí **nguyên liệu** (sợi+nhuộm+dớ),
KHÔNG gồm nhân công, điện, hao mòn máy, vận chuyển, lặt vặt.

> Skill này lấy số từ **sổ thật (Excel)**, không đọc Zalo. Nhưng nếu có lúc cần đối chiếu
> tin nhắn Zalo, theo **quy tắc chung mọi việc xưởng (anh Đức chốt 21/08/2026):** đọc qua
> **Zalo PC gom chữ** (`zalo_dump.mjs`) — **KHÔNG** dùng Zalo Web, **KHÔNG** chụp ảnh, **KHÔNG** `read_page`.

Định mức & công thức đầy đủ: [[chi-phi-nguyen-lieu]] (`wiki/khai-niem/chi-phi-nguyen-lieu.md`).

## Định mức (chốt 2026-08-21)

| Khoản | Giá | | Đơn vị | Khối lượng | Chi phí/đơn vị |
|---|---|---|---|---|---|
| Sợi | 42.000 đ/kg | | 1 bộ (polo = cổ+tay) | 0,03365 kg | 2.288 đ |
| Nhuộm | 23.000 đ/kg | | 1 cổ lẻ | 0,01945 kg | 1.323 đ |
| Dớ | 3.000 đ/kg | | 1 tay lẻ | 0,0142 kg | 966 đ |
| **Gộp** | **68.000 đ/kg** | | 1 cạp quần (10 cạp=0,65kg) | 0,065 kg | 4.420 đ |
| | | | 1 gấu (10 gấu=0,985kg) | 0,0985 kg | 6.698 đ |

Mọi thành phẩm đều gồm đủ sợi+nhuộm+dớ → luôn nhân **68.000 đ/kg**.

## Quy trình

**Việc duy nhất cần LLM đọc** là bóc số lượng từ cột NỘI DUNG (chữ tự do). Mọi
tính toán do script làm.

### 1. Liệt kê khối trả hàng của tháng

```bash
python tools/chi_phi_nvl.py liet-ke --thang 7
```

(`--nam` mặc định 2026.) Lệnh in mỗi đơn một dòng: `ngày | mã KH | nội dung [tiền]`.

### 2. Bóc sản lượng từ NỘI DUNG → cộng dồn theo nhóm

Quy ước đơn vị trong nội dung:
- `b` / `bộ` → **bộ**   ·   `cổ` → **cổ lẻ**   ·   `tay` → **tay lẻ**
- `cạp` / `cạp lô` / dòng khách "tuan" ghi "N cái" → **cạp**
- `gấu` → **gấu**   ·   `kg` → **bán theo cân**

Bẫy cần tránh:
- Dòng có **tổng cuối** (`… = 1200b`, `… = 500 cái`, `… = 35kg`) → dùng số **tổng**,
  KHÔNG cộng lại các phần (tránh đếm trùng).
- Có **kg thực** ghi thẳng → ưu tiên kg thực, bỏ số cái/bộ. Vd `rêu gân 700 cái = 88kg` → **88kg**
  (hàng gân nặng hơn định mức bộ chuẩn ~3,7 lần).
- Tên màu chứa chữ dễ nhầm (vd "cổ vịt" là màu, không phải cổ lẻ) → đọc kỹ ngữ cảnh.

Ghi ra JSON (khoá thiếu = 0):

```json
{"thang":7, "bo":24879, "co":11150, "tay":1490, "cap":2540, "gau":0, "kg":196.0}
```

### 3. Tính

```bash
python tools/chi_phi_nvl.py tinh --json <file.json>
```

Script in bảng từng nhóm + tổng khối lượng + tổng chi phí.

### 4. Thuật lại cho anh Đức

Nêu tổng chi phí, bảng đóng góp từng nhóm, và **các dòng nội dung nhập nhằng đã suy
đoán** để anh soát. Nhắc rõ đây chỉ là chi phí nguyên liệu.

## Đối chiếu tháng 7/2026 (mốc kiểm thử)

Sản lượng bóc: 24.879 bộ · 11.150 cổ · 1.490 tay · 2.540 cạp · 0 gấu · 196 kg bán cân.
→ ~1.436 kg → **≈ 97,67 triệu đ**. Nếu chạy lại ra khác nhiều là có sai ở bước bóc.

> Số này lấy từ **file Excel local** (bản cũ). Bản **Google Sheet** ghi chi tiết hơn
> (có "áo khoác", "cạp quần", số cái) nên T7 ra **29.193 bộ** — dùng bản sống Google Sheet
> khi anh Đức yêu cầu tính từ đó.

---

## Lấy dữ liệu & ghi vào Google Sheet "Xưởng Dệt Bo Đức Lan 2026"

Google Sheet ID `1IxoAYIrmGZqWLqnpLhEsgCPOeG9H17udabQjmGDg7nI`. Đọc/ghi qua Chrome
(`credentials:'include'`). Kỹ thuật ghi ô: xem `so-sach-duc-lan/references/ghi-google-sheets.md`.

**Bóc sản lượng tự động (đã kiểm, khớp bản thô):**
- Nội dung khối TRẢ HÀNG (cột D) ghi lẫn `500b`/`500 bộ` · `cổ` · `tay` · `cạp`/`áo khoác` (=**cái**) · `kg`.
- **Áo khoác = gấu a Tuân** (0,0985 kg/cái). **Gân bán cân** (`gân` mà không phải cạp) → lấy thẳng **cột THÀNH TIỀN (E)**, không quy 68k/kg. "cạp quần gân" vẫn là **cạp**.
- Regex bắt cả `b` viết tắt; bỏ segment chứa `tổng` (tránh đếm trùng); phân `cái` theo ngữ cảnh áo khoác/cạp.
- Đối chiếu tự động "Tổng ghi" vs "tổng cộng phần" để lọc dòng cần rà — cả 8 tháng chỉ ~2 dòng lệch (dòng trộn áo khoác + cạp).
- Kết quả 2026: T1–T8 tổng NVL **≈ 652,09 triệu** (định mức 474,6tr + gân 177,5tr).

**⚠️ CẠM BẪY GHI SHEET CHI PHÍ — ĐỌC KỸ (đã từng đè nhầm dòng):**
1. Sheet **CHI PHÍ** dùng đối tượng **"Bảng_5"** (Google Table): **hàng 1** tiêu đề, **hàng 2 trống**,
   **hàng 3 = header** (`Tr Tháng | Mã CP | 1 | 2 | … | 12 | Cột1..`), **Sợi = hàng 4, Nhuộm = 5, Dớ = 6**.
   Cột **C = tháng 1 … J = tháng 8 … N = tháng 12**.
2. **gviz CSV BỎ dòng trống & gộp tiêu đề** → chỉ số dòng CSV **KHÁC** số hàng thật (A1).
   **KHÔNG suy số hàng từ CSV.** Luôn nav bằng `t-name-box` tới ô rồi **chụp màn hình / đọc formula bar** xác nhận đúng hàng trước khi dán.
3. 3 dòng Sợi/Nhuộm/Dớ là **công thức `=SUMIFS('TỔNG HỢP'!…)`** tự kéo **tiền THỰC CHI**, nuôi sheet
   **LỢI NHUẬN**. Đè bằng ước tính giá vốn (NVL) sẽ phá công thức và làm lợi nhuận lệch lớn — **chỉ đè khi anh Đức xác nhận rõ**; nếu không, thêm dòng riêng ngoài vùng bảng.
4. Trước khi đè: **backup giá trị cũ** (đọc CSV) và nhớ **Ctrl+Z hoàn tác được** (thoát edit bằng
   Escape trước khi Ctrl+Z, nếu ô đang mở soạn thảo).
5. Ghi giá vốn = **số âm**, tách theo tỉ lệ **42/23/3** (sợi/nhuộm/dớ) trên tổng NVL mỗi tháng.
   Đã ghi T1–T8/2026 (anh Đức chốt đè ngày 21/08/2026).
