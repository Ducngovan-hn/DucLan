---
name: dmo
description: Vận hành nếp ngày (DMO) của anh Đức — tạo DMO mỗi ngày, tick việc đã xong, thêm việc phát sinh, chốt kiểm đếm cuối ngày (tiền · 6 lọ · chi · khách trả hàng), tính % tiến độ, tạo DMO hôm sau và chuyển việc tồn, cập nhật ✅ lên Lịch Google. Dùng skill này BẤT CỨ KHI NÀO anh Đức nói tới việc trong ngày theo nếp DMO — "hôm nay có việc gì", "tick việc X", "xong việc Y", "thêm việc hôm nay", "thêm việc phát sinh", "chốt kiểm đếm", "tiền thực nhận hôm nay", "chia 6 lọ", "tạo DMO ngày mai", "báo cáo tiến độ", "còn việc gì chưa xong", "đánh giá cuối ngày", "3 lời biết ơn". KHÔNG dùng cho tổng hợp doanh thu/chi phí xưởng (skill so-sach / chi-phi-nvl) hay phân tích chạy bộ (skill chay-bo).
---

# Nếp ngày DMO — cẩm nang vận hành

Nếp ngày của anh Đức theo mô hình Phạm Thành Long. Dựa trên [[nep-ngay-dmo]] và
mô hình 6 lọ tiền. Chi tiết nền: `CLAUDE.md` mục 10, `production/dmo/HUONG-DAN-DUNG.md`.

## 0. NGUYÊN TẮC BẮT BUỘC (đọc trước mọi thao tác)

1. **Luôn lấy ĐÚNG NGÀY theo giờ Việt Nam TRƯỚC** — không tin trí nhớ hay currentDate.
   Gọi Composio `GOOGLECALENDAR_GET_CURRENT_DATE_TIME` timezone `Asia/Ho_Chi_Minh`
   (nạp schema bằng ToolSearch nếu deferred). Ngày này quyết định file DMO nào, event Lịch nào.
2. **Con số chính xác, không suy đoán** ([[con-so-chinh-xac-khong-suy-doan]]): tiền, số khách,
   km/nhịp… phải tra **NGUỒN THẬT (mục 5)** trước — tự lấy được thì lấy, KHÔNG hỏi lại; chỉ khi
   nguồn thiếu/không rõ mới HỎI anh Đức. Tuyệt đối không tự điền số đoán.
3. **Tiếng Việt toàn bộ**, gọi người dùng là **anh Đức**.
4. **% tiến độ** luôn tính bằng `python tools/dmo.py bao-cao --ngay <ngày>`, không đếm tay/đoán.

## 1. Cấu trúc

- File mỗi ngày: `production/dmo/DMO-YYYY-MM-DD.md` (nguồn chân lý của ngày đó).
- Template: `production/dmo/_MAU-DMO.md`. Công cụ: `tools/dmo.py`.
- Ký hiệu tick: `[ ] ⬜` chưa làm → `[x] 💚` đã xong.
- **6 việc DMO** (giữ đúng thứ tự này): 1 Rèn thân (chạy bộ) · 2 Học 1 điều mới
  (tiếng Trung · LTTTL · đọc/nghe sách · học tạo video) · 3 Làm việc tạo ra tiền
  (xưởng dệt · content+video) · 4 Kiểm đếm cuối ngày · 5 Phalon · 6 Đánh giá cuối ngày.
- **6 lọ** (chia theo tiền thực nhận, tỷ lệ 55/10/10/10/10/5): Đầu tư · Mua sắm lâu dài ·
  Học tập · Tiêu dùng · Ăn chơi · Cho đi.

## 2. Công cụ dmo.py

```bash
python tools/dmo.py tao --ngay YYYY-MM-DD      # tạo DMO ngày đó, tự chuyển việc phát sinh tồn
python tools/dmo.py bao-cao --ngay YYYY-MM-DD  # in "n/N việc · P%" + việc còn tồn
python tools/dmo.py lich --ngay YYYY-MM-DD      # JSON 6 việc + khung giờ
```

## 3. Các thao tác thường gặp

### Tick việc đã xong
Sửa dòng trong file DMO đúng ngày: `[ ] ⬜` → `[x] 💚`, ghi số liệu anh Đức cho vào chỗ `___`.
Nếu là **cả một việc lớn (1–6)** đã xong → đánh dấu ✅ lên thẻ Lịch (mục 4).

### Thêm việc phát sinh hôm nay
Thêm dòng `- [ ] ⬜ <việc>` vào mục tương ứng trong file DMO (thường mục III — Làm việc tạo ra tiền,
dưới nhãn `**Việc phát sinh hôm nay:**`). Rồi đổ vào **mô tả instance hôm nay** của thẻ Lịch
liên quan (mục 4) — KHÔNG sửa event gốc (tránh lặp sang ngày sau).

### Chốt kiểm đếm cuối ngày (mục IV)
Lấy số từ **nguồn thật (mục 5)**, KHÔNG hỏi nếu tự lấy được:
- (1) tiền thực nhận · (3) chia 6 lọ → Excel 6 lọ; (2) đã chi → **footage my-life** (nhật ký/event/ảnh hoá đơn).
- (4) số khách trả hàng → Zalo nhóm "Trả hàng" (không có tin trong ngày = 0).
Chia 6 lọ tính 55/10/10/10/10/5 (tiền = 0 thì mọi lọ = 0). Nguồn thiếu/không rõ mới hỏi anh Đức.
Điền vào bảng mục IV, tick các dòng, rồi ✅ thẻ "Kiểm đếm" trên Lịch.

### Tick việc 1 — chạy bộ
Số km · thời gian lấy từ **footage my-life (mục 5)**, không hỏi nếu tự lấy được.

### Quy tắc tick MẶC ĐỊNH (chỉ thị anh Đức)
- **Chạy bộ:** không thấy ảnh chạy trong footage my-life ngày đó → ghi thẳng **"không chạy"**,
  KHÔNG hỏi lại (anh Đức sẽ tự sửa nếu thực ra có chạy).
- **Hôm nào CÓ chạy bộ → tự tick luôn "Đọc / nghe sách nói"** (anh Đức nghe audio khi chạy).
- **Phalon (việc 5) → mặc định tick mỗi ngày** (anh Đức luôn làm trước khi ngủ).
- **Quay video** (trong việc 3 "Viết content + quay video") → kiểm **footage xưởng** ngày đó;
  có clip quay → tick.

### Báo cáo tiến độ
Chạy `dmo.py bao-cao --ngay <ngày> --cap-nhat` — **luôn kèm `--cap-nhat`** để dòng `**TIẾN ĐỘ: n/N · P%**`
ở cuối file DMO tự nhảy số (không có cờ này thì chỉ in màn hình, dòng trong file vẫn `0/? · 0%`).
Trình bày: đã xong (liệt kê), TIẾN ĐỘ n/N · P%, còn lại.

### Tạo DMO ngày mai + đánh giá cuối ngày (mục VI)
`dmo.py tao --ngay <mai>` (tự bê việc phát sinh tồn). Hỏi anh Đức muốn đổ việc tồn lên thẻ Lịch mai
không. Ghi 3 lời biết ơn + bài học anh Đức đọc. Tick các dòng mục VI.

## 4. Lịch Google (Composio, toolkit `googlecalendar`, account `hn`)

6 việc là **event lặp hằng ngày** (RRULE FREQ=DAILY). Muốn sửa/đánh dấu **một ngày cụ thể** thì
tác động lên **instance** ngày đó, KHÔNG lên event gốc.

- Lấy instance: `GOOGLECALENDAR_FIND_EVENT` (timeMin/timeMax bao ngày đó, `single_events: true`) →
  lấy `id` trả về (đã có hậu tố `_YYYYMMDDTHHMMSSZ` theo giờ UTC).
- Đánh dấu xong: `GOOGLECALENDAR_PATCH_EVENT` với `event_id` = id instance, đổi `summary` thêm `✅`
  và ghi số vào `description`.
- Thêm việc phát sinh: PATCH `description` của instance thẻ "💰 Làm việc tạo ra tiền" ngày đó.
- Master id 6 việc hiện tại (đổi khi tạo lại — ưu tiên FIND_EVENT): chạy bộ `ce77pu32die077a57co1vfbet0`,
  học `rk3huoi3vrkvb5u294ha5bq93s`, làm tiền `b8ik3m2e8vdjor3g0dirllh2h4`,
  kiểm đếm `299396d999mf614bv8de791am0`, phalon `7q5b643e59c3b0h59gpte9bvgs`,
  đánh giá `gpbeddkdft2f9e4n10riodiq74`.
- Quy đổi giờ instance (VN→UTC, trừ 7h): 08:00→`T010000Z`, 22:00→`T150000Z`, 23:00→`T160000Z`,
  05:30→ngày hôm trước `T223000Z`. An toàn nhất: đọc id thật từ FIND_EVENT.

## 5. Nguồn dữ liệu — TỰ ĐỘNG LẤY, KHÔNG HỎI

**Chỉ thị thường trực của anh Đức (01/09/2026):** mỗi khi báo cáo / chốt kiểm đếm, MẶC ĐỊNH tự lấy
3 nguồn dưới đây rồi điền thẳng vào báo cáo — KHÔNG hỏi anh Đức trước. Chỉ báo lại khi nguồn
không lấy được (Zalo chưa mở, token Garmin lỗi…) hoặc số bất thường cần anh xác nhận.

- **Tiền thực nhận · chia 6 lọ** → đọc file Excel **`production/Mo-hinh-6-cai-lo.xlsx`**
  (nhật ký thu · bảng số dư 6 lọ). Đọc bằng skill `xlsx` hoặc openpyxl; lọc theo đúng ngày.
- **Đã chi trong ngày** → đọc **FOOTAGE my-life** (`C:\Users\admin\my-life`): file nhật ký ngày +
  event md + ảnh hoá đơn/đơn hàng của ngày đó. Ghi rõ khoản chi (số tiền từ ảnh, không đoán) và trừ vào lọ nào.
- **Số khách trả hàng** → đọc nhóm **Zalo "Trả hàng"** (gom chữ, xem [[doc-zalo-qua-zalo-pc-gom-chu]]):
  nếu trong ngày KHÔNG có tin nhắn trả hàng → **0 khách** (không trả cho ai). Nếu có → ghi **số lượng + tên khách**.
- **Chạy bộ** → lấy từ **FOOTAGE my-life trong máy** (`C:\Users\admin\my-life`) — xem ảnh/clip buổi chạy
  hôm đó, KHÔNG vào Garmin/Strava (cho nhanh).

Sau khi tự lấy, luôn báo lại số cho anh Đức khi ghi vào DMO (minh bạch nguồn).

**⚠️ 2 BẪY SÓT SỐ (đã mắc 03/09 — luôn phòng):**
- **Excel cột ngày lưu nhầm:** anh Đức gõ "3/9" nhưng Excel lưu thành `2026-03-09` (đảo dd↔mm).
  → KHÔNG chỉ match chuỗi "3/9"; phải **đọc hết các dòng CUỐI bảng** (mới nhập) và soi cả ngày kiểu
  `YYYY-03-09`, `YYYY-09-03`. Rà cột ngày kỹ trước khi kết luận "không có giao dịch".
- **Zalo script bỏ nhãn "Hôm nay":** `zalo_dump.mjs` báo "mốc tới 01/09" nhưng tin ngày hiện tại nằm
  dưới nhãn **"Hôm nay"** ở CUỐI file → luôn `tail` đọc phần cuối file dump, đừng tin mốc script tự báo.

## 6. Đồng bộ Git — TỰ ĐỘNG sau mỗi lần chốt DMO (anh Đức không phải nhắc)

Chỉ thị anh Đức (03/09): **tạo/chốt DMO xong là tự đồng bộ, không chờ nhắc.** Quy trình:
1. `git add -A && git commit -m "..."` — chạy được (local, không bị chặn) → LUÔN tự làm.
2. `git push` — bị auto-classifier chặn với Claude → **tự đưa sẵn khối lệnh `git push` (tag bash, có nút Run)
   cho anh Đức bấm ngay** ở cuối phản hồi, KHÔNG chờ anh yêu cầu.
3. Nếu anh Đức đã thêm rule `Bash(git push:*)` vào settings thì thử push thẳng trước; chặn thì mới đưa nút.
Xem [[he-thong-dmo-va-git]].
