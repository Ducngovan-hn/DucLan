#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
offload_content.py — Cất footage content Xưởng Bo Đức Lan (Windows, 1 nguồn iPhone 11 Pro Max)

Bản gọn của offload_day.py (file mẫu, macOS/8 máy) cho nhu cầu: mỗi ngày quay
vài clip bằng iPhone -> chép về kho theo ngày -> VERIFY hash -> (tuỳ chọn) backup #2.

QUY TRÌNH LẤY FOOTAGE TỪ iPHONE (Windows):
  iPhone không hiện ra ổ đĩa (nó là thiết bị MTP). Cách chắc ăn:
    1. Cắm iPhone bằng cáp (cần cài "Apple Devices" hoặc iTunes để Windows nhận).
    2. Mở File Explorer -> "Apple iPhone" -> Internal Storage -> DCIM.
    3. Kéo các clip/ảnh quay HÔM NAY vào một thư mục tạm, ví dụ:  C:\\Users\\admin\\iphone-tam\\
    4. Chạy lệnh này với --from trỏ vào thư mục tạm đó.
  (iCloud Photos đồng bộ về một thư mục cũng dùng làm --from được.)

BA LUẬT THÉP (in nhắc mỗi lần chạy):
  1. Chưa thấy "✅ VERIFY ĐỦ" thì chưa được nói "an toàn".
  2. Chưa có backup #2 thì KHÔNG xoá footage khỏi iPhone. (Script này KHÔNG BAO GIỜ xoá nguồn.)
  3. Số liệu kiểm kê lấy từ log này, không từ trí nhớ.

Ví dụ:
  # Xem trước, không đụng file:
  python tools/offload_content.py --from C:\\Users\\admin\\iphone-tam --dry-run
  # Chép thật vào kho mặc định:
  python tools/offload_content.py --from C:\\Users\\admin\\iphone-tam
  # Có ổ backup #2 (khi anh Đức mua ổ):
  python tools/offload_content.py --from C:\\Users\\admin\\iphone-tam --backup2 E:\\footage-backup
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

# ---- Cấu hình mặc định ------------------------------------------------------
CONFIG_PATH = Path(__file__).with_name(".offload_config.json")
DEFAULT_DRIVE = r"C:\Users\admin\footage-content"   # kho footage (ngoài repo git)
VIDEO_EXT = {".mov", ".mp4", ".m4v", ".hevc"}
IMAGE_EXT = {".jpg", ".jpeg", ".heic", ".png", ".dng", ".aae"}
MEDIA_EXT = VIDEO_EXT | IMAGE_EXT


def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_config(cfg: dict) -> None:
    try:
        CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def sha256_of(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def day_of(path: Path) -> str:
    """Ngày quay -> nhãn thư mục YYYY-MM-DD, lấy từ thời gian sửa file (mtime)."""
    ts = path.stat().st_mtime
    return dt.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def scan_sources(sources: list[Path]) -> list[Path]:
    files: list[Path] = []
    for src in sources:
        if not src.exists():
            print(f"  ⚠ Bỏ qua (không thấy): {src}")
            continue
        for p in sorted(src.rglob("*")):
            if p.is_file() and p.suffix.lower() in MEDIA_EXT:
                files.append(p)
    return files


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


def copy_verify(src: Path, dst: Path, dry: bool) -> tuple[bool, str]:
    """Chép + verify hash. Trả (ok, ghi_chú)."""
    if dst.exists() and dst.stat().st_size == src.stat().st_size:
        # Đã có -> vẫn verify hash để chắc.
        if not dry and sha256_of(src) == sha256_of(dst):
            return True, "đã có, hash khớp"
    if dry:
        return True, "[dry-run] sẽ chép"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    ok = sha256_of(src) == sha256_of(dst)
    return ok, ("hash khớp" if ok else "❌ HASH LỆCH")


def main() -> int:
    cfg = load_config()
    ap = argparse.ArgumentParser(description="Cất footage content iPhone -> kho + verify + backup#2")
    ap.add_argument("--from", dest="sources", action="append", default=[],
                    help="Thư mục nguồn (clip iPhone đã kéo ra). Cho nhiều lần --from.")
    ap.add_argument("--drive", default=cfg.get("drive", DEFAULT_DRIVE),
                    help=f"Kho footage đích (mặc định {cfg.get('drive', DEFAULT_DRIVE)})")
    ap.add_argument("--backup2", default=cfg.get("backup2"),
                    help="Ổ/thư mục backup #2 (khi anh Đức đã mua ổ). Bỏ trống = chưa backup.")
    ap.add_argument("--dry-run", action="store_true", help="Chỉ in ra, không đụng file.")
    args = ap.parse_args()

    print("=" * 64)
    print(" CẤT FOOTAGE CONTENT — Xưởng Bo Đức Lan")
    print("=" * 64)
    print(" LUẬT: chưa '✅ VERIFY ĐỦ' thì chưa an toàn · script KHÔNG xoá nguồn.")
    print()

    if not args.sources:
        print("❌ Thiếu --from <thư mục nguồn>. Xem hướng dẫn lấy footage iPhone ở đầu file.")
        return 2

    sources = [Path(s) for s in args.sources]
    drive = Path(args.drive)
    backup2 = Path(args.backup2) if args.backup2 else None

    files = scan_sources(sources)
    if not files:
        print("⚠ Không thấy file media nào trong nguồn. (Đã kéo clip hôm nay ra thư mục tạm chưa?)")
        return 1

    # Gom theo ngày
    by_day: dict[str, list[Path]] = {}
    for f in files:
        by_day.setdefault(day_of(f), []).append(f)

    total = len(files)
    total_size = sum(f.stat().st_size for f in files)
    print(f"Nguồn: {', '.join(str(s) for s in sources)}")
    print(f"Đích : {drive}")
    print(f"Backup#2: {backup2 if backup2 else '⚠ CHƯA CÓ — iPhone giữ nguyên làm bản 2'}")
    print(f"Tìm thấy {total} file · {human(total_size)} · {len(by_day)} ngày")
    print("-" * 64)

    ok_count = 0
    fail: list[str] = []
    log = {"chay_luc": dt.datetime.now().isoformat(timespec="seconds"),
           "nguon": [str(s) for s in sources], "dich": str(drive),
           "backup2": str(backup2) if backup2 else None,
           "dry_run": args.dry_run, "ngay": {}}

    for day, day_files in sorted(by_day.items()):
        print(f"\n📅 {day} — {len(day_files)} file")
        day_log = {"so_file": len(day_files), "video": 0, "anh": 0, "loi": []}
        for src in day_files:
            dst = drive / day / src.name
            ok, note = copy_verify(src, dst, args.dry_run)
            kind = "video" if src.suffix.lower() in VIDEO_EXT else "anh"
            day_log["video" if kind == "video" else "anh"] += 1
            mark = "✅" if ok else "❌"
            print(f"   {mark} {src.name:40} {human(src.stat().st_size):>8}  {note}")
            if ok:
                ok_count += 1
                # backup #2
                if backup2 and not args.dry_run:
                    b_ok, b_note = copy_verify(src, backup2 / day / src.name, False)
                    if not b_ok:
                        fail.append(f"{src.name} (backup2: {b_note})")
                        day_log["loi"].append(f"{src.name}: backup2 {b_note}")
            else:
                fail.append(f"{src.name} ({note})")
                day_log["loi"].append(f"{src.name}: {note}")
        log["ngay"][day] = day_log

        # Ghi log cạnh footage của ngày
        if not args.dry_run:
            logdir = drive / day
            logdir.mkdir(parents=True, exist_ok=True)
            (logdir / "_offload-log.json").write_text(
                json.dumps({"ngay": day, **day_log,
                            "chay_luc": log["chay_luc"], "backup2": log["backup2"]},
                           ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n" + "=" * 64)
    print(f"Chép/verify OK: {ok_count}/{total}")
    if fail:
        print(f"❌ CÓ LỖI ({len(fail)}): " + "; ".join(fail[:8]))
        print("   -> KHÔNG xoá footage khỏi iPhone. Kiểm cáp, chạy lại.")
        result = 1
    elif args.dry_run:
        print("🔎 [DRY-RUN] Không đụng file. Bỏ --dry-run để chép thật.")
        result = 0
    else:
        print("✅ VERIFY ĐỦ — footage đã an toàn trong kho.")
        if not backup2:
            print("⚠ CHƯA CÓ backup #2 → GIỮ NGUYÊN footage trên iPhone (đó là bản thứ hai).")
        result = 0
    print("=" * 64)

    # Nhớ cấu hình lần cuối
    if not args.dry_run:
        cfg["drive"] = str(drive)
        if backup2:
            cfg["backup2"] = str(backup2)
        save_config(cfg)

    return result


if __name__ == "__main__":
    sys.exit(main())
