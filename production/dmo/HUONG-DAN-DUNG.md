# 🧭 Hướng dẫn dùng hệ thống DMO

> Nếp ngày (DMO) của anh Đức: mỗi ngày 1 file việc, tick khi xong, báo cáo 3 khung giờ,
> tối tự tạo DMO hôm sau. File DMO là file chữ trong `production/dmo/DMO-YYYY-MM-DD.md`.

---

## 1. Công cụ `tools/dmo.py` — 3 lệnh

```bash
# Tạo DMO cho hôm nay (tự bê việc phát sinh chưa xong từ hôm trước sang)
python tools/dmo.py tao

# Tạo cho một ngày cụ thể
python tools/dmo.py tao --ngay 2026-08-20

# Xem tiến độ: n/N việc · %  + liệt kê việc còn tồn
python tools/dmo.py bao-cao

# Ghi luôn dòng TIẾN ĐỘ vào file
python tools/dmo.py bao-cao --cap-nhat

# Xuất JSON 6 việc + khung giờ (để đẩy lên Google Calendar)
python tools/dmo.py lich
```

**Cách tick việc:** mở file DMO trong ngày, đổi `[ ]` → `[x]` ở dòng việc đã xong,
rồi điền số liệu vào chỗ `_______`. Cuối ngày chạy `bao-cao` để ra %.

**Việc phát sinh:** cứ thêm dòng `- [ ] ⬜ <tên việc>` vào file. Nếu tối chưa xong,
lệnh `tao` hôm sau sẽ tự chuyển sang (việc cố định lặp lại thì KHÔNG bị nhân đôi).

---

## 2. Quy trình một ngày

| Giờ | Việc |
|---|---|
| Sáng | Mở DMO hôm nay (đã được tạo sẵn từ tối qua) — "ăn con ếch trước" |
| Trong ngày | Xong việc nào tick việc đó `[x]` |
| 22:00 | Kiểm đếm: tiền thực nhận → chia 6 lọ → đã chi → số khách trả hàng |
| 22:00 | Đánh giá: `dmo.py bao-cao` xem %, `dmo.py tao` tạo DMO mai, viết 3 lời biết ơn |
| 23:00 | Phalon — suy ngẫm 30 phút |

---

## 3. Dùng trên điện thoại + máy tính (đồng bộ qua GitHub)

Vault đồng bộ qua **GitHub riêng tư** (chỉ phần chữ — nhẹ, pull nhanh).
File Excel sổ sống + nguồn `raw/` **giữ trên máy tính**, không lên GitHub.

### Trên máy tính (chính)
Làm trực tiếp trong `C:\Users\admin\DucLan`. Xong việc thì đẩy lên GitHub:
```bash
git add -A && git commit -m "cap nhat DMO" && git push
```

### Trên điện thoại — 2 cách

**a) App Claude Code (cloud + Git)** — khi đi ra ngoài, máy tắt:
1. Mở dự án từ repo GitHub `DucLan`.
2. `git pull` để lấy DMO mới nhất → xem, tick việc.
3. `git commit` + `git push` khi xong.

**b) Remote Control** — khi cần chạy `tools/dmo.py` hoặc mở Excel sổ sống:
- Điện thoại điều khiển thẳng máy Windows ở nhà (máy phải bật + nối mạng).
- Làm y như đang ngồi trước máy.

> ⚠️ Quy tắc tránh xung đột: **luôn `git pull` trước khi sửa**, `git push` ngay sau khi sửa xong.
> Đừng sửa cùng lúc ở cả 2 nơi mà chưa đồng bộ.

---

## 4. Báo cáo tự động 7h / 12h / 22h

Chạy trên **cloud** (máy không cần bật), đọc DMO từ GitHub:
- **07:00** — nhắc 6 việc trong ngày, "ăn con ếch trước".
- **12:00** — báo tiến độ giữa ngày (%), việc chưa xong.
- **22:00** — tổng kết ngày, tạo sẵn DMO hôm sau.

*(Chi tiết cấu hình routine cloud ghi bổ sung sau khi dựng xong.)*

---

## 5. Liên quan
- Khái niệm gốc: [[nep-ngay-dmo]] · [[sau-cai-lo]]
- Mô hình 6 lọ tiền chi tiết: `production/Mo-hinh-6-cai-lo.md`
