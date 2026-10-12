# Báo cáo tuần "Bộ Não Thứ Hai" — 05/10 → 11/10/2026

> Số liệu lấy từ `tools/bao_cao_tuan.py --json` (git log, `wiki/log.md`, `production/dmo/`, frontmatter wiki). Không tự cộng, không suy đoán.
>
> **Cập nhật 12/10:** bản đầu (chạy đúng tối Chủ Nhật 11/10) ghi nhận 2 ngày 09/10–10/10 còn thiếu/0% vì DMO chưa kịp chốt trên máy. Anh Đức đã chốt xong và push lên git; bản này chạy lại công cụ với dữ liệu đầy đủ 7/7 ngày.

## 1. Bảng so sánh 2 tuần

| Chỉ số | Tuần này (05/10–11/10) | Tuần trước (28/09–04/10) |
|---|---|---|
| Commit git | 23 | 18 |
| Mục nhật ký `ingest` | 7 | 6 |
| Mục nhật ký `query` | 0 | 0 |
| Mục nhật ký `lint` | 0 | 0 |
| Mục nhật ký `update` | 0 | 0 |
| Trang wiki mới | 7 (tom-tat-nguon/footage-xuong-...) | 6 (tom-tat-nguon/footage-xuong-...) |
| Số ngày có file DMO | 7 / 7 | 7 / 7 |
| % DMO trung bình | **70%** | 65% |

Commit tăng mạnh (18 → 23) một phần vì các commit "sửa/chốt bù DMO 9–10/10" được đẩy dồn trong ngày 10–11/10 (tìm lại bảng tích, điền số Excel, viết tổng kết) — nợ dữ liệu được trả đủ, không phải việc mới phát sinh thêm.

## 2. Nhận định — bộ não tiến hoá thế nào

- **Nhánh ingest (nạp footage xưởng) vẫn đều và nhích lên:** 7 lần nạp/tuần (so với 6 tuần trước — tuần này dài hơn 1 ngày ingest vì trùng mốc 11/10). Mỗi ngày một trang tóm tắt nguồn mới trong `wiki/tom-tat-nguon/`, không đứt mạch.
- **Nhánh nếp ngày (DMO) phục hồi và vượt tuần trước:** đủ 7/7 ngày có file, % trung bình **70%** — cao hơn tuần trước (65%). Ban đầu 2 ngày 09/10, 10/10 có dấu hiệu chậm (09/10 còn 0% lúc tối Chủ Nhật, 10/10 chưa có file), nhưng anh Đức đã tìm lại bảng tích tay và chốt đủ: 09/10 đạt 13/19 (68%), 10/10 đạt 12/18 (67%). Ngày 11/10 (Chủ Nhật) cao nhất tuần — 14/18 (78%).
- **Vẫn chưa có `query` hay `lint` nào** trong 2 tuần liên tiếp — toàn bộ log là ingest thuần, chưa có vòng "truy vấn → sinh trang tổng hợp" hay rà soát sức khỏe wiki.
- **Sản phẩm ra trong tuần:** 7 trang tóm tắt nguồn footage xưởng (05–11/10) + báo cáo tuần này (bản đầu và bản cập nhật). Không có sản phẩm khác trong `production/` (blog, kịch bản...) ghi nhận qua git log.

## 3. III. Làm ra tiền — trích nguyên văn dòng kiểm đếm (đủ 7/7 ngày)

| Ngày | Dòng tiền ghi trong DMO | Khách trả hàng |
|---|---|---|
| 05/10 (T2) | `TỔNG: 0 đ` — "Chưa có dòng tiền về ngày 5/10 trong Excel nhật ký thu" | 1 khách — a Nghĩa (8.125.000đ) |
| 06/10 (T3) | CK a Nghĩa **49.000.000 đ** → TỔNG 49.000.000 đ; 6 lọ TK0: 14.700.000 đ | 1 khách Zalo — c Hoàn (3.710.000đ); bảng tay tích thêm c Nhi & LFD nhưng Zalo "Trả hàng" chưa đăng |
| 07/10 (T4) | CK c Hiệp **15.000.000 đ** → TỔNG 15.000.000 đ; 6 lọ TK0: 4.500.000 đ | 1 khách — c Hằng (2.080.000đ) |
| 08/10 (T5) | CK a Minh **3.000.000 đ** → TỔNG 3.000.000 đ; 6 lọ TK0: 900.000 đ | 2 khách — c Nhi (14.525.000đ) · a Nghĩa (7.087.500đ); tổng hàng trả ghi sẵn: 21.612.500đ |
| 09/10 (T6) | CK c Ngọc **8.000.000 đ** → TỔNG 8.000.000 đ; 6 lọ TK0: 2.400.000 đ | 0 khách [Zalo "Trả hàng" 9/10 không có tin]; bảng tay tích c Hiệp nhưng Zalo chưa đăng |
| 10/10 (T7) | CK cô Hoa **4.870.000 đ** → TỔNG 4.870.000 đ; 6 lọ TK0: 1.461.000 đ | 0 khách [Zalo "Trả hàng" 10/10 không có tin] |
| 11/10 (CN) | CK a Minh **3.725.000 đ** → TỔNG 3.725.000 đ; 6 lọ TK0: 1.117.500 đ (Excel ghi nhầm ngày 11/11 — thực là 11/10) | 3 khách — a Nghĩa (15.600.000đ) · c Hiệp (3.900.000đ) · a Minh (6.665.000đ); tổng hàng trả ghi sẵn: 26.165.000đ |

Tóm: **6/7 ngày có tiền về** (06→11/10), **1 ngày ghi rõ 0đ** (05/10) — không có ngày nào còn thiếu số. Không cộng tổng tuần vì công cụ không tự tính tổng, chỉ trích nguyên văn từng dòng.

## 4. Đề xuất cho tuần tới

1. **Đăng Zalo nhóm "Trả hàng" đều hơn** — nhiều ngày (06, 08, 09/10) bảng tay đã tích khách trả hàng nhưng nhóm Zalo chưa đăng kịp, khiến số liệu phải ghi "chờ cập nhật". Đăng ngay trong ngày để sổ khớp luôn, không phải đối chiếu lại sau.
2. **Chốt DMO đúng tối hôm đó** — tuần này 2 ngày (09, 10/10) phải bù lại sau 1–2 ngày mới có đủ số. Nếp chốt ngay buổi tối giúp báo cáo tuần không phải chạy lại lần hai.
3. **Dành 1 lần truy vấn hoặc rà soát trong tuần tới** (ví dụ so sánh doanh thu các tuần, hoặc lint phát hiện trang mồ côi) — 2 tuần liền 100% log vẫn là ingest, chưa có trang `tong-hop`/`so-sanh` nào được sinh ra từ việc "lưu ngược giá trị mới".
