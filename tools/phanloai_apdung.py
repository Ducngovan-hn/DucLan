# -*- coding: utf-8 -*-
"""
phanloai_apdung.py — Di chuyển file theo quyết định phân loại của Claude.

Đọc, cho mỗi ngày, trong <tu>/_phanloai/<ngày>/:
    map.json          (do phanloai_montage.py sinh: [{o,ten,loai,full,nhe},...])
    quyet-dinh.json   (do Claude ghi: {"xuong":[3,7,...], "khong_chac":[...]})

Quy tắc AN TOÀN: CHỈ nhóm "xuong" (chắc chắn) mới nằm ở kho xưởng; mọi thứ khác
ở/ về my-life.
  - Luồng thường (--nhom xuong):  move các ô "xuong"      từ my-life → kho xưởng.
  - Hồi tố       (--nhom con-lai): move các ô KHÔNG "xuong" từ kho xưởng → my-life.

Move cả full-res + bản nhẹ. Sau đó reindex ngày đó ở CẢ hai kho. Verify tổng số
file bảo toàn. KHÔNG xoá nguồn gốc trên iPhone.

    python tools/phanloai_apdung.py --tu <khoXuong> --den <myLife> --nhom con-lai
    python tools/phanloai_apdung.py --tu <myLife> --den <khoXuong> --nhom xuong
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys
from pathlib import Path

def dem_file(kho: Path) -> int:
    n = 0
    for typ in ("photo", "video", "audio"):
        d = kho / typ
        if d.is_dir():
            n += sum(1 for x in d.rglob("*") if x.is_file())
    return n

def reindex(kho: Path, ngay: str):
    muc = []
    for typ in ("photo", "video", "audio"):
        d = kho / typ / ngay / "iphone"
        if d.is_dir():
            muc += [str(x) for x in d.iterdir() if x.is_file()]
    idx = kho / "index" / f"{ngay}.json"
    if not muc:
        if idx.exists():
            idx.unlink()   # ngày không còn file ở kho này → bỏ index
        return
    idx.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(["exiftool", "-json", "-g", *muc],
                           capture_output=True, text=True, timeout=300)
        idx.write_text(r.stdout, encoding="utf-8")
    except Exception as e:
        print(f"   ⚠ reindex {kho.name}/{ngay} lỗi: {e}")

def move_mot(m: dict, tu: Path, den: Path, ngay: str) -> int:
    """Move full-res + bản nhẹ của 1 mục từ tu→den. Trả số file đã move."""
    dem = 0
    sub = "photo" if m["loai"] == "photo" else "video"
    # full-res
    full = Path(m["full"]) if m["full"] else None
    if full and full.exists():
        dst = den / sub / ngay / "iphone" / full.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(full), str(dst))
        dem += 1
    # bản nhẹ
    nhe = Path(m["nhe"])
    if nhe.exists():
        if m["loai"] == "photo":
            dst = den / "ban-nhe" / ngay / "iphone" / nhe.name
        else:
            dst = den / "ban-nhe" / ngay / "_contact" / nhe.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(nhe), str(dst))
    return dem

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tu", required=True, help="Kho nguồn (đang chứa file + _phanloai)")
    ap.add_argument("--den", required=True, help="Kho đích")
    ap.add_argument("--nhom", choices=["xuong", "con-lai"], required=True)
    ap.add_argument("--ngay", help="Chỉ 1 ngày (bỏ trống = mọi ngày có quyet-dinh)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    tu, den = Path(a.tu), Path(a.den)
    pl = tu / "_phanloai"
    if not pl.is_dir():
        print(f"❌ Không thấy {pl} (chạy phanloai_montage trước)")
        return 1

    ngays = [a.ngay] if a.ngay else sorted(
        d.name for d in pl.iterdir()
        if d.is_dir() and (d / "quyet-dinh.json").exists())
    if not ngays:
        print("❌ Chưa có ngày nào có quyet-dinh.json.")
        return 1

    print("=" * 60)
    print(f" ÁP DỤNG PHÂN LOẠI · nhóm={a.nhom} · {tu.name} → {den.name}"
          f"{'  [DRY-RUN]' if a.dry_run else ''}")
    print("=" * 60)
    truoc = dem_file(tu) + dem_file(den)

    tong_move = 0
    ngay_cham = set()
    for ngay in ngays:
        d = pl / ngay
        muc = json.loads((d / "map.json").read_text(encoding="utf-8"))
        qd = json.loads((d / "quyet-dinh.json").read_text(encoding="utf-8"))
        xuong = set(qd.get("xuong", []))
        if a.nhom == "xuong":
            can_move = [m for m in muc if m["o"] in xuong]
        else:  # con-lai = mọi thứ KHÔNG chắc chắn là xưởng
            can_move = [m for m in muc if m["o"] not in xuong]
        if not can_move:
            print(f"   • {ngay}: không có mục nào cần chuyển.")
            continue
        if a.dry_run:
            print(f"   • {ngay}: sẽ chuyển {len(can_move)} mục "
                  f"({sum(1 for m in can_move if m['loai']=='photo')} ảnh / "
                  f"{sum(1 for m in can_move if m['loai']=='video')} video)")
            continue
        d_move = 0
        for m in can_move:
            d_move += move_mot(m, tu, den, ngay)
        tong_move += d_move
        ngay_cham.add(ngay)
        print(f"   ✅ {ngay}: chuyển {len(can_move)} mục ({d_move} file full-res)")

    if a.dry_run:
        print("\n[DRY-RUN] Không di chuyển gì.")
        return 0

    # reindex 2 kho cho các ngày đã đụng
    for ngay in sorted(ngay_cham):
        reindex(tu, ngay)
        reindex(den, ngay)

    sau = dem_file(tu) + dem_file(den)
    print("-" * 60)
    print(f"Đã chuyển {tong_move} file full-res · tổng file trước={truoc} sau={sau}")
    if truoc == sau:
        print("✅ VERIFY ĐỦ — không mất/không nhân đôi file. Reindex xong 2 kho.")
    else:
        print("❌ LỆCH SỐ FILE — kiểm lại ngay, KHÔNG xoá nguồn iPhone.")
        return 1
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
