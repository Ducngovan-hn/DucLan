---
tieu_de: KỊCH BẢN DỰNG — Bo cổ áo polo là gì? (Ngày 1/28)
loai: tong-hop
ngay_tao: 2026-09-02
ngay_cap_nhat: 2026-09-02
nguon:
  - production/content/kich-ban/2026-08-20-bo-co-polo-la-gi.md
  - footage-content/2026-content-xuong-bo/ (đã ingest, 30 ngày footage)
tags: [content, kich-ban-dung, ngay-01]
---

# KỊCH BẢN DỰNG — Bo cổ áo polo là gì? (Ngày 1/28 · nhóm KT)

> Dựng từ **footage thật đã ingest** (kho `2026-content-xuong-bo`) thay cho luồng
> `/offload` theo ngày. Kiểm kê lấy từ `index/*.json` + `map.json` (file thật), không từ trí nhớ.
> Video short dọc 9:16, giọng AI, phụ đề cháy chữ. Anh Đức **duyệt rồi tự đăng**.

## 1. Kiểm kê footage thật (so với shot list Mốc 1)

| Shot | Yêu cầu (Mốc 1) | Footage thật chọn | Có/Thiếu |
|---|---|---|---|
| 1 | Tay cầm bo cổ đưa lên (hook) | `19/08 IMG_6231.JPG` (bo cam cầm tay, ánh sáng ngoài trời) | ✅ Có (ảnh) |
| 2 | Bo cổ cạnh áo polo | `04/08 IMG_5966.JPG` (bo cổ polo cam thành phẩm) | ⚠️ Thay: dùng bo cổ thành phẩm thật (không có cảnh bo+áo cùng khung; ảnh áo polo IMG_6071 là PNG tải về → bỏ, tránh bản quyền) |
| 3 | Cận macro bề mặt bo (sợi, gân) | `08/08 IMG_6022.JPG` + `IMG_6021.JPG` (mặt dệt bo navy) | ✅ Có (ảnh) |
| 4 | **Máy dệt đang ra sợi bo (cú đắt)** | `22/08 IMG_6280.MOV` (dàn máy chạy) + `IMG_6287.MOV` (ống sợi lên máy) | ✅✅ Có VIDEO THẬT |
| 5 | Kéo giãn bo rồi thả (bật lại) | `08/08 IMG_6023.JPG` (bo navy kéo giãn) | ⚠️ Chỉ có ẢNH tĩnh — **thiếu video kéo-thả động** |
| 6 | Trải 4–5 kiểu bo cổ | `04/08 IMG_5951.JPG` (bảng màu) + `25/08 IMG_6339.JPG` (sàn đủ màu/kiểu) | ✅ Có (ảnh) |
| 7 | Anh Đức talking-head / CTA | *(không có footage anh Đức nói)* | ❌ **THIẾU** — thay bằng ảnh thành phẩm + chữ CTA + giọng AI |

**Cú đắt nhất (Shot 4 — máy dệt): CÓ**, 14 clip .MOV ngày 22/08 → video giữ được sức "hàng tự sản xuất".
**Trượt:** Shot 5 không có video kéo giãn động; Shot 7 không có mặt/giọng anh Đức. Ghi ở §6.

## 2. Tiếng & giọng
- **Giọng: AI** (bài Kiến thức) — edge-tts `vi-VN-NamMinhNeural` (nam, chắc, hợp thương hiệu).
  Câu CTA cuối lẽ ra để **giọng anh Đức** (theo Mốc 1) nhưng chưa có bản thu → tạm dùng AI, ghi tồn.
- **Tiếng hiện trường đắt:** giữ **tiếng máy dệt thật** từ IMG_6280/6287 ở Shot 4, hạ nhỏ dưới giọng.
- **Nhạc nền:** chưa có file nhạc không bản quyền trong repo → **để trống**, ghi tồn (không bịa nhạc bản quyền).

## 3. Cấu trúc chốt theo giây (khớp giọng TTS thật — cập nhật sau khi đo)
| Đoạn | Câu thoại | Shot/hình | Giây (dự kiến) |
|---|---|---|---|
| Hook | "Chiếc polo 300 nghìn hay 3 triệu — khác nhau nằm ở đúng cái vòng nhỏ này." | Shot 1 | 0–4s |
| Định nghĩa | "Nó gọi là bo cổ. Là phần dệt co giãn viền quanh cổ áo polo." | Shot 2 | 4–9s |
| Dệt riêng | "Không phải cắt ra từ vải áo — mà dệt riêng, để ôm, để giữ form, để bật lại sau mỗi lần bạn kéo qua đầu." | Shot 3 | 9–17s |
| Từ sợi | "Ở xưởng, mỗi chiếc bo đi ra từ sợi, dệt thành cổ và tay đi cùng một bộ." | Shot 4 (máy dệt) | 17–24s |
| Bo tốt | "Bo tốt thì kéo giãn rồi bật lại ngay, không dão, không xoắn." | Shot 5 | 24–29s |
| Nhiều kiểu | "Và có nhiều kiểu — kẻ trơn, gân, lacoste — chọn theo chiếc áo bạn may." | Shot 6 | 29–35s |
| CTA | "Bạn đang cần bo cho mẫu áo nào? Nhắn Đức Lan để mình tư vấn đúng loại." | Shot 7 | 35–42s |

## 4. Phụ đề
- Cháy chữ (burn-in) toàn bộ, .ass, font **Be Vietnam Pro** đậm (fallback Arial Bold), viền đen.
- Nhấn từ khoá màu **cam #F97316**: "bo cổ", "dệt riêng", "bật lại", "từ sợi".
- Mỗi câu 1 dòng, khớp mốc giọng.

## 5. Ba gói đăng (tinh chỉnh từ Mốc 1 theo footage thật)

### YouTube (Short)
- **Tiêu đề:** Bo cổ áo polo là gì? Vì sao cái vòng nhỏ này quyết định giá trị chiếc áo | Dệt Bo Đức Lan
- **Mô tả:** Bo cổ là phần dệt co giãn quanh cổ áo polo — dệt riêng, không cắt từ vải áo. Video quay tại xưởng: từ sợi lên máy dệt đến chiếc bo cổ hoàn chỉnh. Xưởng Dệt Bo Đức Lan nhận dệt bo cổ, bo tay theo yêu cầu (sỉ & lẻ). Liên hệ: [ĐIỀN — SĐT/Zalo].
- **Tags:** bo cổ, bo cổ áo polo, dệt bo, bo polo, xưởng bo, đức lan, phụ liệu may, áo polo, rib cổ áo, bo cổ tay, ngành may, dệt bo theo yêu cầu

### TikTok
- **Caption:** Cái vòng nhỏ này quyết định chiếc polo của bạn 👕 Bo cổ là gì? Xem xưởng dệt trong 40 giây.
- **Hashtag:** #detbo #boduclan #bocoao #aopolo #nganhmay *(kiểm 1–2 hashtag xu hướng lúc đăng)*
- **CTA ghim:** "Cần tư vấn bo cho mẫu áo của bạn → nhắn Zalo ở bio nhé."

### Facebook
- **Caption:** Bạn cầm chiếc áo polo lên — thứ đầu tiên tay chạm vào là **cổ áo**. Đó là **bo cổ**: phần dệt co giãn riêng, quyết định độ ôm, form dáng và cảm giác cao cấp của chiếc áo. Ở Đức Lan, mỗi chiếc bo đi ra từ sợi, dệt thành cổ và tay cùng một bộ, kéo giãn là bật lại ngay. 👉 Bạn đang cần bo cho mẫu áo nào? Nhắn mình để tư vấn đúng loại. 📞 [ĐIỀN SĐT] · Zalo: [ĐIỀN]
- **Hashtag:** #DetBoDucLan #bocoao #aopolo #nganhmay #phulieumay

## 6. Việc tồn
- **Quay bù:** (a) video **kéo giãn bo rồi thả** (Shot 5) — cảnh động, ảnh tĩnh chưa đủ lực;
  (b) **anh Đức talking-head đọc CTA** (Shot 7) — tăng độ tin & gần gũi.
- **Dữ kiện cần anh Đức xác minh/điền:** SĐT · Zalo · Facebook · TikTok handle (đang `[ĐIỀN]` — điền vào SOP mục "Thông tin liên hệ chuẩn" để tự chèn).
- **Nhạc nền:** cần 1 file nhạc nền tươi, không bản quyền (chưa có trong repo).
- **Short phụ cắt được:** riêng cụm máy dệt 22/08 (14 clip) đủ dựng 1 short "hậu trường dệt bo" độc lập.
