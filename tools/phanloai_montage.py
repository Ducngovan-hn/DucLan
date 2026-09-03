# -*- coding: utf-8 -*-
"""
phanloai_montage.py — Gộp bản nhẹ mỗi ngày thành LƯỚI ẢNH ĐÁNH SỐ để Claude
phân loại xưởng-bo / cá-nhân bằng ÍT token (đọc 1 lưới thay vì từng ảnh).

Đọc bản nhẹ có sẵn trong 1 kho (my-life hoặc kho xưởng):
    <kho>/ban-nhe/<ngày>/iphone/*.jpg     (ảnh resize)
    <kho>/ban-nhe/<ngày>/_contact/*.jpg   (contact sheet video)
Mỗi mục thành 1 ô 300px, đánh số + tên file, ghép lưới 5 cột (25 ô/tấm).
Xuất:
    <kho>/_phanloai/<ngày>/grid-NN.jpg
    <kho>/_phanloai/<ngày>/map.json   [{o, ten, loai, full, nhe}]

    python tools/phanloai_montage.py --kho "C:\\Users\\admin\\footage-content\\2026-content-xuong-bo"
    python tools/phanloai_montage.py --kho ... --ngay 2026-08-30
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

COLS = 5
CELL = 300
PAD = 6
HDR = 26          # dải nhãn số + tên phía trên mỗi ô
PER_SHEET = 25    # 5x5 ô mỗi tấm

def _font(sz: int):
    for fp in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        try:
            return ImageFont.truetype(fp, sz)
        except Exception:
            pass
    return ImageFont.load_default()

def full_tuong_ung(kho: Path, ngay: str, stem: str, loai: str) -> Path | None:
    """Tìm file full-res ứng với 1 bản nhẹ (theo stem, mọi đuôi)."""
    sub = "photo" if loai == "photo" else "video"
    d = kho / sub / ngay / "iphone"
    if d.is_dir():
        for x in d.iterdir():
            if x.is_file() and x.stem == stem:
                return x
    return None

def liet_ke_muc(kho: Path, ngay: str) -> list[dict]:
    """Danh sách mục (ảnh + video) của 1 ngày, kèm đường full-res + bản nhẹ."""
    muc = []
    pdir = kho / "ban-nhe" / ngay / "iphone"
    if pdir.is_dir():
        for x in sorted(pdir.iterdir()):
            if x.is_file() and x.suffix.lower() == ".jpg":
                full = full_tuong_ung(kho, ngay, x.stem, "photo")
                muc.append({"ten": x.stem, "loai": "photo",
                            "nhe": str(x), "full": str(full) if full else ""})
    cdir = kho / "ban-nhe" / ngay / "_contact"
    if cdir.is_dir():
        for x in sorted(cdir.iterdir()):
            if x.is_file() and x.suffix.lower() == ".jpg":
                full = full_tuong_ung(kho, ngay, x.stem, "video")
                muc.append({"ten": x.stem, "loai": "video",
                            "nhe": str(x), "full": str(full) if full else ""})
    return muc

def ve_o(canvas: Image.Image, draw: ImageDraw.ImageDraw, col: int, row: int,
         so: int, m: dict, f_num, f_name):
    x0 = col * (CELL + PAD)
    y0 = row * (CELL + HDR + PAD)
    # dải nhãn
    nhan = f"{so}  {m['ten']}" + ("  [V]" if m["loai"] == "video" else "")
    draw.rectangle([x0, y0, x0 + CELL, y0 + HDR], fill=(20, 20, 20))
    draw.text((x0 + 4, y0 + 3), nhan, fill=(255, 235, 120), font=f_name)
    # ảnh thu nhỏ vào ô
    try:
        im = Image.open(m["nhe"]).convert("RGB")
        im.thumbnail((CELL, CELL), Image.LANCZOS)
        ox = x0 + (CELL - im.width) // 2
        oy = y0 + HDR + (CELL - im.height) // 2
        canvas.paste(im, (ox, oy))
    except Exception:
        draw.rectangle([x0, y0 + HDR, x0 + CELL, y0 + HDR + CELL], fill=(60, 60, 60))
    # số lớn góc trái để đọc chắc
    draw.text((x0 + 4, y0 + HDR + 2), str(so), fill=(255, 60, 60), font=f_num)

def lam_ngay(kho: Path, ngay: str) -> int:
    muc = liet_ke_muc(kho, ngay)
    if not muc:
        return 0
    out_dir = kho / "_phanloai" / ngay
    out_dir.mkdir(parents=True, exist_ok=True)
    # map.json (đánh số 1..N toàn ngày)
    for i, m in enumerate(muc, 1):
        m["o"] = i
    (out_dir / "map.json").write_text(
        json.dumps(muc, ensure_ascii=False, indent=1), encoding="utf-8")

    f_num = _font(30)
    f_name = _font(15)
    so_tam = 0
    for start in range(0, len(muc), PER_SHEET):
        phần = muc[start:start + PER_SHEET]
        rows = (len(phần) + COLS - 1) // COLS
        W = COLS * (CELL + PAD)
        H = rows * (CELL + HDR + PAD)
        canvas = Image.new("RGB", (W, H), (245, 245, 245))
        draw = ImageDraw.Draw(canvas)
        for j, m in enumerate(phần):
            ve_o(canvas, draw, j % COLS, j // COLS, m["o"], m, f_num, f_name)
        so_tam += 1
        canvas.save(out_dir / f"grid-{so_tam:02d}.jpg", "JPEG", quality=80)
    print(f"   🧩 {ngay}: {len(muc)} mục → {so_tam} lưới  ({out_dir})")
    return len(muc)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kho", required=True, help="Root kho có sẵn ban-nhe/")
    ap.add_argument("--ngay", help="Chỉ 1 ngày YYYY-MM-DD (bỏ trống = mọi ngày)")
    a = ap.parse_args()
    kho = Path(a.kho)
    bn = kho / "ban-nhe"
    if not bn.is_dir():
        print(f"❌ Không thấy {bn}")
        return 1
    if a.ngay:
        ngays = [a.ngay]
    else:
        ngays = sorted(d.name for d in bn.iterdir() if d.is_dir())
    print("=" * 60)
    print(f" TẠO LƯỚI PHÂN LOẠI — {kho.name}")
    print("=" * 60)
    tong = 0
    for ng in ngays:
        tong += lam_ngay(kho, ng)
    print("-" * 60)
    print(f"Xong: {len(ngays)} ngày · {tong} mục. Đọc lưới trong {kho / '_phanloai'}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
