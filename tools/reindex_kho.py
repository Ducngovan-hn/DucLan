# -*- coding: utf-8 -*-
"""
reindex_kho.py — Reindex EXIF cho MỌI ngày trong 1 kho type-first, đồng bộ với
file thực tế: ngày nào còn file thì viết lại index/<ngày>.json (bỏ mục đã chuyển
đi), ngày nào hết file thì xoá index đó. Cũng đảm bảo khung thư mục đầy đủ.

    python tools/reindex_kho.py --kho "C:\\Users\\admin\\footage-content\\2026-content-xuong-bo"
    python tools/reindex_kho.py --kho "C:\\Users\\admin\\my-life"
"""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

TYPES = ("photo", "video", "audio")

def reindex_ngay(kho: Path, ngay: str) -> int:
    muc = []
    for typ in TYPES:
        d = kho / typ / ngay / "iphone"
        if d.is_dir():
            muc += [str(x) for x in d.iterdir() if x.is_file()]
    idx = kho / "index" / f"{ngay}.json"
    if not muc:
        if idx.exists():
            idx.unlink()
            print(f"   🗑  bỏ index/{ngay}.json (không còn file)")
        return 0
    idx.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["exiftool", "-json", "-g", *muc],
                       capture_output=True, text=True, timeout=600)
    idx.write_text(r.stdout, encoding="utf-8")
    print(f"   📄 index/{ngay}.json  ({len(muc)} file)")
    return len(muc)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kho", required=True)
    a = ap.parse_args()
    kho = Path(a.kho)
    if not kho.is_dir():
        print(f"❌ Không thấy {kho}")
        return 1

    # khung thư mục đầy đủ (như kho xưởng)
    for sub in ("photo", "video", "audio", "tracklog", "index"):
        (kho / sub).mkdir(parents=True, exist_ok=True)

    # tập ngày = mọi thư mục con ngày trong photo/ video/ audio/
    ngays = set()
    for typ in TYPES:
        d = kho / typ
        if d.is_dir():
            ngays |= {x.name for x in d.iterdir() if x.is_dir()}
    # + ngày đang có index (để xoá nếu đã rỗng)
    idxd = kho / "index"
    if idxd.is_dir():
        ngays |= {x.stem for x in idxd.glob("*.json")}

    print("=" * 60)
    print(f" REINDEX — {kho.name}  ({len(ngays)} ngày)")
    print("=" * 60)
    tong = 0
    for ngay in sorted(ngays):
        tong += reindex_ngay(kho, ngay)
    print("-" * 60)
    print(f"Xong. Tổng file được index: {tong}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
