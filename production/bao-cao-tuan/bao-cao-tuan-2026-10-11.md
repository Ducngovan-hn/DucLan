# Báo cáo tuần "Bộ Não Thứ Hai" — 05/10 → 11/10/2026

> Số liệu lấy từ `tools/bao_cao_tuan.py --json` (git log, `wiki/log.md`, `production/dmo/`, frontmatter wiki). Không tự cộng, không suy đoán.

## 1. Bảng so sánh 2 tuần

| Chỉ số | Tuần này (05/10–11/10) | Tuần trước (28/09–04/10) |
|---|---|---|
| Commit git | 15 | 18 |
| Mục nhật ký `ingest` | 6 | 6 |
| Mục nhật ký `query` | 0 | 0 |
| Mục nhật ký `lint` | 0 | 0 |
| Mục nhật ký `update` | 0 | 0 |
| Trang wiki mới | 6 (tom-tat-nguon/footage-xuong-...) | 6 (tom-tat-nguon/footage-xuong-...) |
| Số ngày có file DMO | **5 / 7** (05,06,07,08,09/10) | 7 / 7 (đủ cả tuần) |
| % DMO trung bình | **56%** | 65% |

**Lưu ý quan trọng:** hôm nay Chủ Nhật 11/10 — thời điểm chạy báo cáo này — **chưa có file `DMO-2026-10-10.md` và `DMO-2026-10-11.md`**. Tức Thứ Bảy 10/10 và Chủ Nhật 11/10 chưa được tạo/chốt DMO. Ngày 09/10 (Thứ Sáu) có file nhưng **0/19 việc được tick (0%)** — coi như chưa làm. Các số "5 ngày / 56%" ở trên chỉ phản ánh 05→09/10; 2 ngày cuối tuần hoàn toàn **chưa có dữ liệu**.

## 2. Nhận định — bộ não tiến hoá thế nào

- **Nhánh ingest (nạp footage xưởng) vẫn đều, không đứt mạch:** đúng 6 lần nạp/tuần cả hai tuần, mỗi ngày một trang tóm tắt nguồn mới trong `wiki/tom-tat-nguon/`. Đây là phần ổn định nhất của hệ thống.
- **Nhánh nếp ngày (DMO) chậm lại rõ:** từ 7/7 ngày (65% TB) tuần trước xuống 5/7 ngày có file (56% TB) tuần này, và 2 ngày gần nhất (10/10, 11/10) **trống hoàn toàn** — chưa rõ là quên tạo DMO hay chưa chốt kịp. Hoạt động git cũng giảm (18 → 15 commit), phần lớn giảm đến từ việc thiếu các commit "tạo DMO + đồng bộ Lịch" của 2 ngày cuối.
- **Chưa có `query` hay `lint` nào trong 2 tuần liên tiếp** — toàn bộ log vẫn là ingest thuần (nạp nguồn), chưa có lần nào wiki được truy vấn để sinh trang tổng hợp (`loai: tong-hop`/`so-sanh`) hay rà soát sức khỏe wiki. Tri thức đang tích lũy một chiều (nạp vào), chưa có vòng "suy ra giá trị mới rồi lưu ngược".
- **Sản phẩm ra trong tuần:** 6 trang tóm tắt nguồn footage xưởng (05–10/10) + chính báo cáo tuần này; không có sản phẩm `production/` khác (blog, kịch bản...) được ghi nhận qua git log tuần này.

## 3. III. Làm ra tiền — trích nguyên văn dòng kiểm đếm

| Ngày | Dòng tiền ghi trong DMO | Khách trả hàng |
|---|---|---|
| 05/10 (T2) | `TỔNG: 0 đ` — "Chưa có dòng tiền về ngày 5/10 trong Excel nhật ký thu" | 1 khách — a Nghĩa (8.125.000đ) |
| 06/10 (T3) | CK a Nghĩa **49.000.000 đ** → TỔNG 49.000.000 đ; 6 lọ TK0: 14.700.000 đ | 1 khách Zalo — c Hoàn (3.710.000đ); bảng tay tích thêm c Nhi & LFD nhưng Zalo "Trả hàng" chưa đăng |
| 07/10 (T4) | CK c Hiệp **15.000.000 đ** → TỔNG 15.000.000 đ; 6 lọ TK0: 4.500.000 đ | 1 khách — c Hằng (2.080.000đ) |
| 08/10 (T5) | CK a Minh **3.000.000 đ** → TỔNG 3.000.000 đ; 6 lọ TK0: 900.000 đ | 2 khách — c Nhi (14.525.000đ) · a Nghĩa (7.087.500đ); tổng hàng trả ghi sẵn: 21.612.500đ |
| 09/10 (T6) | Chưa tick: "Có tiền thực nhận hôm nay: _______ đ" / "chia 6 lọ: _______ đ" — **chưa điền số** | chưa có dữ liệu (mục kiểm đếm chưa làm) |
| 10/10 (T7) | **chưa có file DMO** | chưa có |
| 11/10 (CN, hôm nay) | **chưa có file DMO** | chưa có |

Tóm: tuần này có **3 ngày có tiền về** (06, 07, 08/10), **1 ngày ghi rõ 0đ** (05/10), **1 ngày chưa chốt số** (09/10), và **2 ngày chưa có dữ liệu** (10, 11/10). Không cộng tổng vì 09/10, 10/10, 11/10 chưa đủ số.

## 4. Đề xuất cho tuần tới

1. **Chốt bù DMO 10/10 và 11/10** càng sớm càng tốt — nếu không, khoảng trống "III. Làm ra tiền" của 2 ngày này sẽ mất hẳn, không thể tổng hợp lại sau. Đồng thời tick/điền số còn thiếu của 09/10.
2. **Theo dõi khoản c Nhi & LFD (ghi nhận bảng tay 06/10)** — cập nhật khi nhóm Zalo "Trả hàng" đăng, để số khách trả hàng không bị lệch giữa bảng tay và Zalo.
3. **Dành 1 lần truy vấn hoặc rà soát trong tuần** (ví dụ so sánh doanh thu các tuần, hoặc lint phát hiện trang mồ côi) để bắt đầu sinh ra trang `tong-hop`/`so-sanh` — hiện 2 tuần liền 100% log là ingest, chưa có vòng "lưu ngược giá trị mới" nào.
