---
tieu_de: Báo cáo tuần "Bộ Não Thứ Hai" — 14/09 đến 20/09/2026
loai: tong-hop
ngay_tao: 2026-09-20
ngay_cap_nhat: 2026-09-21
nguon:
  - tools/bao_cao_tuan.py (output --json --den 2026-09-20)
  - wiki/log.md
  - production/dmo/DMO-2026-09-14.md .. DMO-2026-09-20.md
tags:
  - bao-cao-tuan
  - dmo
  - so-sach
---

# Báo cáo tuần "Bộ Não Thứ Hai" — 14/09 → 20/09/2026

> **Bản chạy lại 21/09**, sau khi anh Đức đã cập nhật đủ DMO 18, 19, 20/09 — thay cho bản chạy tối 20/09 khi 3 ngày này còn thiếu dữ liệu. Tuần 14–20/09 nay đã **chốt đủ 7/7 ngày**.

## 1. Bảng so sánh 2 tuần

| Chỉ số | Tuần trước (07/09–13/09) | Tuần này (14/09–20/09) | Chênh lệch |
|---|---|---|---|
| Commit git | 30 | 11 | ↓ mạnh |
| Mục nhật ký `ingest` | 6 | 7 | ↑ |
| Mục nhật ký `query` | 0 | 0 | = |
| Mục nhật ký `lint` | 0 | 0 | = |
| Mục nhật ký `update` | 0 | 0 | = |
| Tổng mục log.md | 6 | 7 | ↑ |
| Trang wiki mới | 6 | 7 | ↑ |
| Số ngày có DMO | 7 | 7 | = |
| % DMO trung bình | 55% | 51% | ↓ nhẹ |

## 2. Nhận định — bộ não tiến hoá thế nào so với tuần trước

Với dữ liệu đầy đủ, bức tranh khác hẳn bản chạy tối 20/09 (khi đó thiếu 3 ngày nên trông như "đứt quãng"): tuần này thực ra **vận hành liên tục cả 7/7 ngày**, kể cả Thứ Bảy (19/09) và Chủ Nhật (20/09) — không có ngày nào bỏ trắng. Commit git giảm mạnh so với tuần trước (30 → 11) nhưng đó là vì tuần trước có đợt sửa công cụ dồn dập (`zalo_dump.mjs`, các quy tắc skill DMO...); tuần này commit gọn hơn nhưng đều — mỗi ngày đúng 1 commit DMO + 1 commit ingest wiki. Số mục nhật ký (6 → 7) và số trang wiki mới (6 → 7) đều **tăng nhẹ**, vì tuần này nạp đủ 7 ngày footage xưởng (14–20/09) so với 6 ngày tuần trước (thiếu 11/09). Loại tri thức nạp vào vẫn một mạch: toàn bộ 7 trang mới đều là `tom-tat-nguon` cho footage xưởng, không có `khai-niem`/`thuc-the`/`so-sanh` mới, và không có mục `query` hay `lint` nào — bộ não vẫn ở pha "nạp đều mỗi ngày", chưa được hỏi lại hay rà soát sức khoẻ.

Sản phẩm phụ tuần này: công cụ `bieu_do_tra_hang.py` (biểu đồ đường tiền trả hàng đọc thẳng từ DMO) + biểu đồ tháng 9, và một điều chỉnh skill DMO (ưu tiên đọc số có sẵn trong DMO, không mở lại Zalo/Excel nếu không cần) — cải tiến cách lấy số liệu hơn là tri thức mới.

% DMO trung bình giảm nhẹ (55% → 51%, 4 điểm) — không đáng lo bằng con số 41% ở bản chạy thiếu dữ liệu trước đó. Nhìn theo từng ngày: 4 ngày đầu tuần (14–17/09) đạt 42–61%, riêng 16–17/09 bài tổng kết tự ghi nhận việc học cá nhân (tiếng Trung, LTTTL, đọc sách, chạy bộ) bị "việc xưởng lấn" 2 ngày liền. 18–19/09 xưởng vẫn mạnh (dệt trọn, tiền về lớn) nhưng việc học tiếp tục lỡ. Điểm sáng nằm ở **20/09 (Chủ Nhật)**: bảng việc tồn đã sạch từ tối 19/09, và bài tổng kết ghi rõ "quay lại được việc học tiếng Trung sau nhiều ngày trống" — dấu hiệu nhịp cá nhân đang được kéo lại sau khi bị xưởng cuốn theo giữa tuần.

## 3. III. Làm ra tiền — trích nguyên văn từng ngày

| Ngày | Tổng tiền về (nguyên văn Excel) | Khách trả hàng |
|---|---|---|
| 14/09 (T2) | **37.150.000 đ** — Tiến 3.900.000 + a Tuân 33.250.000 (chia 6 lọ: 11.145.000đ TK0) | 2 khách — c Hằng (3.770.000đ) + c Hiệp (5.250.000đ), tổng 9.020.000đ |
| 15/09 (T3) | **0 đ** — "Không có dòng tiền về ngày 15/9 trong Excel nhật ký thu" | 2 khách — c Hằng (5.525.000đ) + c Sự (650.000đ), tổng 6.175.000đ |
| 16/09 (T4) | **0 đ** — "Không có dòng tiền về ngày 16/9 trong Excel nhật ký thu" | 2 khách — a Nghĩa (18.650.000đ) + cty Bform (350.000đ), tổng 19.000.000đ |
| 17/09 (T5) | **0 đ** — "Không có dòng tiền về ngày 17/9 trong Excel nhật ký thu" | 3 khách — c Hằng (3.900.000đ) + c Hoàn (5.795.000đ) + a Tuân (8.400.000đ), tổng 18.095.000đ |
| 18/09 (T6) | **11.285.000 đ** — c Hoàn 5.795.000 + a Minh 3.000.000 + cô Huyền Tuấn 2.490.000 (chia 6 lọ: 3.385.500đ TK0) | 2 khách — c Hằng (1.040.000đ) + a Nghĩa (9.300.000đ), tổng 10.340.000đ |
| 19/09 (T7) | **28.283.000 đ** — c Hằng (chia 6 lọ: 8.484.900đ TK0) | 2 khách — c Hằng (2.720.000đ) + c Ngân (390.000đ), tổng 3.110.000đ |
| 20/09 (CN) | **0 đ** — "Không có dòng tiền về ngày 20/9 trong Excel nhật ký thu (Chủ Nhật)" | 2 khách — c Hằng (740.000đ) + Tiến (13.000.000đ), tổng 13.740.000đ |

→ Tuần này có **3 ngày có tiền về TK** (14, 18, 19/09) và **4 ngày ghi 0đ** (15, 16, 17, 20/09). Cả 4 ngày "0đ" đều có khách trả hàng bình thường — tiền chỉ đơn giản là chưa vào tài khoản đúng ngày đó, giống mẫu hình các tuần trước. Không tự cộng tổng tiền cả tuần vì mỗi dòng là một khoản riêng theo ngày, không phải luỹ kế — anh Đức đối chiếu trực tiếp với sổ thật nếu cần tổng chính xác.

## 4. Đề xuất cho tuần tới

1. **Giữ nhịp chốt DMO đúng ngày** (kể cả Thứ Bảy, Chủ Nhật như tuần này) — tuần 14–20/09 là tuần đầu tiên gần đây chốt trọn 7/7 ngày, nên duy trì thay vì để dồn cập nhật sau như đã xảy ra với 18–20/09.
2. **Bám nhịp học cá nhân vừa lấy lại được ở 20/09** — đặt khung giờ cố định cho tiếng Trung/đọc sách/LTTTL/chạy bộ ngay cả những ngày xưởng bận (16–19/09), để không lặp lại vết "việc xưởng lấn" đã ghi nhận 2 ngày liền giữa tuần.
3. **Thử chạy `query` hoặc `lint` ít nhất 1 lần** — 3 tuần liên tiếp không có mục nào trong log.md ngoài `ingest`; wiki vẫn đang ở giai đoạn nạp thuần, chưa được hỏi lại hay rà soát sức khoẻ (trang mồ côi, khái niệm cần tách trang...).
