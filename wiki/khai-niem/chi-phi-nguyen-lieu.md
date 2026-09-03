---
tieu_de: Chi phí nguyên liệu xưởng dệt bo (sợi + nhuộm + dớ)
loai: khai-niem
ngay_tao: 2026-08-21
ngay_cap_nhat: 2026-08-21
nguon: []
tags:
  - chi-phi
  - san-xuat
  - gia-thanh
---

# Chi phí nguyên liệu xưởng dệt bo

Anh Đức cung cấp bảng định mức (2026-08-21). Chi phí nguyên liệu để làm ra
thành phẩm gồm **3 khoản tính theo cân**: sợi, nhuộm, dớ.

## Đơn giá nguyên liệu (theo kg)

| Khoản | Đơn giá |
|---|---|
| Sợi | 42.000 đ/kg |
| Nhuộm | 23.000 đ/kg |
| Dớ | 3.000 đ/kg |
| **Gộp** | **68.000 đ/kg** |

> Mọi thành phẩm (bộ áo polo, cạp, gấu…) đều gồm đủ **sợi + nhuộm + dớ** →
> dùng luôn đơn giá gộp **68.000 đ/kg**.

## Định mức khối lượng

| Đơn vị | Khối lượng | Chi phí NL / đơn vị (× 68.000) |
|---|---|---|
| 100 cổ | 1,945 kg → 1 cổ = 0,01945 kg | 1.323 đ/cổ |
| 100 tay | 1,42 kg → 1 tay = 0,0142 kg | 966 đ/tay |
| **1 bộ = 1 cổ + 1 tay** | **0,03365 kg** | **2.288 đ/bộ** |
| 10 cạp quần | 0,65 kg → 1 cạp = 0,065 kg | 4.420 đ/cạp |
| 10 gấu (a Tuân) | 0,985 kg → 1 gấu = 0,0985 kg | 6.698 đ/gấu |

**1 bộ = 1 bộ áo polo hoàn chỉnh** (thành phẩm cổ + tay). Cạp, gấu là mặt hàng riêng.

## Công thức tính chi phí một tháng

```
Chi phí NL = 68.000 × [ (số bộ × 0,03365)
                      + (số cổ lẻ × 0,01945)
                      + (số tay lẻ × 0,0142)
                      + (số cạp × 0,065)
                      + (số gấu × 0,0985)
                      + (kg hàng bán theo cân) ]
```

**Lưu ý bóc tách sản lượng từ khối TRẢ HÀNG** (sheet `TỔNG HỢP`):
- Nội dung ghi tự do, đơn vị lẫn lộn: `b`/`bộ` = bộ · `cổ` = cổ lẻ · `tay` = tay lẻ ·
  cạp/cạp lô = cạp quần · `kg` = hàng bán theo cân (bo tay, hàng gân…).
- Dòng có tổng cuối (`… = 1200b`, `… = 500 cái`, `… = 35kg`) → **dùng số tổng**, không cộng lại các phần (tránh đếm trùng).
- Khi nội dung ghi thẳng **kg thực** thì **ưu tiên kg thực** (vd `rêu gân 700 cái = 88kg` → lấy 88kg).
  Hàng gân cân nặng hơn định mức bộ chuẩn nhiều nên không suy từ số cái/bộ.

Đây là chi phí **nguyên liệu**, độc lập với giá bán; chưa gồm nhân công, điện, hao mòn máy, vận chuyển, lặt vặt.

Xem thêm [[doanh-thu-that]].
