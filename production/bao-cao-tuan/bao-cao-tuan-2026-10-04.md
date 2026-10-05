# Báo cáo tuần "Bộ Não Thứ Hai" — 2026-10-04

> So sánh tuần **28/09 – 04/10/2026** (tuần này) với tuần **21/09 – 27/09/2026** (tuần trước).
> Số liệu lấy nguyên văn từ `tools/bao_cao_tuan.py --json` (git log, `wiki/log.md`, `production/dmo/`, frontmatter wiki). Không tự cộng, không suy đoán.
> Bản cập nhật: tuần này nay đã **chốt đủ 7/7 ngày** (3/10 và 4/10 đã có đủ dữ liệu, khác với lần chạy báo cáo đầu tiên lúc 2 ngày này còn trống).

## 1. Bảng so sánh số liệu

| Chỉ số | Tuần này (28/9–4/10) | Tuần trước (21/9–27/9) |
|---|---|---|
| Commit git | **18** | **20** |
| Mục nhật ký `wiki/log.md` (ingest/query/lint/update) | **6** (ingest 6, query 0, lint 0, update 0) | **9** (ingest 8, query 0, lint 0, update 1) |
| Trang wiki mới | **6** | **9** |
| Số ngày có DMO | **7/7** | **7/7** |
| % DMO trung bình | **65%** | **60%** |

### 1.1. Chi tiết DMO từng ngày trong tuần này

| Ngày | Thứ | Việc đã xong | % |
|---|---|---|---|
| 28/9 | Thứ Hai | 15/18 | 83% |
| 29/9 | Thứ Ba | 11/18 | 61% |
| 30/9 | Thứ Tư | 11/19 | 58% |
| 1/10 | Thứ Năm | 11/19 | 58% |
| 2/10 | Thứ Sáu | 11/18 | 61% |
| 3/10 | Thứ Bảy | 10/18 | 56% |
| 4/10 | Chủ Nhật | 11/14 | **79%** |

## 2. Nhận định: bộ não tiến hoá thế nào so với tuần trước?

Về **nếp ngày (DMO)**: tuần này **tiến bộ hơn** tuần trước — % trung bình 65% so với 60%, và cả 7/7 ngày đều chốt đủ kiểm đếm. Không ngày nào tụt dưới 56%, trong khi tuần trước có ngày xuống 52%. Đáng chú ý nhất: ngày 28/9 lần đầu anh Đức gom đủ cả 4 mảng DMO (chạy bộ + học + dệt + trả hàng) trong 1 ngày (83%), và ngày 4/10 anh **hoàn thành giải bán marathon 21,32km với thành tích nhanh nhất từ trước đến nay (PR)** — chỉ hơn 1 tuần sau buổi chạy 3,27km đầu tiên (28/9). Ngày 3/10 còn có dấu mốc gia đình: bé SK lần đầu thi "kid run".

Về **wiki/tri thức**: tuần này **chậm lại rõ** — chỉ 6 mục nhật ký và 6 trang wiki mới, so với 9 và 9 của tuần trước. Và giống tuần trước, tuần này **100% là ingest footage xưởng hàng ngày** (mỗi ngày 1 trang `tom-tat-nguon/footage-xuong-...`, từ 28/9 đến 3/10) — không có `query`, `lint` hay `update` nào, nghĩa là wiki chỉ "ăn vào" dữ liệu thô tuần này, chưa có vòng tổng hợp/liên kết chéo sâu hơn (tuần trước còn có 1 dòng `update` — tách khách hàng [[thay-luong]] thành trang riêng).

Về **commit git**: 18 so với 20 — gần ngang nhau, không phải dấu hiệu chậm lại rõ rệt như số liệu wiki.

**Tóm lại:** mảng vận hành cá nhân (DMO, sức khỏe, gia đình) tiến bộ hơn tuần trước; mảng tích lũy tri thức (wiki) chậm lại, mới ở mức ingest thô, chưa sinh ra phân tích/liên kết mới.

## 3. Mục III. Làm ra tiền — nguyên văn số liệu từng ngày

| Ngày | Tiền thực nhận | Khách trả hàng |
|---|---|---|
| 28/9 (Thứ Hai) | **6.605.000 đ** (c Hoàn) | 2 khách — a Tuân (9.625.000đ) · cô Tuấn Huyền (520.000đ), tổng hàng trả 10.145.000đ |
| 29/9 (Thứ Ba) | **0 đ** — "Chưa có dòng tiền về ngày 29/9 trong Excel nhật ký thu" | 1 khách — c Hằng (3.250.000đ) |
| 30/9 (Thứ Tư) | **0 đ** — "Chưa có dòng tiền về ngày 30/9 trong Excel nhật ký thu" | 2 khách — a Nghĩa (9.100.000đ) · a Tuân (11.750.000đ), tổng hàng trả 20.850.000đ |
| 1/10 (Thứ Năm) | **0 đ** — "Chưa có dòng tiền về ngày 1/10 trong Excel nhật ký thu" | 1 khách — Cty Bform (1.572.000đ) |
| 2/10 (Thứ Sáu) | **0 đ** — "Chưa có dòng tiền về ngày 2/10 trong Excel nhật ký thu" | 2 khách — a Tuân (11.500.000đ) · c Hằng (4.327.000đ), tổng hàng trả 15.827.000đ |
| 3/10 (Thứ Bảy) | **0 đ** — "Chưa có dòng tiền về ngày 3/10 trong Excel nhật ký thu" | 1 khách — c Hiệp (1.300.000đ) |
| 4/10 (Chủ Nhật) | **3.900.000 đ** (C Nhung) | 2 khách — Bform (5.400.000đ) · cty Thanh Huyền (800.000đ), tổng hàng trả 6.200.000đ |

→ Tuần này (đủ 7/7 ngày): **2 ngày có tiền về** (28/9: 6.605.000đ, 4/10: 3.900.000đ), **5 ngày ghi "0 đ"** (29/9, 30/9, 1/10, 2/10, 3/10). Khách trả hàng ghi nhận ở **cả 7/7 ngày**, nhưng không cộng tổng tiền trả hàng cả tuần ở đây vì công cụ chỉ liệt kê từng ngày riêng, không có dòng tổng tuần.

## 4. Đề xuất cho tuần tới

1. Dòng tiền thực nhận rất thưa (chỉ 2/7 ngày có số) dù lượng hàng trả ra đều mỗi ngày — nên rà lại các khoản khách còn nợ (ví dụ a Tuân, a Nghĩa, c Hằng, Bform đã trả hàng nhiều ngày nhưng Excel nhật ký thu chưa ghi nhận tiền về tương ứng).
2. Khôi phục nhịp `update`/`lint`/`query` cho wiki — tuần này chỉ ingest thô 7 ngày liên tiếp, chưa có vòng rà soát/tổng hợp nào; nên dành 1 buổi lọc các trang `tom-tat-nguon/footage-xuong-...` mới để rút khái niệm/thực thể chung (nếu có), như tuần trước đã làm với [[thay-luong]].
3. Giữ nhịp 5h sáng chạy bộ đang rất tốt (từ 3,27km lên 21,32km PR trong hơn 1 tuần) — tuần tới có thể cân nhắc ghi lại bài học phục hồi sau giải vào DMO để không đứt mạch.
