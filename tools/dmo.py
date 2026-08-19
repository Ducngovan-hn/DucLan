#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
dmo.py — CÔNG CỤ NẾP NGÀY (DMO) CỦA ANH ĐỨC

Sinh và theo dõi file DMO (Daily Method of Operations) mỗi ngày trong
production/dmo/. Mọi việc đếm % / chuyển việc tồn / xuất lịch làm ở đây
(không tốn token). File DMO là file chữ .md — nguồn chân lý của một ngày.

Các lệnh:
  python tools/dmo.py tao [--ngay YYYY-MM-DD] [--ep]
        Tạo production/dmo/DMO-<ngày>.md từ template _MAU-DMO.md,
        tự điền ngày/thứ và bê VIỆC CÒN TỒN (chưa tick) từ file DMO gần nhất sang.
        Mặc định ngày = hôm nay. --ep để ghi đè nếu file đã có.

  python tools/dmo.py bao-cao [--ngay YYYY-MM-DD] [--cap-nhat]
        Đọc file DMO ngày đó, đếm [x] vs [ ], in "n/N việc · P%" + việc còn tồn.
        --cap-nhat: ghi lại dòng "TIẾN ĐỘ:" trong chính file DMO.

  python tools/dmo.py lich [--ngay YYYY-MM-DD]
        Xuất JSON danh sách 6 việc + khung giờ (để LLM đẩy lên Google Calendar).

Mặc định --ngay là HÔM NAY theo giờ máy.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

# ----- buộc stdout ra UTF-8 để tiếng Việt không lỗi trên Windows -----
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ============================ ĐƯỜNG DẪN ============================
VAULT = Path(__file__).resolve().parent.parent
DMO_DIR = VAULT / "production" / "dmo"
TEMPLATE = DMO_DIR / "_MAU-DMO.md"

THU_VN = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]

# Ký hiệu trạng thái ở đầu nội dung việc — cắt bỏ khi trích tên việc.
EMOJI_TRANG_THAI = ["⬜", "🔴", "💚", "✅"]

# Regex một dòng checkbox:  - [ ] nội dung  /  - [x] nội dung
RE_CHECKBOX = re.compile(r"^\s*[-*]\s*\[(?P<dau>[ xX])\]\s*(?P<noidung>.*)$")

# Khung giờ mặc định cho 6 việc (giờ VN) — dùng cho lệnh "lich".
LICH_MAC_DINH = [
    {"ten": "🏃 Rèn thân — chạy bộ", "bat_dau": "05:30", "ket_thuc": "06:45"},
    {"ten": "📚 Tiếng Trung — 1 tiếng", "bat_dau": "06:45", "ket_thuc": "07:45"},
    {"ten": "💰 Làm việc tạo ra tiền (xưởng dệt + content/video)", "bat_dau": "08:00", "ket_thuc": "18:00"},
    {"ten": "📚 LTTTL — 1 tiếng", "bat_dau": "19:00", "ket_thuc": "20:00"},
    {"ten": "📚 Đọc / nghe sách — 1 tiếng", "bat_dau": "20:00", "ket_thuc": "21:00"},
    {"ten": "📚 Học tạo video — 1 tiếng", "bat_dau": "21:00", "ket_thuc": "22:00"},
    {"ten": "🧾 Kiểm đếm cuối ngày (tiền · 6 lọ · chi · khách trả hàng)", "bat_dau": "22:00", "ket_thuc": "23:00"},
    {"ten": "🌙 Đánh giá cuối ngày (% · việc tồn · 3 lời biết ơn · DMO mai)", "bat_dau": "22:00", "ket_thuc": "23:00"},
    {"ten": "🕯️ Phalon — suy ngẫm 30 phút", "bat_dau": "23:00", "ket_thuc": "23:30"},
]


# ============================ TIỆN ÍCH ============================
def parse_ngay(s: str | None) -> dt.date:
    """Đổi chuỗi YYYY-MM-DD thành date; None = hôm nay."""
    if not s:
        return dt.date.today()
    try:
        return dt.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        sys.exit(f"Ngày không hợp lệ: {s!r} — cần dạng YYYY-MM-DD")


def duong_dan_dmo(ngay: dt.date) -> Path:
    return DMO_DIR / f"DMO-{ngay.isoformat()}.md"


def thu_tieng_viet(ngay: dt.date) -> str:
    return THU_VN[ngay.weekday()]


def trich_ten_viec(noidung: str) -> str:
    """Bỏ emoji trạng thái + phần placeholder gạch dưới, giữ tên việc gọn."""
    t = noidung.strip()
    for e in EMOJI_TRANG_THAI:
        if t.startswith(e):
            t = t[len(e):].strip()
    # Bỏ đuôi ": ______" hoặc chuỗi gạch dưới trống
    t = re.sub(r":\s*_+.*$", "", t).strip()
    t = re.sub(r"\s*_{3,}.*$", "", t).strip()
    return t


def liet_ke_files() -> list[tuple[dt.date, Path]]:
    """Danh sách (ngày, path) các file DMO-*.md, sắp tăng dần theo ngày."""
    ket_qua = []
    for p in DMO_DIR.glob("DMO-*.md"):
        m = re.match(r"DMO-(\d{4}-\d{2}-\d{2})\.md$", p.name)
        if m:
            try:
                ket_qua.append((dt.date.fromisoformat(m.group(1)), p))
            except ValueError:
                pass
    return sorted(ket_qua, key=lambda x: x[0])


def file_hom_truoc(ngay: dt.date) -> Path | None:
    """File DMO có ngày gần nhất TRƯỚC ngày cho trước."""
    truoc = [(d, p) for d, p in liet_ke_files() if d < ngay]
    return truoc[-1][1] if truoc else None


def dem_tien_do(noi_dung: str) -> tuple[int, int, list[str]]:
    """Trả về (số việc xong, tổng việc, danh sách việc chưa xong)."""
    xong = tong = 0
    con_ton = []
    for line in noi_dung.splitlines():
        m = RE_CHECKBOX.match(line)
        if not m:
            continue
        tong += 1
        if m.group("dau").lower() == "x":
            xong += 1
        else:
            con_ton.append(trich_ten_viec(m.group("noidung")))
    return xong, tong, con_ton


def dong_tien_do(xong: int, tong: int) -> str:
    pct = round(xong / tong * 100) if tong else 0
    return f"TIẾN ĐỘ: {xong}/{tong} việc · {pct}%"


# ============================ LỆNH: tao ============================
def lenh_tao(args):
    ngay = parse_ngay(args.ngay)
    dich = duong_dan_dmo(ngay)
    if dich.exists() and not args.ep:
        sys.exit(f"Đã có {dich.name}. Thêm --ep để ghi đè (cẩn thận mất dữ liệu đã tick).")
    if not TEMPLATE.exists():
        sys.exit(f"Không thấy template: {TEMPLATE}")

    mau = TEMPLATE.read_text(encoding="utf-8")

    # Tên các việc CỐ ĐỊNH đã có sẵn trong template — không bê lại (tránh nhân đôi).
    _, _, viec_co_dinh = dem_tien_do(mau)
    tap_co_dinh = {v for v in viec_co_dinh if v}

    # --- Bê việc còn tồn từ file gần nhất trước đó ---
    khoi_ton = ""
    truoc = file_hom_truoc(ngay)
    if truoc:
        _, _, con_ton = dem_tien_do(truoc.read_text(encoding="utf-8"))
        # Chỉ giữ VIỆC PHÁT SINH (tên khác việc cố định trong template).
        con_ton = [v for v in con_ton if v and v not in tap_co_dinh]
        if con_ton:
            m = re.match(r"DMO-(\d{4}-\d{2}-\d{2})\.md$", truoc.name)
            ngay_truoc = m.group(1) if m else "hôm trước"
            dong = "\n".join(f"- [ ] ⬜ {v}" for v in con_ton)
            khoi_ton = f"## ⏮️ VIỆC CÒN TỒN TỪ {ngay_truoc}\n\n{dong}\n"

    noi_dung = (
        mau.replace("{{THU}}", thu_tieng_viet(ngay))
        .replace("{{NGAY}}", ngay.isoformat())
        .replace("{{VIEC_TON}}", khoi_ton)
        .replace("{{TIEN_DO}}", "0/? việc · 0% (chạy `dmo.py bao-cao` để tính)")
    )

    DMO_DIR.mkdir(parents=True, exist_ok=True)
    dich.write_text(noi_dung, encoding="utf-8")
    print(f"✅ Đã tạo {dich.relative_to(VAULT)}")
    if khoi_ton:
        print(f"   ⏮️  Đã chuyển {khoi_ton.count(chr(10)) - 2} việc còn tồn từ {truoc.name}")
    else:
        print("   (không có việc tồn từ hôm trước)")


# ============================ LỆNH: bao-cao ============================
def lenh_bao_cao(args):
    ngay = parse_ngay(args.ngay)
    f = duong_dan_dmo(ngay)
    if not f.exists():
        sys.exit(f"Chưa có file DMO cho {ngay.isoformat()}. Chạy: python tools/dmo.py tao --ngay {ngay.isoformat()}")

    noi_dung = f.read_text(encoding="utf-8")
    xong, tong, con_ton = dem_tien_do(noi_dung)
    dong = dong_tien_do(xong, tong)

    print(f"📋 DMO {thu_tieng_viet(ngay)}, {ngay.isoformat()}")
    print(dong)
    if con_ton:
        print(f"\n⬜ Còn lại {len(con_ton)} việc:")
        for v in con_ton:
            print(f"   · {v}")
    else:
        print("\n💚 Đã xong hết!")

    if args.cap_nhat:
        moi = re.sub(r"TIẾN ĐỘ:.*", dong, noi_dung)
        if moi != noi_dung:
            f.write_text(moi, encoding="utf-8")
            print(f"\n(đã cập nhật dòng TIẾN ĐỘ trong {f.name})")


# ============================ LỆNH: lich ============================
def lenh_lich(args):
    ngay = parse_ngay(args.ngay)
    events = []
    for viec in LICH_MAC_DINH:
        events.append({
            "summary": viec["ten"],
            "start": {"dateTime": f"{ngay.isoformat()}T{viec['bat_dau']}:00", "timeZone": "Asia/Ho_Chi_Minh"},
            "end": {"dateTime": f"{ngay.isoformat()}T{viec['ket_thuc']}:00", "timeZone": "Asia/Ho_Chi_Minh"},
        })
    print(json.dumps({"ngay": ngay.isoformat(), "events": events}, ensure_ascii=False, indent=2))


# ============================ MAIN ============================
def main():
    ap = argparse.ArgumentParser(description="Công cụ nếp ngày (DMO) của anh Đức")
    sub = ap.add_subparsers(dest="lenh", required=True)

    p_tao = sub.add_parser("tao", help="Tạo file DMO cho một ngày")
    p_tao.add_argument("--ngay", help="YYYY-MM-DD (mặc định: hôm nay)")
    p_tao.add_argument("--ep", action="store_true", help="Ghi đè nếu file đã tồn tại")
    p_tao.set_defaults(func=lenh_tao)

    p_bc = sub.add_parser("bao-cao", help="Báo cáo tiến độ một ngày")
    p_bc.add_argument("--ngay", help="YYYY-MM-DD (mặc định: hôm nay)")
    p_bc.add_argument("--cap-nhat", action="store_true", help="Ghi lại dòng TIẾN ĐỘ vào file")
    p_bc.set_defaults(func=lenh_bao_cao)

    p_l = sub.add_parser("lich", help="Xuất JSON 6 việc + khung giờ cho Google Calendar")
    p_l.add_argument("--ngay", help="YYYY-MM-DD (mặc định: hôm nay)")
    p_l.set_defaults(func=lenh_lich)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
