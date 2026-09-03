---
description: Dựng video dọc từ footage thật đã cất + xuất 3 gói đăng (YouTube/TikTok/Facebook) cho anh Đức duyệt & tự đăng. Chạy SAU khi /offload verify xong.
argument-hint: "[dd/mm hoặc YYYY-MM-DD — bỏ trống = hôm nay]"
---

# /kich-ban-dung $ARGUMENTS

Dựng **video dọc** cho một ngày content xưởng bo — chạy **SAU khi `/offload` báo `✅ VERIFY ĐỦ`**.
Đầu ra để anh Đức **duyệt rồi tự đăng cả 3 kênh** (không tự đăng).

## Cách chạy

1. **Xác định ngày.** Trống → hôm nay (`date +%F`).
2. **Kiểm data an toàn.** Đọc `C:\Users\admin\footage-content\<ngày>\_offload-log.json`.
   - Không có file, hoặc `loi` không rỗng → **DỪNG, báo anh Đức chạy `/offload` cho xong**. Không dựng.
3. **Đọc theo thứ tự:**
   - `production/content/kich-ban/<ngày>-*.md` — kịch bản quay Mốc 1 (shot list dự kiến, hook, giọng, 3 caption nháp, §9 định hướng dựng).
   - `_offload-log.json` — **số clip/ảnh thật, video/ảnh từng loại** (kiểm kê từ log, không từ trí nhớ).
   - `production/content/guideline-social.md` — độ dài, phụ đề, khung caption 3 nền tảng, hashtag, CTA.
4. **Viết kịch bản dựng** vào `production/content/dung/<ngày>-<slug>.md` — đủ **6 phần** dưới.
5. **Dựng video** (xem phần "Kỹ thuật dựng").
6. **Ghi log** `wiki/log.md`: `## [YYYY-MM-DD] update | kich-ban-dung | <chủ đề> · <số clip> · giọng <loại>`. Báo lại: đường dẫn video + 3 gói đăng + cảnh nào thiếu.

## Đủ 6 phần (trong file dung/)

1. **Kiểm kê footage thật** — số clip · dung lượng · so với shot list Mốc 1: **cảnh nào có, cú đắt nhất có quay được không, cảnh nào thiếu**. Ghi thẳng, không che.
2. **Tiếng & giọng** — chọn loại giọng cho video này: **AI** (bài kiến thức) / **anh Đức** (chia sẻ, case study) / **để tiếng máy dệt** (hậu trường). Có tiếng hiện trường đắt nào (máy dệt) không.
3. **Cấu trúc chốt theo giây** — các đoạn với **giây thật**: Hook (0–3s) → thân → CTA. Khớp footage đang có.
4. **Phụ đề** — bản chữ chạy theo câu, cháy chữ (burn-in), font Be Vietnam Pro đậm, nhấn từ khoá màu cam.
5. **Ba gói đăng** — tinh chỉnh caption Mốc 1 theo footage thực: **YouTube** (tiêu đề + mô tả + tags) · **TikTok** (caption + hashtag + CTA ghim) · **Facebook** (caption + CTA có SĐT/Zalo + hashtag). Liên hệ lấy từ SOP, thiếu → `[ĐIỀN]`.
6. **Việc tồn** — cảnh phải quay bù, dữ kiện cần anh Đức xác minh (giá/thông số), short phụ cắt được.

## Kỹ thuật dựng

- Nguồn hình: **footage thật** trong `footage-content/<ngày>/`. Chỉ chèn AI (Flow/Veo) cho **cảnh thiếu** không quay lại được — dùng skill `flow-studio` (rẻ, credits) hoặc `veo3-studio` (khi cần chất lượng).
- Giọng AI + nhạc nền + **phụ đề cháy chữ**: tái dùng pipeline skill **`video-nguoi-que`** (`scripts/make_subs.py`, `build_video.py`) — chỉ đổi nguồn hình từ "người que" sang footage thật. Ghép/chuẩn 9:16 bằng ffmpeg.
- Xuất **dọc 1080×1920**. Lưu video ra `production/content/dung/<ngày>-<slug>.mp4` (gitignore — nặng).

## Đăng (anh Đức tự làm)
- Xuất xong, trình anh Đức **duyệt**. Cả 3 kênh **anh tự đăng**.
- `tools/yt.py` dùng để **đo số liệu / nghiên cứu đối thủ**, KHÔNG tự đăng trong lệnh này (trừ khi anh Đức yêu cầu rõ đăng private để xem trước).

## Luật cứng
Không chạy khi data chưa an toàn · **số liệu kiểm kê từ log, không từ trí nhớ** · **cảnh trượt ghi thẳng** · không bịa giá/thông số/testimonial (thiếu → `[ĐIỀN]`) · tiếng Việt 100% · gọi **"anh Đức"** · **không tự đăng công khai**.
