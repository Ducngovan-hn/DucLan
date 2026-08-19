# ⏰ Routine báo cáo DMO 3 khung giờ (7h · 12h · 22h)

> Cách dựng báo cáo tự động chạy trên **cloud** (máy không cần bật), đọc DMO từ GitHub,
> ghi báo cáo lên **Lịch Google**. Tạo tại **claude.ai/code → Routines** (hoặc lệnh `/schedule`).

---

## 0. Chuẩn bị (làm 1 lần)

Routine chạy trên môi trường cloud nên cần 2 kết nối trong môi trường đó:
1. **Repo GitHub** `Ducngovan-hn/DucLan` (private) — để routine `git clone/pull` đọc file DMO.
2. **Composio Lịch Google** (`googlecalendar`, account `hn`) — để ghi event báo cáo.

> ⚠️ Điểm cần thử thực tế: nếu môi trường routine cloud **chưa gọi được Composio**, thì phần
> ghi Lịch sẽ báo lỗi. Khi đó tách đôi: báo cáo chữ vẫn chạy cloud, phần ghi Lịch chuyển về
> chạy trên máy (Task Scheduler + `tools/dmo.py`). Xem mục 4.

---

## 1. Lịch cron (giờ Việt Nam UTC+7)

| Khung giờ VN | Cron (nếu nhập theo UTC) | Việc |
|---|---|---|
| **07:00** | `0 0 * * *` | Báo cáo sáng — nhắc 6 việc, "ăn con ếch trước" |
| **12:00** | `0 5 * * *` | Báo cáo giữa ngày — tính %, việc chưa xong |
| **22:00** | `0 15 * * *` | Tổng kết ngày + tạo DMO mai + đổ event Lịch mai |

> Nếu giao diện Routines cho chọn **timezone Asia/Ho_Chi_Minh** thì nhập thẳng 07:00/12:00/22:00.

---

## 2. Prompt cho từng routine (dán vào ô nội dung)

### 🌅 Routine 07:00 — Báo cáo sáng
```
Đọc file production/dmo/DMO-<hôm nay>.md trong repo Ducngovan-hn/DucLan (pull mới nhất).
Nếu chưa có file cho hôm nay, tạo bằng: python tools/dmo.py tao
Tóm tắt 6 việc hôm nay + khung giờ. Nhắc anh Đức "ăn con ếch trước" (việc khó làm sớm).
Ghi tóm tắt này vào mô tả event Lịch Google tên "📊 Báo cáo DMO sáng" lúc 07:00 hôm nay
(account googlecalendar hn, timezone Asia/Ho_Chi_Minh). Toàn bộ tiếng Việt.
```

### ☀️ Routine 12:00 — Báo cáo giữa ngày
```
Pull repo Ducngovan-hn/DucLan. Chạy: python tools/dmo.py bao-cao
Lấy dòng "TIẾN ĐỘ: n/N việc · P%" và danh sách việc còn tồn.
Ghi vào mô tả event Lịch Google "📊 Báo cáo DMO giữa ngày" lúc 12:00 hôm nay
(account hn, Asia/Ho_Chi_Minh). Nêu rõ việc nào chưa xong / quá giờ. Tiếng Việt.
```

### 🌙 Routine 22:00 — Tổng kết + tạo DMO mai
```
Pull repo Ducngovan-hn/DucLan.
1) Chạy: python tools/dmo.py bao-cao  → lấy % cuối ngày + việc còn tồn.
2) Chạy: python tools/dmo.py tao --ngay <ngày mai>  → tạo DMO hôm sau (tự chuyển việc tồn).
3) Chạy: python tools/dmo.py lich --ngay <ngày mai>  → lấy JSON 6 việc + khung giờ,
   tạo các event tương ứng trên Lịch Google (account hn, Asia/Ho_Chi_Minh, create_meeting_room=false).
4) Ghi tổng kết % vào event "📊 Tổng kết DMO" lúc 22:00 hôm nay.
5) git add -A && git commit -m "DMO <ngày mai> + tong ket <hôm nay>" && git push
Toàn bộ tiếng Việt.
```

---

## 3. Cách anh Đức dùng hằng ngày (kết hợp Lịch + file)
- Trong ngày: mở **file DMO** bằng app Claude Code / Obsidian → tick `[x]`, điền số liệu → push.
- Xem báo cáo: mở các event **📊 Báo cáo DMO** trên Lịch (đọc %, việc tồn) — event này **sửa được**.
- Việc ngày mai: 22h routine tự đổ lên Lịch, sáng mở ra là có sẵn.

---

## 4. Phương án dự phòng (nếu cloud không gọi được Composio Lịch)
Chạy báo cáo bằng Windows Task Scheduler ngay trên máy (máy phải bật lúc đó):
- Tạo 3 task chạy `python C:\Users\admin\DucLan\tools\dmo.py bao-cao` vào 7h/12h/22h.
- Phần đổ event Lịch: chạy tại máy qua Composio (đã kết nối sẵn ở phiên Claude Code desktop).
```
