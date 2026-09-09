# 📈 Báo cáo tuần "Bộ Não Thứ Hai" — tự chạy mỗi Chủ Nhật

> Mỗi Chủ Nhật tối, tự tổng hợp số liệu THẬT của tuần vừa qua, so với tuần trước,
> viết đánh giá, lưu vào `production/bao-cao-tuan/` và (tuỳ chọn) ghi tóm tắt lên Lịch Google.
> Dựa trên công cụ `tools/bao_cao_tuan.py` (chỉ đếm số chắc chắn, trích nguyên văn dòng tiền —
> KHÔNG tự cộng, KHÔNG suy đoán).

---

## 1. Công cụ nền — `tools/bao_cao_tuan.py`

Tự lấy số liệu 2 tuần liền kề từ: `git log` · `wiki/log.md` · `production/dmo/` · frontmatter `ngay_tao` của các trang wiki.

```bash
python tools/bao_cao_tuan.py                 # bảng số liệu cho người đọc
python tools/bao_cao_tuan.py --json          # JSON cho LLM viết đánh giá
python tools/bao_cao_tuan.py --den 2026-09-13   # chốt tuần tới ngày cụ thể
```

**Cách chia tuần:** `--den` = ngày cuối tuần (mặc định hôm nay).
Tuần này = `[den-6 .. den]`, tuần trước = `[den-13 .. den-7]`.
➡️ Chạy đúng **Chủ Nhật** thì `den` = Chủ Nhật → tuần = **Thứ Hai → Chủ Nhật** trọn vẹn.

**Chỉ số công cụ trả về:** commit git · mục nhật ký (ingest/query/lint/update) · trang wiki mới ·
số ngày có DMO · % DMO trung bình · danh sách commit + mục log + các dòng kiểm đếm tiền của từng ngày.

> ⚠️ Nên chạy **sau khi đã chốt DMO Chủ Nhật (sau 22:00)**. Nếu chạy giữa ngày, DMO hôm đó
> chưa tick xong sẽ kéo tụt "% DMO trung bình".

---

## 2. Lịch chạy

| Khung giờ VN | Cron (UTC) | Việc |
|---|---|---|
| **Chủ Nhật 22:30** | `30 15 * * 0` | Tổng hợp tuần + viết đánh giá + lưu file (+ Lịch Google) |

---

## 3. Prompt routine (dán vào ô nội dung Routine / `/schedule`)

```
Bối cảnh: đây là vault "bộ não thứ hai" của anh Đức (repo Ducngovan-hn/DucLan). Toàn bộ tiếng Việt.

1) Pull repo mới nhất.
2) Chạy: python tools/bao_cao_tuan.py --json   → lấy số liệu THẬT 2 tuần (tuần này vs tuần trước).
3) Viết một BÁO CÁO TUẦN ngắn gọn (~500-700 từ) gồm:
   - Bảng so sánh số liệu 2 tuần (commit, mục nhật ký, trang wiki mới, số ngày DMO, % DMO TB).
   - Nhận định: tuần qua bộ não tiến hoá thế nào so với tuần trước? Nhanh hơn hay chậm lại?
     Nạp thêm loại tri thức gì? Ra sản phẩm gì?
   - Cột "III. Làm ra tiền" trong DMO: đọc các dòng kiểm đếm tiền, nêu tuần này có mấy ngày
     có tiền về / mấy ngày "0", mấy khách trả hàng. KHÔNG tự cộng tổng nếu số liệu không rõ —
     chỉ nêu lại nguyên văn con số đã ghi.
   - 2-3 điểm cần lưu ý / đề xuất cho tuần tới.
   Nguyên tắc: mọi con số phải lấy từ output công cụ, không bịa. Nếu thiếu dữ liệu thì nói rõ "chưa có".
4) Lưu báo cáo vào: production/bao-cao-tuan/bao-cao-tuan-<Chủ Nhật YYYY-MM-DD>.md
5) (Tuỳ chọn) Ghi 5-6 dòng tóm tắt vào mô tả event Lịch Google tên "📈 Báo cáo tuần bộ não"
   lúc Chủ Nhật 22:30 (account googlecalendar hn, timezone Asia/Ho_Chi_Minh, create_meeting_room=false).
6) git add -A && git commit -m "Bao cao tuan <ngày>" && git push
```

---

## 4. Chạy tay bất cứ lúc nào

Muốn xem ngay không cần chờ Chủ Nhật, chỉ cần nói với Claude:
**"làm báo cáo tuần"** — Claude chạy `python tools/bao_cao_tuan.py`, đọc số, viết đánh giá,
lưu vào `production/bao-cao-tuan/`.

---

## 5. Dự phòng (nếu routine cloud chưa gọi được Composio Lịch)

Bỏ bước 5 (ghi Lịch). Báo cáo chữ vẫn chạy và lưu file bình thường.
Phần ghi Lịch làm tại máy qua phiên Claude Code desktop (Composio đã kết nối sẵn).
