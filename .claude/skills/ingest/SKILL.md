---
name: ingest
description: >
  Nạp footage/nguồn đã cất vào WIKI. Hai nhánh theo đối tượng anh Đức gõ:
  "ingest my-life" (hoặc "ingest đời sống", "ingest cá nhân") → nạp footage cá nhân
  vào vault đời sống C:\Users\admin\my-life. "ingest xưởng" (hoặc "ingest xưởng bo",
  "ingest content xưởng") → nạp content xưởng vào wiki DucLan. Kích hoạt cả khi anh
  nói "nạp nhật ký tháng này", "sinh wiki từ footage", "ingest tháng 8", "viết nhật
  ký my-life". Gõ "ingest" trơ (không nói nhánh) → làm CẢ HAI (xưởng + my-life) cho
  ngày chưa ingest, không hỏi.
---

# Ingest — nạp footage/nguồn vào wiki

Gọi người dùng là **anh Đức**. Xác định nhánh từ chữ anh gõ:
- có **"my-life" / "đời sống" / "cá nhân" / "nhật ký"** → **chỉ Nhánh A (đời sống)**.
- có **"xưởng" / "xuong" / "bo" / "content xưởng"** → **chỉ Nhánh B (xưởng)**.
- **`ingest` trơ (không nói nhánh) → LÀM CẢ HAI** (anh Đức chốt 4/9): chạy Nhánh B (xưởng)
  rồi Nhánh A (my-life) cho (các) ngày chưa ingest. KHÔNG hỏi nữa.

## Nguyên tắc token (chung)
Đã xem lưới phân loại lúc `/offload` thì **KHÔNG đọc lại từng ảnh** — dùng nội dung đã
nắm để viết event. Chỉ đọc thêm ảnh/lưới cho ngày chưa từng xem. Định danh nơi: **tra
GPS trong `index/<ngày>.json` TRƯỚC** (reverse-geocode), chỉ hỏi khi GPS vắng.

---

## Nhánh A — ingest my-life (vault đời sống)

**Vault:** `C:\Users\admin\my-life` (Obsidian, có `.git` — CẨN THẬN, chỉ ghi trong
`wiki/` và `raw/photos/`, KHÔNG đụng thư mục khác).
**Nguồn footage:** `C:\Users\admin\footage-content\my-life` (bản nhẹ + index).

1. **Đọc `C:\Users\admin\my-life\CLAUDE.md`** để nhớ luật vault (14 mục): date-first,
   5 loại trang, 6 domain, tên file không dấu kebab, wikilink bắt buộc, event 5–10 dòng.
2. **Xem vault đã có gì** (`wiki/entities`, `wiki/events`) để không tạo trùng.
3. **Mỗi ngày footage → 1 event** `wiki/events/YYYY-MM-DD-mo-ta.md`:
   - frontmatter: `title / type: event / date / domain: [..] / entities: [[[x]], [[y]]] / source`.
   - 5–10 dòng, mọi entity nhắc tới đều `[[wikilink]]` (tên không dấu).
   - người thân giữ **slug quan hệ** `[[con-gai]]`, `[[vo]]`, `[[anh-duc]]` (anh Đức đã chốt).
   - chỗ không chắc ghi **(suy đoán)** / **(chưa rõ)**, không bịa.
   - **KHÔNG lưu thông tin cá nhân nhạy cảm** (anh Đức chốt 05/09): ngày sinh người thân,
     số điện thoại, địa chỉ nhà, số tài khoản, biển số... — dù suy ra được từ ảnh cũng
     KHÔNG ghi vào wiki/nhật ký. Chỉ ghi hoạt động/sự kiện, không ghi dữ liệu định danh.
   - **BẮT BUỘC mục "## Chi tiêu trong ngày"** (anh Đức chốt 3/9): bảng các khoản chi
     đọc được từ ảnh hoá đơn / chuyển khoản / đơn hàng ngày đó (Mục | Số tiền | Nguồn IMG),
     rồi dòng **Tổng ghi nhận được**. Chỉ ghi **số đúng trên ảnh**, không đoán; khoản không
     rõ số ghi "(chưa rõ số)"; ngày không có chứng từ ghi "Không có ghi nhận chi tiêu".
     Chỉ tính chi tiêu **đời sống** — chuyển khoản việc xưởng (XBO, tiền hàng/nhuộm/điện)
     KHÔNG phải chi tiêu cá nhân. Thêm `tai-chinh` vào `domain` khi có khoản chi.
     **Đối chiếu 6 lọ (anh Đức chốt 3/9):** ngoài chứng từ trên ảnh, đối chiếu thêm với
     **lọ chi tiêu trong DMO / bảng 6 lọ** (nguồn số thật của chi tiêu ngày — xem skill
     `dmo` / Excel 6 lọ) để không sót khoản không chụp hoá đơn; ghi rõ khoản nào từ ảnh,
     khoản nào từ 6 lọ.
4. **Tạo/cập nhật entity** (`wiki/entities/`, category `nguoi`/`noi`/`thiet-bi`) và
   **concept** (`wiki/concepts/`, ví dụ `chay-bo`, `hoc-tieng-trung`) khi tái diễn.
5. **Ảnh đại diện:** copy 1–5 ảnh chọn lọc/ngày từ `footage-content\my-life\ban-nhe\<ngày>\iphone`
   sang `raw/photos/<ngày>/` (vault chỉ giữ ảnh đại diện, KHÔNG đổ toàn bộ).
6. **Nhật ký:** khi anh yêu cầu "viết nhật ký", tạo `wiki/journal/YYYY-MM-nhat-ky-thang.md`
   (`type: journal`, `period: YYYY-MM`) tổng hợp các event theo 4 mảng, link event/entity.
7. **Log:** thêm 1 dòng `## [YYYY-MM-DD] ingest|journal | …` vào `wiki/log.md` (append-only).
8. Index.md dùng Dataview tự dựng — không sửa tay. Xong thì mở Obsidian cho anh xem:
   `Start-Process "obsidian://open?vault=my-life&file=<url-encoded path>"`.

---

## Nhánh B — ingest xưởng (wiki DucLan)

**Wiki:** `C:\Users\admin\DucLan\wiki` (vault xưởng bo — tri thức kinh doanh).
**Nguồn:** content xưởng `C:\Users\admin\footage-content\2026-content-xuong-bo`, HOẶC
file nguồn trong `raw/` (`.srt`, `.docx`...) khi anh chỉ định.

Theo **Quy trình NẠP NGUỒN** ở `DucLan/CLAUDE.md` mục 5:
1. Đọc/nắm nguồn (footage đã phân loại thì dùng lưới đã xem; tài liệu thì đọc file).
2. Trao đổi vài ý chính, xác nhận hướng trước khi ghi nhiều.
3. Viết **trang tóm tắt nguồn** `wiki/tom-tat-nguon/` (`loai: tom-tat-nguon`).
4. Cập nhật **`wiki/index.md`** — thêm dòng cho mọi trang mới.
5. Tạo/cập nhật **thực thể/khái niệm** liên quan (`wiki/thuc-the/`, `wiki/khai-niem/`,
   `wiki/products/`, `wiki/customers/`, `wiki/competitors/`), giữ liên kết chéo `[[...]]`.
6. Ghi chú mâu thuẫn nếu nguồn mới trái nguồn cũ.
7. Thêm 1 dòng `## [YYYY-MM-DD] ingest | <nguồn>` vào `wiki/log.md`.

Quy ước tên/loai/frontmatter theo `DucLan/CLAUDE.md` mục 4. Đây là wiki công việc —
KHÔNG trộn đời sống cá nhân vào đây (cái đó thuộc Nhánh A).

---

## Luật cứng
- Footage cá nhân ↔ xưởng đã tách 2 kho từ `/offload`; ingest đúng kho theo nhánh.
- Trước khi ghi vào bất kỳ thư mục nào, chắc chắn đó là wiki đích đúng (my-life vault
  vs DucLan wiki) — **đã từng nhầm vault một lần**, luôn kiểm.
- Việc nặng (nhiều ngày) chạy tuần tự, báo cáo cuối: số event/entity, câu hỏi mở.
