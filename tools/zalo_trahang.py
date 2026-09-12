#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Đếm khách trả hàng từ file dump Zalo — KHÔNG đếm bằng mắt, tránh sót.

Cách hoạt động: mỗi đơn trong nhóm "Trả hàng" luôn mở đầu bằng dòng
    "<ngày>/<tháng>: trả <tên khách>"
(ví dụ "12/9: trả cty Bform:"). Công cụ quét TOÀN BỘ file theo tiền tố này —
không phụ thuộc nhãn tương đối "Hôm nay"/"Hôm qua" và không cắt bớt dòng nào —
nên không bỏ sót đơn ở đầu khối.

Dùng:
    python tools/zalo_trahang.py <file_dump.txt> --ngay 12/9
In ra: từng đơn (tên · tiền), SỐ KHÁCH (gom theo tên), tổng tiền.
"""
import argparse
import re
import sys
from pathlib import Path

# Dòng mở đầu một đơn: "12/9: trả cty Bform:"  /  "9/9: trả a Tuân"
RE_DON = re.compile(r"^\s*(\d{1,2})\s*/\s*(\d{1,2})\s*:\s*trả\s+(.+?)\s*:?\s*$", re.IGNORECASE)
# Số tiền: chuỗi dạng 1.234.567 (>= 4 chữ số kể cả dấu chấm)
RE_TIEN = re.compile(r"(\d{1,3}(?:\.\d{3})+)")


def doc_don(noi_dung: str, ngay: int, thang: int):
    """Trả về list đơn [(ten, tien)] của đúng ngày/tháng."""
    dong = noi_dung.splitlines()
    dons = []
    i = 0
    while i < len(dong):
        m = RE_DON.match(dong[i])
        if not m:
            i += 1
            continue
        d, thg, ten = int(m.group(1)), int(m.group(2)), m.group(3).strip()
        # Gom các dòng tới trước đơn kế tiếp để tìm số tiền lớn nhất (thường là "Tổng"/"=")
        j = i + 1
        tien_max = 0
        while j < len(dong) and not RE_DON.match(dong[j]):
            for s in RE_TIEN.findall(dong[j]):
                val = int(s.replace(".", ""))
                if val > tien_max:
                    tien_max = val
            j += 1
        if d == ngay and thg == thang:
            dons.append((ten, tien_max))
        i = j
    return dons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="File dump Zalo (từ zalo_dump.mjs)")
    ap.add_argument("--ngay", required=True, help="Ngày cần đếm, dạng d/m (vd 12/9)")
    args = ap.parse_args()

    p = Path(args.file)
    if not p.exists():
        sys.exit(f"Không thấy file: {p}")
    try:
        ngay_s, thang_s = args.ngay.replace(" ", "").split("/")
        ngay, thang = int(ngay_s), int(thang_s)
    except ValueError:
        sys.exit("--ngay phải dạng d/m, ví dụ 12/9")

    dons = doc_don(p.read_text(encoding="utf-8"), ngay, thang)
    if not dons:
        print(f"📦 Ngày {ngay}/{thang}: KHÔNG có đơn trả hàng nào trong file.")
        return

    # Gom theo tên khách (một khách có thể nhiều đơn)
    from collections import OrderedDict
    theo_khach = OrderedDict()
    for ten, tien in dons:
        theo_khach.setdefault(ten, []).append(tien)

    print(f"📦 KHÁCH TRẢ HÀNG ngày {ngay}/{thang}: {len(theo_khach)} khách · {len(dons)} đơn")
    tong = 0
    for ten, ds in theo_khach.items():
        for t in ds:
            tong += t
        chi_tiet = " + ".join(f"{t:,.0f}".replace(",", ".") for t in ds)
        print(f"   • {ten}: {chi_tiet} đ")
    print(f"   ─────────────")
    print(f"   TỔNG hàng trả: {tong:,.0f}".replace(",", ".") + " đ")
    print(f"\n→ SỐ KHÁCH = {len(theo_khach)} (con số máy đếm, không đếm tay)")


if __name__ == "__main__":
    main()
