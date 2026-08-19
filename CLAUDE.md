# CLAUDE.md — Schema & Cẩm Nang Vận Hành "Bộ Não Thứ Hai"

> File này là **cấu hình then chốt** của vault. Mọi phiên làm việc sau đều bắt đầu bằng việc đọc file này để nhớ lại quy tắc trước khi làm bất cứ việc gì.

---

## 1. Triết lý

Đây là một **wiki tri thức bền vững** ("bộ não thứ hai"), KHÔNG phải hệ thống RAG (Retrieval-Augmented Generation — sinh câu trả lời bằng cách truy xuất tài liệu thô mỗi lần hỏi).

Khác biệt cốt lõi:

- **RAG truyền thống:** mỗi lần hỏi lại đi truy xuất tài liệu thô từ đầu, suy luận lại từ đầu, không tích lũy gì.
- **Hệ thống này:** DUY TRÌ MỘT WIKI liên kết chéo, tích lũy dần. Mỗi khi nạp nguồn mới, LLM (mô hình ngôn ngữ lớn) ĐỌC nó, trích thông tin then chốt, rồi TÍCH HỢP vào wiki hiện có: cập nhật trang thực thể, chỉnh tóm tắt chủ đề, ghi chú mâu thuẫn với dữ liệu cũ.

Nguyên tắc vàng: **Kiến thức được biên dịch MỘT LẦN rồi giữ cập nhật, không suy lại mỗi lần hỏi.** Wiki là **tài sản bền vững, lớn dần theo thời gian**.

Khi trả lời một câu hỏi mà sinh ra giá trị mới (so sánh, phân tích, phát hiện mối liên hệ), hãy **lưu ngược giá trị đó thành trang wiki mới** để lần sau không phải suy lại.

---

## 2. Kiến trúc ba tầng (+ thư mục sản phẩm)

| Tầng | Thư mục / File | Quyền | Vai trò |
|---|---|---|---|
| 1. Nguồn thô | `raw/` | **CHỈ ĐỌC — BẤT BIẾN** | Nguồn chân lý. KHÔNG BAO GIỜ sửa, xóa hay ghi đè. Dự án này dùng các file `.srt` (phụ đề) làm nguồn. Tài nguyên đính kèm để trong `raw/assets/`. |
| 2. Wiki | `wiki/` | LLM sở hữu hoàn toàn | Các file markdown do LLM sinh ra: trang tóm tắt nguồn, trang thực thể, trang khái niệm, bảng so sánh, tổng quan, tổng hợp. LLM tạo, cập nhật, giữ liên kết chéo nhất quán. |
| 3. Schema | `CLAUDE.md` | Cấu hình | Quy tắc tổ chức wiki, quy ước, quy trình làm việc. Chính là file này. |
| (+) Sản phẩm | `production/` | Đầu ra theo lệnh | Các file sinh ra **khi người dùng ra lệnh**: blog, bài đăng Facebook, kịch bản video, file PDF, hoặc tài liệu khác. KHÔNG trộn lẫn với `wiki/`. |

**Quy tắc bất khả xâm phạm:** `raw/` là nguồn chân lý bất biến — chỉ đọc, không bao giờ ghi (ngoại lệ duy nhất: người dùng tự thêm file nguồn mới vào).

### 2.1. Sổ sống — hai workbook được ghi

Hai file trong `production/` là **sổ sống**, LLM được ghi qua `tools/dh.py`:

| File | Vai trò |
|---|---|
| `production/Xưởng Dệt Bo Đức Lan 2026.xlsx` | **SỔ THẬT** — trả hàng, doanh thu, chi phí, lãi lỗ |
| `production/Tong-hop-don-hang-Xbo-Duc-Lan-2026.xlsx` | Sổ đơn hàng: mẫu dệt · màu · kích thước · số lượng |

Hai file cùng tên trong `raw/xưởng  bo Đức Lan/Sổ sách HKD/` là **bản đóng băng đã cũ** —
chỉ đọc, không dùng, không đối chiếu. Bản sống duy nhất nằm ở `production/`.

**Không ghi Excel bằng tay.** Mọi thao tác ghi đi qua `tools/dh.py` để giữ được sao lưu,
chống trùng, và kiểm tra file có đang mở trong Excel không.

### 2.2. Doanh thu thật ≠ số nộp thuế

Doanh thu **luôn** lấy từ sổ thật (khối TRẢ HÀNG, sheet `TỔNG HỢP`).
Hoá đơn trong `raw/.../Hóa đơn bán hàng/` **chỉ để tổng hợp tiền nộp thuế**, chỉ đọc khi
anh Đức yêu cầu rõ. Hai con số chênh **hơn 7 lần** (1.158.185.500 đ so với 158.736.500 đ
tại 28/07/2026). Chi tiết ở [[doanh-thu-that]].

---

## 3. Quy ước ngôn ngữ

- Toàn bộ vault và schema viết bằng **TIẾNG VIỆT**.
- **Mọi thứ hiển thị ra màn hình cho anh Đức đều bằng TIẾNG VIỆT** — không chỉ câu trả lời mà cả **phần suy nghĩ (thinking)**, mô tả tác vụ, tên việc trong danh sách công việc. Suy nghĩ bằng tiếng Việt ngay từ đầu, không nghĩ tiếng Anh rồi dịch. Lý do: anh Đức theo dõi cả quá trình suy luận để biết có đi đúng hướng không.
- Ngoại lệ duy nhất: **code, tên lệnh, tên file, log của công cụ** giữ nguyên, không dịch.
- Luôn gọi người dùng là **anh Đức**.
- Nếu buộc phải dùng thuật ngữ nước ngoài, **luôn kèm chú thích tiếng Việt trong ngoặc ngay lần đầu xuất hiện**. Ví dụ: "embedding (vector nhúng)", "frontmatter (phần siêu dữ liệu đầu file)", "orphan (trang mồ côi)".

---

## 4. Quy ước trang wiki

### 4.1. Tên file
- Chữ **thường**, **không dấu**, nối bằng **gạch ngang**.
- Ví dụ: `pham-thanh-long.md`, `chien-luoc-gia.md`, `ips-16-tap-01.md`.

### 4.2. Frontmatter YAML (bắt buộc mở đầu mỗi trang)

```yaml
---
tieu_de: Tên hiển thị đầy đủ của trang
loai: thuc-the        # thuc-the | khai-niem | tom-tat-nguon | so-sanh | tong-quan | tong-hop
ngay_tao: YYYY-MM-DD
ngay_cap_nhat: YYYY-MM-DD
nguon:                # danh sách file nguồn tham chiếu (trong raw/)
  - ten-nguon-1.srt
  - ten-nguon-2.srt
tags:
  - the-loai
  - chu-de
---
```

Giá trị hợp lệ của `loai`:

| Giá trị | Ý nghĩa | Thư mục |
|---|---|---|
| `thuc-the` | Người, tổ chức, địa điểm, sản phẩm, sự vật cụ thể | `wiki/thuc-the/` |
| `khai-niem` | Ý tưởng, phương pháp, nguyên lý, thuật ngữ trừu tượng | `wiki/khai-niem/` |
| `tom-tat-nguon` | Tóm tắt một file nguồn cụ thể trong `raw/` | `wiki/tom-tat-nguon/` |
| `so-sanh` | Bảng/trang đối chiếu hai hay nhiều thực thể/khái niệm | `wiki/so-sanh/` |
| `tong-quan` | Trang tổng quan toàn vault hoặc một mảng chủ đề lớn | `wiki/` (gốc) |
| `tong-hop` | Trang tổng hợp/phân tích liên nguồn, sinh ra từ truy vấn có giá trị | `wiki/` (gốc) |
| `san-pham` | Sản phẩm của Dệt Bo Đức Lan (một loại `thuc-the` chuyên biệt) | `wiki/products/` |
| `khach-hang` | Khách hàng / đối tác (một loại `thuc-the` chuyên biệt) | `wiki/customers/` |
| `doi-thu` | Đối thủ cạnh tranh (một loại `thuc-the` chuyên biệt) | `wiki/competitors/` |

> **Ghi chú:** `san-pham`, `khach-hang`, `doi-thu` là ba **phân loại thực thể chuyên biệt** cho nghiệp vụ của Đức Lan. Về bản chất chúng vẫn là thực thể; tách riêng thư mục để tra cứu nhanh theo nghiệp vụ. Thực thể chung chung khác vẫn để trong `wiki/thuc-the/`.

### 4.3. Liên kết chéo
- Nối các trang bằng cú pháp `[[ten-file-khong-duoi]]` (không kèm đuôi `.md`).
- Ví dụ: `Xem thêm [[pham-thanh-long]] và [[chien-luoc-gia]]`.
- Ưu tiên liên kết **hai chiều** khi hợp lý: nếu trang A trỏ tới B thì cân nhắc B trỏ lại A.
- Một liên kết `[[...]]` chưa có file tương ứng là **chấp nhận được** — nó đánh dấu trang đáng viết sau, không phải lỗi.

### 4.4. Trích dẫn nguồn
- **Mọi khẳng định rút ra từ nguồn phải TRÍCH DẪN**, theo dạng:
  `(nguồn: ten-file.srt, mốc thời gian nếu có)`.
- Ví dụ: "Diễn giả nhấn mạnh tư duy dài hạn (nguồn: ips-16-tap-01.srt, 00:04:12)."
- Không trích dẫn = không được coi là dữ kiện. Suy luận riêng của LLM phải ghi rõ là suy luận, không trình bày như dữ kiện từ nguồn.

---

## 5. Quy trình "NẠP NGUỒN" (Ingest — nạp và tích hợp nguồn mới)

> Một nguồn có thể **chạm 10–15 trang** wiki. Mặc định nạp **TỪNG nguồn một, có giám sát**. Hỗ trợ nạp hàng loạt (batch) nếu người dùng yêu cầu rõ.

Checklist đánh số — làm đủ, đúng thứ tự:

1. **Đọc** file nguồn trong `raw/`.
2. **Trao đổi** với người dùng vài ý chính rút ra được (xác nhận hướng trước khi ghi nhiều).
3. **Viết trang tóm tắt** trong `wiki/tom-tat-nguon/` (`loai: tom-tat-nguon`).
4. **Cập nhật** `wiki/index.md` — thêm một dòng cho mọi trang mới.
5. **Cập nhật / tạo các trang thực thể và khái niệm** liên quan khắp wiki (`wiki/thuc-the/`, `wiki/khai-niem/`), giữ liên kết chéo nhất quán.
6. **Ghi chú mâu thuẫn** nếu nguồn mới mâu thuẫn nguồn cũ — nêu rõ trang nào, khẳng định nào, nguồn nào, để người dùng phân xử.
7. **Thêm 1 dòng** vào `wiki/log.md` (mục `ingest`).

---

## 6. Quy trình "TRUY VẤN" (Query — trả lời câu hỏi từ wiki)

1. Đọc `wiki/index.md` **TRƯỚC** để tìm các trang liên quan.
2. Đọc các trang đó (lần theo liên kết chéo nếu cần).
3. Tổng hợp câu trả lời **CÓ TRÍCH DẪN** (trỏ về nguồn gốc trong `raw/`).
4. Nếu câu trả lời có **giá trị tích lũy** (so sánh, phân tích, phát hiện mối liên hệ mới), **đề nghị người dùng lưu ngược** thành trang wiki mới (`loai: tong-hop` hoặc `so-sanh`) để tích lũy tri thức.
5. Nếu truy vấn đáng lưu vết, ghi 1 dòng `query` vào `wiki/log.md`.

### 6.1. Format đầu ra "Tóm tắt 1 trang cho cuộc họp"

Khi người dùng yêu cầu **"tóm tắt 1 trang cho cuộc họp"** (hoặc "bản họp", "meeting brief"), trình bày câu trả lời gọn trong **đúng 1 trang** theo khung sau — ngắn, quét mắt được, ai cũng đọc hiểu:

```
# [Chủ đề] — Tóm tắt cuộc họp (YYYY-MM-DD)

**Mục tiêu:** 1 câu — cuộc họp này cần quyết định / làm rõ điều gì.

**Bối cảnh:** 2–3 câu — tình hình hiện tại, vì sao bàn việc này.

**Điểm chính (3–5 gạch đầu dòng):**
- Ý chính, kèm số liệu nếu có (trích dẫn: nguồn: ten-file.srt, mốc thời gian)
- ...

**Số liệu / dữ kiện then chốt:** liệt kê ngắn các con số quan trọng (mỗi con số một trích dẫn).

**Rủi ro / mâu thuẫn:** điểm cần lưu ý, hoặc mâu thuẫn giữa các nguồn (nếu có).

**Đề xuất hành động:** 2–4 việc cụ thể, ai làm — làm gì — khi nào.

**Câu hỏi mở:** những điều wiki chưa trả lời được, cần quyết trong họp.
```

Quy tắc của format này:
- **Giới hạn 1 trang** (~250–400 từ). Cắt bớt chi tiết phụ, giữ cái ra quyết định được.
- Vẫn **TRÍCH DẪN** đầy đủ như mọi câu trả lời khác — mỗi dữ kiện trỏ về nguồn trong `raw/`.
- Suy luận của LLM (không phải dữ kiện từ nguồn) phải ghi rõ là **nhận định**.
- Nếu người dùng muốn lưu lại, xuất ra `production/` (không phải `wiki/`) vì đây là sản phẩm theo lệnh; đặt tên dạng `hop-<chu-de>-YYYY-MM-DD.md`.

---

## 7. Quy trình "RÀ SOÁT" (Lint — kiểm tra sức khỏe wiki)

Rà soát định kỳ, kiểm tra:

- **Mâu thuẫn** giữa các trang (cùng dữ kiện, khác kết luận).
- **Khẳng định lỗi thời** (nguồn mới đã thay thế nhưng trang cũ chưa cập nhật).
- **Trang mồ côi** (orphan — không có liên kết nào trỏ đến).
- **Khái niệm quan trọng chưa có trang riêng** (xuất hiện nhiều nơi nhưng chưa được tách trang).
- **Thiếu liên kết chéo** (hai trang liên quan nhưng chưa nối `[[...]]`).
- **Khoảng trống dữ liệu** (câu hỏi hợp lý mà wiki chưa trả lời được).

Kết quả rà soát: **đề xuất câu hỏi mới cần làm rõ** và **nguồn cần đi tìm**. Ghi 1 dòng `lint` vào `wiki/log.md`.

---

## 8. Vai trò của `index.md` và `log.md`

- **`wiki/index.md`** — Mục lục sống của toàn wiki, danh mục MỌI trang, tổ chức theo hạng mục (Thực thể / Khái niệm / Tóm tắt nguồn / So sánh / Khác). Mỗi trang một dòng: `- [[ten-file]] — tóm tắt một dòng`. **Cập nhật MỖI lần nạp nguồn.** Đây là điểm khởi đầu của mọi truy vấn.

- **`wiki/log.md`** — Nhật ký **CHỈ-THÊM** (append-only — chỉ thêm cuối, không sửa mục cũ), theo thời gian. Mỗi mục bắt đầu bằng tiền tố nhất quán để grep được:
  - `## [YYYY-MM-DD] ingest | Tên nguồn`
  - `## [YYYY-MM-DD] query | Nội dung`
  - `## [YYYY-MM-DD] lint | Nội dung`

  Lấy 5 mục gần nhất: `grep "^## \[" wiki/log.md | tail -5`.

---

## 9. Bản đồ thư mục

```
DucLan/
├── CLAUDE.md              # Schema này — đọc đầu mỗi phiên
├── raw/                   # Tầng 1: nguồn thô, BẤT BIẾN (chỉ đọc)
│   └── assets/            # Tài nguyên đính kèm của nguồn
├── wiki/                  # Tầng 2: wiki do LLM sở hữu
│   ├── index.md           # Mục lục sống — cập nhật mỗi lần nạp nguồn
│   ├── log.md             # Nhật ký chỉ-thêm
│   ├── tong-quan.md       # Trang tổng quan toàn wiki
│   ├── thuc-the/          # Trang thực thể (chung)
│   ├── products/          # Sản phẩm của Đức Lan (loai: san-pham)
│   ├── customers/         # Khách hàng / đối tác (loai: khach-hang)
│   ├── competitors/       # Đối thủ cạnh tranh (loai: doi-thu)
│   ├── khai-niem/         # Trang khái niệm
│   ├── tom-tat-nguon/     # Tóm tắt từng file nguồn
│   └── so-sanh/           # Bảng/trang so sánh
└── production/            # Sản phẩm đầu ra theo lệnh (blog, post, kịch bản, PDF...)
    └── dmo/               # Hệ thống nếp ngày (DMO) — xem mục 10
```

---

## 10. Hệ thống DMO (nếp ngày) & Lịch Google

Nếp ngày của anh Đức theo mô hình Phạm Thành Long: mỗi ngày 1 file việc, tick khi xong,
báo cáo 3 khung giờ, tối tự tạo DMO hôm sau. Dựa trên khái niệm [[nep-ngay-dmo]].

**Vị trí & công cụ:**
- `production/dmo/_MAU-DMO.md` — template 6 việc (I. Rèn thân · II. Học · III. Làm ra tiền ·
  IV. Kiểm đếm + bảng 6 lọ 55/10/10/10/10/5 · V. Phalon · VI. Đánh giá).
- `production/dmo/DMO-YYYY-MM-DD.md` — file mỗi ngày (nguồn chân lý của ngày đó).
- `tools/dmo.py` — `tao` (sinh DMO, chuyển việc phát sinh tồn) · `bao-cao` (đếm %, việc còn tồn) ·
  `lich` (xuất JSON 6 việc + khung giờ). Chi tiết: `production/dmo/HUONG-DAN-DUNG.md`.

**Lịch Google (qua Composio, toolkit `googlecalendar`):**
- Tài khoản: **ducngovan.hn@gmail.com**, alias `hn` (mặc định). Kết nối đã Active.
- Tool deferred — nạp schema trước bằng `ToolSearch` rồi gọi qua `COMPOSIO_MULTI_EXECUTE_TOOL`
  với `account: "googlecalendar_tarin-cupper"` (hoặc alias `hn` nếu nhận):
  `GOOGLECALENDAR_CREATE_EVENT` (start/end ISO + `timezone: "Asia/Ho_Chi_Minh"`, `create_meeting_room: false`),
  `GOOGLECALENDAR_PATCH_EVENT` (đổi tên/màu khi việc xong), `GOOGLECALENDAR_FIND_EVENT`.
- Thao tác ghi lịch là side-effect → theo thói quen chỉ đổ việc/đánh dấu khi anh Đức đã đồng ý cách làm.

**Đồng bộ Git (repo gọn — chỉ phần chữ):**
- GitHub **private**, chỉ chứa `.md`/`.py`/`.json`. `.gitignore` loại `raw/` + `*.xlsx` + `*.pdf`
  (giữ trên máy, backup ổ cứng). Branch `backup-lich-su-cu-155mb` (local) giữ lịch sử cũ nặng.
- Điện thoại + báo cáo cloud đọc DMO qua repo này (máy không cần bật).
