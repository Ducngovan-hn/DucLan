#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chi phí nguyên vật liệu (sợi + nhuộm + dớ) — Xưởng Dệt Bo Đức Lan.

Hai chế độ:
  liet-ke --thang 7 [--nam 2026]
      In các dòng khối TRẢ HÀNG của tháng (ngày | mã KH | nội dung | tiền)
      để LLM bóc tách sản lượng. Đây là việc DUY NHẤT cần LLM đọc.

  tinh --json sanluong.json
      Nhận sản lượng đã bóc rồi tính chi phí NVL. Không đọc lại Excel.
      JSON: {"thang":7, "bo":24879, "co":11150, "tay":1490,
             "cap":2540, "gau":0, "kg":196.0}
      (mọi khoá số lượng đều mặc định 0 nếu thiếu)

Định mức (anh Đức cung cấp 2026-08-21):
  Sợi 42.000 + Nhuộm 23.000 + Dớ 3.000 = 68.000 đ/kg (mọi thành phẩm)
  100 cổ = 1,945kg | 100 tay = 1,42kg | 1 bộ = 1 cổ + 1 tay
  10 cạp = 0,65kg  | 10 gấu = 0,985kg
"""
import sys, json, argparse, datetime

GIA_KG = 42000 + 23000 + 3000          # 68.000 đ/kg
KG = {
    "co":  1.945 / 100,                 # 1 cổ
    "tay": 1.42  / 100,                 # 1 tay
    "cap": 0.65  / 10,                  # 1 cạp quần
    "gau": 0.985 / 10,                  # 1 gấu
}
KG["bo"] = KG["co"] + KG["tay"]        # 1 bộ = 1 cổ + 1 tay
XLSX = "production/Xưởng Dệt Bo Đức Lan 2026.xlsx"

TEN = {"bo": "Bộ", "co": "Cổ lẻ", "tay": "Tay lẻ",
       "cap": "Cạp", "gau": "Gấu", "kg": "Bán theo cân (kg)"}


def liet_ke(thang, nam):
    import openpyxl
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb["TỔNG HỢP"]
    n = 0
    print(f"# TRẢ HÀNG tháng {thang}/{nam} — bóc sản lượng từ cột NỘI DUNG")
    print("# quy ước: b/bộ=bộ · cổ=cổ lẻ · tay=tay lẻ · cạp/cạp lô=cạp · kg=bán theo cân")
    print("# dòng có tổng cuối (…=1200b / =500 cái / =35kg) -> dùng số TỔNG, đừng cộng lại các phần")
    print("# có kg thực ghi thẳng -> ưu tiên kg thực (vd 'rêu gân 700 cái = 88kg' -> 88kg)")
    print("-" * 72)
    for r in ws.iter_rows(min_row=5, values_only=True):
        ngay, ma, nd, tt = r[1], r[2], r[3], r[4]
        if isinstance(ngay, datetime.datetime) and ngay.month == thang and ngay.year == nam:
            n += 1
            tien = f"{int(tt):,}" if isinstance(tt, (int, float)) else (tt or "")
            print(f"{ngay.strftime('%d/%m')} | {ma or '':10} | {nd or ''}  [{tien}]")
    print("-" * 72)
    print(f"Tổng {n} dòng. Bóc thành JSON rồi chạy: python tools/chi_phi_nvl.py tinh --json <file>")


def tinh(data):
    thang = data.get("thang", "?")
    sl = {k: float(data.get(k, 0) or 0) for k in ["bo", "co", "tay", "cap", "gau", "kg"]}
    print(f"=== CHI PHÍ NVL THÁNG {thang} ===")
    print(f"Đơn giá gộp sợi+nhuộm+dớ = {GIA_KG:,} đ/kg\n")
    tong_kg = 0.0
    tong_tien = 0.0
    print(f"{'Nhóm':18}{'Số lượng':>12}{'Khối lượng':>14}{'Chi phí':>16}")
    for k in ["bo", "co", "tay", "cap", "gau", "kg"]:
        q = sl[k]
        kg = q if k == "kg" else q * KG[k]
        tien = kg * GIA_KG
        tong_kg += kg
        tong_tien += tien
        if q:
            print(f"{TEN[k]:18}{q:>12,.0f}{kg:>13,.1f}kg{tien:>15,.0f}đ")
    print("-" * 60)
    print(f"{'TỔNG':18}{'':>12}{tong_kg:>13,.1f}kg{tong_tien:>15,.0f}đ")
    print(f"\n=> Chi phí nguyên liệu (sợi+nhuộm+dớ) tháng {thang} ≈ {tong_tien:,.0f} đ")
    print("   (chưa gồm nhân công, điện, hao mòn máy, vận chuyển, lặt vặt)")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("liet-ke")
    p1.add_argument("--thang", type=int, required=True)
    p1.add_argument("--nam", type=int, default=2026)
    p2 = sub.add_parser("tinh")
    p2.add_argument("--json", required=True)
    a = ap.parse_args()
    if a.cmd == "liet-ke":
        liet_ke(a.thang, a.nam)
    else:
        with open(a.json, encoding="utf-8") as f:
            tinh(json.load(f))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
