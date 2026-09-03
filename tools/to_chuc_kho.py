# -*- coding: utf-8 -*-
"""
to_chuc_kho.py — Tổ chức kho footage content type-first cho Xưởng Bo Đức Lan.

Phỏng theo SOP raw/Content/3-skill-claude-code/.../quy-trinh-xu-ly-file.md
(dự án caravan của anh Long), nhưng RÚT GỌN + ĐỔI TÊN cho xưởng Bo:
  - 1 nguồn iPhone (source = "iphone"), không GPS/track, không caravan.
  - Cấu trúc type-first: photo/ video/ audio/ tracklog/ index/ + ban-nhe/.
  - Bản nhẹ để trong ban-nhe/ (KHÔNG để raw/ vì raw/ bất biến theo CLAUDE.md).

Chạy lại luôn an toàn (idempotent): đã có + hash khớp thì skip.
KHÔNG xoá nguồn. Chưa "✅ VERIFY ĐỦ" thì chưa an toàn.

    python tools/to_chuc_kho.py --from "C:\\Users\\admin\\iphone-tam"
    python tools/to_chuc_kho.py --from ... --dry-run
    python tools/to_chuc_kho.py --from ... --no-ban-nhe
"""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, sys, datetime as dt
from pathlib import Path

# ---- cấu hình mặc định ----
DEFAULT_DRIVE = r"C:\Users\admin\footage-content"
ROOT_NAME = "2026-content-xuong-bo"   # thay cho 2026-Hanoi2Paris
SOURCE = "iphone"                     # thay cho iphone-long
DEFAULT_FROM = r"C:\Users\admin\iphone-tam"

PHOTO_EXT = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".tif", ".tiff", ".dng"}
VIDEO_EXT = {".mov", ".mp4", ".m4v", ".avi", ".hevc"}
AUDIO_EXT = {".wav", ".m4a", ".mp3", ".aac"}
SKIP_EXT  = {".lrf", ".lrv", ".thm", ".xmp", ".aae"}

def sha256(p: Path, buf=1 << 20) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            b = f.read(buf)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def loai_file(p: Path) -> str | None:
    e = p.suffix.lower()
    if e in PHOTO_EXT: return "photo"
    if e in VIDEO_EXT: return "video"
    if e in AUDIO_EXT: return "audio"
    return None

def mtime_ngay(p: Path) -> str:
    return dt.datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d")

def map_ngay(files: list[Path]) -> dict[str, str]:
    """Đọc ngày cho CẢ danh sách trong 1 lần gọi exiftool (nhanh hơn gọi từng file).
    Ưu tiên DateTimeOriginal > CreateDate > FileModifyDate, fallback mtime."""
    kq: dict[str, str] = {}
    try:
        out = subprocess.run(
            ["exiftool", "-json", "-d", "%Y-%m-%d",
             "-DateTimeOriginal", "-CreateDate", "-FileModifyDate",
             *[str(p) for p in files]],
            capture_output=True, text=True, timeout=900)
        for rec in json.loads(out.stdout or "[]"):
            src = Path(rec.get("SourceFile", "")).name
            ngay = (rec.get("DateTimeOriginal") or rec.get("CreateDate")
                    or rec.get("FileModifyDate") or "")
            ngay = str(ngay)[:10]
            if len(ngay) == 10 and ngay[4] == "-":
                kq[src] = ngay
    except Exception as e:
        print(f"   ⚠ exiftool batch lỗi ({e}) → dùng mtime")
    for p in files:
        kq.setdefault(p.name, mtime_ngay(p))
    return kq

def human(n: int) -> str:
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.1f}{u}" if u != "B" else f"{n}{u}"
        n /= 1024

def contact_sheet(src: Path, dest: Path) -> bool:
    """Contact sheet 5x4 (20 khung) cho 1 video."""
    try:
        pr = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nk=1:nw=1", str(src)],
            capture_output=True, text=True, timeout=120)
        dur = float(pr.stdout.strip() or "0")
    except Exception:
        dur = 0
    if dur <= 0:
        return False
    interval = max(dur / 20.0, 0.001)
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
           "-frames:v", "1", "-q:v", "3",
           "-vf", f"fps=1/{interval:.6f},scale=480:-1,tile=5x4", str(dest)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    return dest.exists() and dest.stat().st_size > 0

def resize_anh(src: Path, dest: Path, cap=2000) -> bool:
    from PIL import Image, ImageOps
    try:
        img = Image.open(src)
        exif = img.info.get("exif")
        img = ImageOps.exif_transpose(img)
        img.thumbnail((cap, cap), Image.LANCZOS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        if exif:
            img.save(dest, "JPEG", quality=85, exif=exif)
        else:
            img.save(dest, "JPEG", quality=85)
        return True
    except Exception as e:
        print(f"      ⚠ resize lỗi {src.name}: {e}")
        return False

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="src", default=DEFAULT_FROM)
    ap.add_argument("--drive", default=DEFAULT_DRIVE)
    ap.add_argument("--root-name", default=ROOT_NAME)
    ap.add_argument("--source", default=SOURCE)
    ap.add_argument("--no-ban-nhe", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    src_dir = Path(a.src)
    root = Path(a.drive) / a.root_name
    print("=" * 64)
    print(" TỔ CHỨC KHO CONTENT type-first — Xưởng Bo Đức Lan")
    print("=" * 64)
    print(" LUẬT: chưa '✅ VERIFY ĐỦ' thì chưa an toàn · KHÔNG xoá nguồn.\n")
    print(f"Nguồn : {src_dir}")
    print(f"Kho   : {root}")
    print(f"Source: {a.source}   Bản nhẹ: {'KHÔNG' if a.no_ban_nhe else 'CÓ'}"
          f"{'   [DRY-RUN]' if a.dry_run else ''}")

    if not src_dir.is_dir():
        print(f"\n❌ Nguồn không tồn tại: {src_dir}")
        return 1

    files = [p for p in sorted(src_dir.iterdir())
             if p.is_file() and p.suffix.lower() not in SKIP_EXT and loai_file(p)]
    if not files:
        print("\n❌ Không thấy file ảnh/video/audio nào trong nguồn.")
        return 1

    tong = sum(p.stat().st_size for p in files)
    print(f"Tìm thấy {len(files)} file · {human(tong)}")
    print("   (đọc ngày EXIF hàng loạt...)")
    ngay_map = map_ngay(files)
    print("-" * 64)

    # tạo khung thư mục (kể cả audio/ tracklog/ trống — bám sát sơ đồ SOP)
    for sub in ("photo", "video", "audio", "tracklog", "index"):
        (root / sub).mkdir(parents=True, exist_ok=True) if not a.dry_run else None

    ok = 0
    ngay_da_cham: set[str] = set()
    for p in files:
        typ = loai_file(p)
        ngay = ngay_map.get(p.name) or mtime_ngay(p)
        ngay_da_cham.add(ngay)
        dest = root / typ / ngay / a.source / p.name
        size = p.stat().st_size
        if a.dry_run:
            print(f"   • {p.name:32.32} {human(size):>9}  → {typ}/{ngay}/{a.source}/")
            ok += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and dest.stat().st_size == size and sha256(dest) == sha256(p):
            print(f"   ✅ {p.name:32.32} {human(size):>9}  đã có, hash khớp")
            ok += 1
            continue
        shutil.copy2(p, dest)
        if sha256(dest) == sha256(p):
            print(f"   ✅ {p.name:32.32} {human(size):>9}  hash khớp")
            ok += 1
        else:
            print(f"   ❌ {p.name:32.32} {human(size):>9}  HASH LỆCH")

    if a.dry_run:
        print("\n[DRY-RUN] Không ghi gì. Bỏ --dry-run để chạy thật.")
        return 0

    # index EXIF cho từng ngày
    print("-" * 64)
    for ngay in sorted(ngay_da_cham):
        muc = []
        for typ in ("photo", "video", "audio"):
            d = root / typ / ngay / a.source
            if d.is_dir():
                muc += [str(x) for x in d.iterdir() if x.is_file()]
        if not muc:
            continue
        idx = root / "index" / f"{ngay}.json"
        try:
            r = subprocess.run(["exiftool", "-json", "-g", *muc],
                               capture_output=True, text=True, timeout=300)
            idx.write_text(r.stdout, encoding="utf-8")
            print(f"   📄 index/{ngay}.json  ({len(muc)} file)")
        except Exception as e:
            print(f"   ⚠ index {ngay} lỗi: {e}")

    # bản nhẹ
    if not a.no_ban_nhe:
        print("-" * 64)
        print("   Bản nhẹ:")
        for ngay in sorted(ngay_da_cham):
            # ảnh resize
            pdir = root / "photo" / ngay / a.source
            if pdir.is_dir():
                for x in sorted(pdir.iterdir()):
                    if x.is_file() and loai_file(x) == "photo":
                        out = root / "ban-nhe" / ngay / a.source / (x.stem + ".jpg")
                        if out.exists():
                            continue
                        if resize_anh(x, out):
                            print(f"      🖼  {out.name}")
            # contact sheet video
            vdir = root / "video" / ngay / a.source
            if vdir.is_dir():
                for x in sorted(vdir.iterdir()):
                    if x.is_file() and loai_file(x) == "video":
                        out = root / "ban-nhe" / ngay / "_contact" / (x.stem + ".jpg")
                        if out.exists():
                            continue
                        if contact_sheet(x, out):
                            print(f"      🎞  _contact/{out.name}")
                        else:
                            print(f"      ⚠ contact sheet lỗi: {x.name}")

    # verify: đếm nguồn vs kho
    print("=" * 64)
    dem_kho = 0
    for typ in ("photo", "video", "audio"):
        for d in (root / typ).rglob("*"):
            if d.is_file():
                dem_kho += 1
    print(f"Nguồn: {len(files)} file · Kho type-first: {dem_kho} file · Copy/verify OK: {ok}/{len(files)}")
    if ok == len(files):
        print("✅ VERIFY ĐỦ — footage đã tổ chức an toàn trong kho type-first.")
        print("⚠ Chưa có backup #2 → GIỮ NGUYÊN footage trên iPhone (bản thứ hai).")
    else:
        print("❌ CÓ LỖI — kiểm lại, KHÔNG format/xoá nguồn.")
        return 1
    print("=" * 64)
    return 0

if __name__ == "__main__":
    sys.exit(main())
