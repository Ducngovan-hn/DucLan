---
description: Dựng kịch bản QUAY content cho 1 ngày Xưởng Bo Đức Lan — chủ đề theo lịch 28 ngày, hook, shot list tại xưởng, lời thoại, 3 gói caption YT/TikTok/FB
argument-hint: "[dd/mm hoặc YYYY-MM-DD — bỏ trống = hôm nay]"
---

# /kich-ban-ngay $ARGUMENTS

Dựng bản kịch bản **quay content** cho một ngày của Xưởng Dệt Bo Đức Lan.

## Cách chạy

1. **Xác định ngày.** `$ARGUMENTS` trống → dùng hôm nay (`date +%F`). Có → dùng ngày đó.
2. **Gọi agent `dao-dien-28ngay`** (Agent tool, `subagent_type: "dao-dien-28ngay"`, `run_in_background: false`) với prompt:
   > Dựng bản kịch bản quay content đầy đủ cho **ngày $ARGUMENTS** (trống thì hôm nay). Tuân thủ toàn bộ quy trình trong định nghĩa agent: đọc lịch 28 ngày để lấy nhóm + ý, viết đủ 9 phần, cập nhật lịch/kho ý tưởng/log. Kết thúc trả về đường dẫn file + tóm tắt 5 dòng.
3. **Báo lại cho anh Đức:** đường dẫn file + tóm tắt (Ngày N/28 · nhóm · chủ đề · loại video + giọng · cú đắt nhất ngày).

## Quy trình đầy đủ
Xem định nghĩa agent `.claude/agents/dao-dien-28ngay.md`.
Nguồn nền: `production/content/lich-28-ngay.md` · `kho-y-tuong.md` · `guideline-social.md` · `SOP-mot-ngay-content.md` · `wiki/products/`.

## Luật cứng
Tiếng Việt 100% · quay **DỌC 9:16** · **cấm bịa giá/thông số/testimonial** (thiếu → `[ĐIỀN — anh Đức bổ sung]`) · liên hệ chỉ lấy từ SOP · wikilink sản phẩm · gọi **"anh Đức"**.
