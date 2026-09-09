#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
bao_cao_tuan.py — SỐ LIỆU BÁO CÁO TUẦN CHO "BỘ NÃO THỨ HAI"

Tự thu thập số liệu THẬT của hai tuần liền kề để so sánh sự tiến hoá của
vault (bộ não thứ hai): tuần này vs tuần trước. Script CHỈ đếm những gì
đếm được chắc chắn, và TRÍCH NGUYÊN VĂN các dòng liên quan tiền để LLM tự
đọc — KHÔNG tự cộng tiền, KHÔNG suy đoán (theo nguyên tắc vault).

Nguồn số liệu:
  - git log ............... số commit mỗi tuần + danh sách tiêu đề
  - wiki/log.md .......... số mục ingest / query / lint / update mỗi tuần
  - production/dmo/ ...... số ngày có DMO, % trung bình, ngày "tiền 0"
  - wiki/**/*.md ......... số trang wiki mới theo frontmatter `ngay_tao`

Cách chia tuần:
  --den YYYY-MM-DD  (mặc định: hôm nay)
  Tuần này  = [den-6 .. den]      (7 ngày, gồm cả 'den')
  Tuần trước = [den-13 .. den-7]  (7 ngày liền trước)

Dùng:
  python tools/bao_cao_tuan.py            # in bảng số liệu 2 tuần (người đọc)
  python tools/bao_cao_tuan.py --json     # xuất JSON (cho LLM viết đánh giá)
  python tools/bao_cao_tuan.py --den 2026-09-13
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

# ----- buộc stdout ra UTF-8 để tiếng Việt không lỗi trên Windows -----
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

VAULT = Path(__file__).resolve().parent.parent
DMO_DIR = VAULT / "production" / "dmo"
WIKI_DIR = VAULT / "wiki"
LOG_MD = WIKI_DIR / "log.md"

THU_VN = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]

RE_CHECKBOX = re.compile(r"^\s*[-*]\s*\[(?P<dau>[ xX])\]\s*.*$")
RE_LOG = re.compile(r"^##\s*\[(?P<ngay>\d{4}-\d{2}-\d{2})\]\s*(?P<loai>\w+)\s*\|")
RE_NGAY_TAO = re.compile(r"^ngay_tao:\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE)
# Dòng có khả năng nói về tiền trong file DMO (để trích nguyên văn cho LLM đọc).
RE_TIEN = re.compile(
    r"(doanh thu|thực nhận|tiền|trả hàng|6 lọ|chi phí|học phí|đồng|₫|\d[\d.]{2,}\s*(đ|tr|k)\b)",
    re.IGNORECASE,
)


# ============================ TIỆN ÍCH THỜI GIAN ============================
def parse_ngay(s: str | None) -> dt.date:
    if not s:
        return dt.date.today()
    try:
        return dt.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        sys.exit(f"Ngày không hợp lệ: {s!r} — cần YYYY-MM-DD")


def khoang_tuan(den: dt.date):
    """Trả về (tuan_nay, tuan_truoc) — mỗi cái là (dau, cuoi) gồm cả 2 mốc."""
    tuan_nay = (den - dt.timedelta(days=6), den)
    tuan_truoc = (den - dt.timedelta(days=13), den - dt.timedelta(days=7))
    return tuan_nay, tuan_truoc


def trong_khoang(ngay: dt.date, khoang) -> bool:
    return khoang[0] <= ngay <= khoang[1]


# ============================ GIT ============================
def git_commits(khoang) -> list[str]:
    """Danh sách tiêu đề commit trong khoảng [dau, cuoi] (theo ngày tác giả)."""
    dau, cuoi = khoang
    try:
        out = subprocess.run(
            ["git", "log",
             f"--since={dau.isoformat()} 00:00",
             f"--until={cuoi.isoformat()} 23:59",
             "--date=short", "--pretty=format:%ad | %s"],
            cwd=VAULT, capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        return [l for l in out.stdout.splitlines() if l.strip()]
    except Exception as e:  # pragma: no cover
        return [f"(không đọc được git: {e})"]


# ============================ LOG.MD ============================
def dem_log(khoang) -> dict:
    """Đếm mục log.md theo loại trong khoảng; kèm danh sách dòng tiêu đề."""
    dem = {"ingest": 0, "query": 0, "lint": 0, "update": 0, "init": 0, "khac": 0}
    dong = []
    if not LOG_MD.exists():
        return {"dem": dem, "dong": dong, "tong": 0}
    for line in LOG_MD.read_text(encoding="utf-8").splitlines():
        m = RE_LOG.match(line)
        if not m:
            continue
        try:
            ngay = dt.date.fromisoformat(m.group("ngay"))
        except ValueError:
            continue
        if not trong_khoang(ngay, khoang):
            continue
        loai = m.group("loai").lower()
        dem[loai if loai in dem else "khac"] += 1
        dong.append(line.lstrip("# ").strip())
    return {"dem": dem, "dong": dong, "tong": sum(dem.values())}


# ============================ DMO ============================
def phan_tich_dmo(khoang) -> dict:
    """Số ngày có DMO, % mỗi ngày, % trung bình, dòng liên quan tiền."""
    ngay_list = []
    for p in sorted(DMO_DIR.glob("DMO-*.md")):
        m = re.match(r"DMO-(\d{4}-\d{2}-\d{2})\.md$", p.name)
        if not m:
            continue
        try:
            ngay = dt.date.fromisoformat(m.group(1))
        except ValueError:
            continue
        if not trong_khoang(ngay, khoang):
            continue
        noi_dung = p.read_text(encoding="utf-8")
        xong = tong = 0
        for line in noi_dung.splitlines():
            mm = RE_CHECKBOX.match(line)
            if mm:
                tong += 1
                if mm.group("dau").lower() == "x":
                    xong += 1
        pct = round(xong / tong * 100) if tong else 0
        dong_tien = [l.strip() for l in noi_dung.splitlines()
                     if RE_TIEN.search(l)
                     and l.strip().startswith(("-", "*", "|", "II", "III", "IV"))
                     and any(c.isdigit() for c in l)]
        ngay_list.append({
            "ngay": ngay.isoformat(),
            "thu": THU_VN[ngay.weekday()],
            "xong": xong, "tong": tong, "pct": pct,
            "dong_tien": dong_tien[:8],
        })
    so_ngay = len(ngay_list)
    pct_tb = round(sum(d["pct"] for d in ngay_list) / so_ngay) if so_ngay else 0
    return {"so_ngay": so_ngay, "pct_tb": pct_tb, "ngay": ngay_list}


# ============================ WIKI ============================
def dem_wiki_moi(khoang) -> dict:
    """Đếm trang wiki có frontmatter ngay_tao rơi vào khoảng."""
    dong = []
    for p in WIKI_DIR.rglob("*.md"):
        try:
            head = p.read_text(encoding="utf-8")[:600]
        except Exception:
            continue
        m = RE_NGAY_TAO.search(head)
        if not m:
            continue
        try:
            ngay = dt.date.fromisoformat(m.group(1))
        except ValueError:
            continue
        if trong_khoang(ngay, khoang):
            dong.append(str(p.relative_to(WIKI_DIR)).replace("\\", "/"))
    return {"so_trang": len(dong), "trang": sorted(dong)}


# ============================ TỔNG HỢP ============================
def thu_thap(khoang) -> dict:
    return {
        "khoang": [khoang[0].isoformat(), khoang[1].isoformat()],
        "git": git_commits(khoang),
        "log": dem_log(khoang),
        "dmo": phan_tich_dmo(khoang),
        "wiki": dem_wiki_moi(khoang),
    }


def in_nguoi_doc(den: dt.date, nay: dict, truoc: dict):
    def dashline():
        print("-" * 60)

    print(f"📊 SỐ LIỆU BÁO CÁO TUẦN — bộ não thứ hai (mốc {den.isoformat()})")
    print(f"   Tuần này : {nay['khoang'][0]} → {nay['khoang'][1]}")
    print(f"   Tuần trước: {truoc['khoang'][0]} → {truoc['khoang'][1]}")
    dashline()
    print(f"{'Chỉ số':<28}{'Tuần trước':>14}{'Tuần này':>14}")
    dashline()
    print(f"{'Commit git':<28}{len(truoc['git']):>14}{len(nay['git']):>14}")
    print(f"{'Mục nhật ký (log.md)':<28}{truoc['log']['tong']:>14}{nay['log']['tong']:>14}")
    for k in ("ingest", "query", "lint", "update"):
        print(f"{'  · ' + k:<28}{truoc['log']['dem'][k]:>14}{nay['log']['dem'][k]:>14}")
    print(f"{'Trang wiki mới (ngay_tao)':<28}{truoc['wiki']['so_trang']:>14}{nay['wiki']['so_trang']:>14}")
    print(f"{'Ngày có DMO':<28}{truoc['dmo']['so_ngay']:>14}{nay['dmo']['so_ngay']:>14}")
    print(f"{'% DMO trung bình':<28}{str(truoc['dmo']['pct_tb'])+'%':>14}{str(nay['dmo']['pct_tb'])+'%':>14}")
    dashline()
    print("\n▶ Commit tuần này:")
    for l in nay["git"] or ["   (không có)"]:
        print(f"   {l}")
    print("\n▶ Mục nhật ký tuần này:")
    for l in nay["log"]["dong"] or ["   (không có)"]:
        print(f"   {l}")
    print("\n▶ DMO tuần này (ngày · % · dòng kiểm đếm tiền):")
    for d in nay["dmo"]["ngay"] or []:
        print(f"   {d['ngay']} ({d['thu']}) — {d['xong']}/{d['tong']} · {d['pct']}%")
        for t in d["dong_tien"]:
            print(f"       ↳ {t}")
    if not nay["dmo"]["ngay"]:
        print("   (không có)")


def main():
    ap = argparse.ArgumentParser(description="Số liệu báo cáo tuần cho bộ não thứ hai")
    ap.add_argument("--den", help="Ngày cuối tuần này, YYYY-MM-DD (mặc định: hôm nay)")
    ap.add_argument("--json", action="store_true", help="Xuất JSON cho LLM")
    args = ap.parse_args()

    den = parse_ngay(args.den)
    tuan_nay, tuan_truoc = khoang_tuan(den)
    nay = thu_thap(tuan_nay)
    truoc = thu_thap(tuan_truoc)

    if args.json:
        print(json.dumps({"den": den.isoformat(), "tuan_nay": nay, "tuan_truoc": truoc},
                         ensure_ascii=False, indent=2))
    else:
        in_nguoi_doc(den, nay, truoc)


if __name__ == "__main__":
    main()
