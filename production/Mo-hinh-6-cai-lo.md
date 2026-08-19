# MÔ HÌNH 6 CÁI LỌ — QUẢN LÝ DÒNG TIỀN

> Bản markdown gọn của `Mo-hinh-6-cai-lo.xlsx`. Toàn bộ logic tính giữ nguyên.
> Số tiền đơn vị VND, không dùng số lẻ thập phân.

---

## 1. Dòng tiền chạy thế nào

```
Khách chuyển tiền  →  TÀI KHOẢN CÔNG TY
       ├─ 70%  giữ lại ở công ty (vốn xoay vòng cho xưởng)
       └─ 30%  rút ra TÀI KHOẢN SỐ 0  →  chia tiếp vào 6 lọ
                  TK1 Thiết yếu 55% · TK2 Tự do tài chính 10% · TK3 Tiết kiệm dài hạn 10%
                  TK4 Giáo dục 10%  · TK5 Hưởng thụ 10%      · TK6 Cho đi 5%
```

**Hai tham số chỉnh được:**

| Tham số | Mặc định | Ghi chú |
|---|---|---|
| Tỷ lệ rút ra TK0 | 30% | anh Đức tự đặt, chưa lấy từ nguồn nào |
| Tỷ lệ giữ lại công ty | 70% | = 100% − tỷ lệ rút ra |

**Kiểm tra bắt buộc:** `TK0 + giữ lại = tổng tiền vào công ty` (lệch thì sai).

---

## 2. Sáu cái lọ

| Mã | Tên lọ | Mục đích sử dụng | Tỷ lệ |
|---|---|---|---|
| TK1 | Thiết yếu (NEC) | Ăn uống, nhà cửa, đi lại, hóa đơn, sinh hoạt hằng ngày | 55% |
| TK2 | Tự do tài chính (FFA) | Đầu tư, mua tài sản sinh lời — **KHÔNG được tiêu** | 10% |
| TK3 | Tiết kiệm dài hạn (LTSS) | Mua nhà, xe, máy dệt mới, quỹ dự phòng lớn | 10% |
| TK4 | Giáo dục (EDU) | Sách, khóa học, học nghề, nâng cấp bản thân | 10% |
| TK5 | Hưởng thụ (PLAY) | Du lịch, ăn chơi, mua sắm cho vui — tiêu hết mỗi tháng | 10% |
| TK6 | Cho đi (GIVE) | Từ thiện, biếu bố mẹ, giúp đỡ người khác | 5% |
| | **TỔNG** | | **100%** |

Tỷ lệ 6 lọ theo mô hình JARS chuẩn (55/10/10/10/10/5) của T. Harv Eker.
**Tổng 6 lọ phải đúng 100%** — sai một chút là hỏng cả sổ.

---

## 3. Công thức tính

Với mỗi khoản khách chuyển vào công ty, gọi `X` là số tiền:

```
TK0            = X × 30%
Giữ lại công ty = X × 70%

TK1 = TK0 × 55%   →  X × 30% × 55%
TK2 = TK0 × 10%
TK3 = TK0 × 10%
TK4 = TK0 × 10%
TK5 = TK0 × 10%
TK6 = TK0 ×  5%

Kiểm tra: TK1+TK2+TK3+TK4+TK5+TK6 = TK0
```

**Số dư từng lọ** = tổng đã nạp (cộng dồn từ nhật ký thu) − tổng đã chi (cộng dồn từ nhật ký chi, lọc theo mã lọ).

### Ví dụ: khách chuyển 20.000.000 đ

| Khoản | Số tiền |
|---|---|
| Vào công ty | 20.000.000 |
| Giữ lại công ty (70%) | 14.000.000 |
| **TK0 rút ra (30%)** | **6.000.000** |
| → TK1 Thiết yếu 55% | 3.300.000 |
| → TK2 Tự do tài chính 10% | 600.000 |
| → TK3 Tiết kiệm dài hạn 10% | 600.000 |
| → TK4 Giáo dục 10% | 600.000 |
| → TK5 Hưởng thụ 10% | 600.000 |
| → TK6 Cho đi 5% | 300.000 |
| Cộng 6 lọ | 6.000.000 ✓ |

---

## 3b. Quy tắc làm tròn (đề xuất — chờ anh Đức chốt)

Excel tính bằng số thực nên chấp nhận số lẻ; sổ tiền thật thì không. Nhân 30% rồi 55% rất dễ ra số lẻ đồng — ví dụ 333.333 đ × 30% = 99.999,9 đ.

Quy tắc để tổng **luôn khớp tuyệt đối**, không mất một đồng nào:

```
Tầng 1:  TK0 = làm tròn(X × 30%) về số nguyên đồng
         Giữ lại công ty = X − TK0          ← lấy phần còn lại, không nhân 70%

Tầng 2:  TK2…TK6 = làm tròn(TK0 × tỷ lệ) về số nguyên đồng
         TK1 = TK0 − (TK2+TK3+TK4+TK5+TK6)  ← lọ lớn nhất gánh phần dư
```

Cách này bảo đảm `TK0 + giữ lại = X` và `tổng 6 lọ = TK0` đúng từng đồng. Phần dư dồn vào TK1 nhiều nhất là vài đồng.

---

## 4. Nhật ký thu — tiền khách chuyển vào

Mỗi khoản tiền vào ghi **một dòng**. Chỉ cần nhập 3 cột đầu, phần chia lọ tính ra từ công thức mục 3.

| Ngày | Người chuyển / Nội dung | Số tiền vào công ty |
|---|---|---|
| 2026-07-28 | *(ví dụ)* Khách A chuyển tiền bo | 20.000.000 |

Cột dẫn xuất (không nhập tay): TK0 · Giữ lại công ty · TK1 · TK2 · TK3 · TK4 · TK5 · TK6.

---

## 5. Nhật ký chi — tiền lấy ra từ từng lọ

Mỗi lần tiêu ghi **một dòng**, bắt buộc chỉ rõ tiêu từ lọ nào (TK1…TK6).

| Ngày | Lọ | Chi vào việc gì | Số tiền |
|---|---|---|---|
| 2026-07-28 | TK1 | *(ví dụ)* Tiền chợ, điện nước | 3.000.000 |

**Quy tắc chi:** không được để lọ nào âm. Chi vượt số dư của lọ đó → từ chối, không ghi.

---

## 6. Bảng số dư (cập nhật mỗi khi có thu/chi)

| Mã | Tên lọ | Đã nạp | Đã chi | Số dư còn lại |
|---|---|---|---|---|
| TK1 | Thiết yếu | 3.300.000 | 3.000.000 | 300.000 |
| TK2 | Tự do tài chính | 600.000 | 0 | 600.000 |
| TK3 | Tiết kiệm dài hạn | 600.000 | 0 | 600.000 |
| TK4 | Giáo dục | 600.000 | 0 | 600.000 |
| TK5 | Hưởng thụ | 600.000 | 0 | 600.000 |
| TK6 | Cho đi | 300.000 | 0 | 300.000 |
| | **TỔNG** | **6.000.000** | **3.000.000** | **3.000.000** |

*(số trên là hai dòng ví dụ trong file gốc — xóa khi dùng thật)*

---

## 7. Dùng hằng ngày

1. **Khách chuyển tiền** → ghi 1 dòng vào *Nhật ký thu*: ngày · tên khách · số tiền. Sáu lọ tự chia.
2. **Tiêu tiền** → ghi 1 dòng vào *Nhật ký chi*: ngày · chọn lọ (TK1…TK6) · nội dung · số tiền.
3. **Xem còn bao nhiêu** → nhìn cột *Số dư còn lại* ở bảng mục 6.

**Muốn đổi tỷ lệ:**
- Đổi 30% / 70% → sửa tham số ở mục 1.
- Đổi tỷ lệ 6 lọ → sửa cột *Tỷ lệ* ở mục 2, tổng vẫn phải đúng 100%.

---

## 8. Kiểm tra bắt buộc trước mỗi báo cáo

- [ ] Tổng tỷ lệ 6 lọ = 100%
- [ ] TK0 + giữ lại công ty = tổng tiền vào công ty
- [ ] Tổng 6 lọ đã nạp = TK0
- [ ] Không lọ nào có số dư âm
- [ ] Không dòng thu/chi nào bị ghi trùng

Sai bất kỳ mục nào → dừng, không xuất báo cáo.
