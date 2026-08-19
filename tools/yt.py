#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
yt.py — CÔNG CỤ YOUTUBE CHO ĐỨC LAN

Gọi thẳng YouTube Data API v3 + YouTube Analytics API v2 (không qua MCP).
Cùng khuôn với tools/dh.py: mọi việc nặng làm ở đây, LLM chỉ ra lệnh.

CHUẨN BỊ MỘT LẦN (xem hướng dẫn ở cuối file):
  1. Bật YouTube Data API v3 trên Google Cloud Console
  2. Tải client_secret về  ->  C:\\Users\\admin\\.youtube\\client_secret.json
  3. python tools/yt.py xin-quyen

NHIỀU KÊNH / NHIỀU EMAIL:
  Mỗi tài khoản một token riêng, gọi bằng --tk <tên tự đặt>:
      python tools/yt.py xin-quyen --tk phu      (đăng nhập email thứ hai)
      python tools/yt.py kenh --tk phu
      python tools/yt.py dang v.mp4 --tk phu --tieu-de "..."
  Không ghi --tk thì dùng tài khoản "chinh".
  Xem đã có những tài khoản nào:  python tools/yt.py tai-khoan

ĐỌC DỮ LIỆU:
  python tools/yt.py kenh                      Thông tin kênh của mình
  python tools/yt.py video --so 25             Video của kênh mình + lượt xem
  python tools/yt.py so-lieu --ngay 28         Lượt xem / giờ xem / sub theo kỳ
  python tools/yt.py xem <videoId> ...         Xem số liệu video bất kỳ
  python tools/yt.py tim "dệt bo" --so 10      Tìm video công khai
  python tools/yt.py binh-luan <videoId>       Đọc bình luận
  python tools/yt.py phu-de <link> <link> ...  Lấy phụ đề video BẤT KỲ (nghiên cứu đối thủ)
                                               -> ra file .txt trong production/youtube/phu-de/
                                               Cần yt-dlp: pip install yt-dlp

ĐĂNG VIDEO:
  python tools/yt.py dang video.mp4 --tieu-de "Bo dệt Đức Lan" \\
      --mo-ta "Mô tả..." --tag "dệt bo,chun dệt" --anh-bia bia.jpg

  Mặc định đăng ở chế độ RIÊNG TƯ (private) cho an toàn.
  Muốn công khai phải ghi rõ:  --che-do public

Thêm --json vào lệnh đọc để lấy JSON thay vì bảng.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import datetime as dt
from pathlib import Path

# ----- buộc stdout ra UTF-8 để tiếng Việt không lỗi trên Windows -----
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
except ImportError:
    sys.exit(
        "Thiếu thư viện Google. Chạy:\n"
        "  pip install google-auth google-auth-oauthlib google-api-python-client"
    )

# ============================ ĐƯỜNG DẪN ============================
YT_DIR = Path(os.environ.get("YT_DIR") or Path.home() / ".youtube")
CLIENT_SECRET = YT_DIR / "client_secret.json"

# Mỗi tài khoản (email) một file token riêng: credentials-<tên>.json
TAI_KHOAN = "chinh"
TOKEN_FILE = YT_DIR / f"credentials-{TAI_KHOAN}.json"


def _dat_tai_khoan(ten: str) -> None:
    """Chọn tài khoản đang làm việc — gọi trước mọi lệnh cần token."""
    global TAI_KHOAN, TOKEN_FILE
    TAI_KHOAN = (ten or "chinh").strip().lower()
    TOKEN_FILE = YT_DIR / f"credentials-{TAI_KHOAN}.json"

VAULT = Path(__file__).resolve().parent.parent
TAI_VE_DIR = VAULT / "production" / "youtube"

# Quyền xin một lần, dùng cho cả đọc lẫn đăng:
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",      # đăng video
    "https://www.googleapis.com/auth/youtube.force-ssl",   # đọc/ghi kênh, phụ đề, bình luận
    "https://www.googleapis.com/auth/yt-analytics.readonly",  # số liệu thống kê
]

# Danh mục video hay dùng (categoryId của YouTube tại VN)
DANH_MUC = {
    "22": "People & Blogs (mặc định)",
    "24": "Entertainment",
    "26": "Howto & Style",
    "27": "Education",
    "28": "Science & Technology",
    "10": "Music",
}


# ============================ TIỆN ÍCH ============================
def _so(n) -> str:
    """1234567 -> 1.234.567"""
    try:
        return f"{int(n):,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(n or "—")


def _cat(s: str, n: int) -> str:
    s = (s or "").replace("\n", " ").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def _ngay(chuoi: str) -> str:
    """2026-07-31T10:20:30Z -> 31/07/2026"""
    if not chuoi:
        return "—"
    try:
        return dt.datetime.fromisoformat(chuoi.replace("Z", "+00:00")).strftime("%d/%m/%Y")
    except ValueError:
        return chuoi


def _in_json(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


# ============================ XÁC THỰC ============================
def _luu_token(creds: Credentials) -> None:
    YT_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    try:  # chỉ chủ máy đọc được
        os.chmod(TOKEN_FILE, 0o600)
    except OSError:
        pass


def lenh_xin_quyen(args) -> None:
    """Chạy luồng đồng ý OAuth, lấy refresh_token dùng lâu dài."""
    if TOKEN_FILE.exists() and not args.lai:
        print(f"Tài khoản '{TAI_KHOAN}' đã có token: {TOKEN_FILE}")
        print("Muốn xin lại quyền (ví dụ để thêm quyền mới), chạy kèm --lai")
        print("Muốn thêm email KHÁC, đặt tên khác:  xin-quyen --tk phu")
        return

    if not CLIENT_SECRET.exists():
        sys.exit(
            f"Chưa thấy file client_secret tại:\n  {CLIENT_SECRET}\n\n"
            "Cách lấy:\n"
            "  1. console.cloud.google.com -> chọn project\n"
            "  2. APIs & Services -> Library -> bật 'YouTube Data API v3'\n"
            "     và 'YouTube Analytics API'\n"
            "  3. Credentials -> Create credentials -> OAuth client ID\n"
            "     -> Application type: Desktop app\n"
            "  4. Tải file JSON về, đổi tên thành client_secret.json,\n"
            f"     bỏ vào thư mục {YT_DIR}"
        )

    print(f"Đang xin quyền cho tài khoản '{TAI_KHOAN}'.")
    print("Trình duyệt sắp mở — nhớ CHỌN ĐÚNG EMAIL của kênh này.\n")

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    # access_type=offline + prompt=consent để chắc chắn nhận được refresh_token
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    _luu_token(creds)

    print(f"Xong. Token đã lưu: {TOKEN_FILE}")
    print("Quyền đã cấp:")
    for s in creds.scopes or []:
        print(f"  · {s}")

    try:  # xác nhận đúng kênh, tránh đăng nhầm về sau
        k = _kenh_cua_toi(build("youtube", "v3", credentials=creds, cache_discovery=False))
        print(f"\nTài khoản '{TAI_KHOAN}' = kênh: {k['snippet']['title']}  ({k['id']})")
    except HttpError as e:
        print(f"\nCẢNH BÁO: chưa đọc được tên kênh — {e}")

    print(f"\nThử ngay:  python tools/yt.py kenh --tk {TAI_KHOAN}")


def lenh_tai_khoan(args) -> None:
    """Liệt kê các tài khoản đã xin quyền."""
    ds = sorted(YT_DIR.glob("credentials-*.json")) if YT_DIR.exists() else []
    if not ds:
        print("Chưa có tài khoản nào. Chạy:  python tools/yt.py xin-quyen")
        return

    print(f"{'TÀI KHOẢN':<12} {'KÊNH':<38} CẬP NHẬT")
    print("-" * 76)
    for f in ds:
        ten = f.stem.replace("credentials-", "")
        _dat_tai_khoan(ten)
        try:
            k = _kenh_cua_toi(_yt())
            kenh = _cat(k["snippet"]["title"], 36)
        except (HttpError, SystemExit) as e:
            kenh = f"(lỗi: {_cat(str(e), 30)})"
        sua = dt.datetime.fromtimestamp(f.stat().st_mtime).strftime("%d/%m/%Y %H:%M")
        print(f"{ten:<12} {kenh:<38} {sua}")

    print("\nDùng tài khoản nào thì thêm --tk <tên> vào lệnh. Không ghi = 'chinh'.")


def _lay_cred() -> Credentials:
    if not TOKEN_FILE.exists():
        sys.exit("Chưa có quyền. Chạy trước:  python tools/yt.py xin-quyen")

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    thieu = [s for s in SCOPES if s not in (creds.scopes or [])]
    if thieu:
        print("CẢNH BÁO — token đang thiếu quyền:", file=sys.stderr)
        for s in thieu:
            print(f"  · {s}", file=sys.stderr)
        print("Chạy lại:  python tools/yt.py xin-quyen --lai\n", file=sys.stderr)

    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            _luu_token(creds)
        else:
            sys.exit("Token hỏng hoặc đã bị thu hồi. Chạy:  python tools/yt.py xin-quyen --lai")
    return creds


def _yt():
    return build("youtube", "v3", credentials=_lay_cred(), cache_discovery=False)


def _analytics():
    return build("youtubeAnalytics", "v2", credentials=_lay_cred(), cache_discovery=False)


def _kenh_cua_toi(yt) -> dict:
    r = yt.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()
    if not r.get("items"):
        sys.exit("Tài khoản này chưa có kênh YouTube nào.")
    return r["items"][0]


# ============================ LỆNH ĐỌC ============================
def lenh_kenh(args) -> None:
    k = _kenh_cua_toi(_yt())
    if args.json:
        _in_json(k)
        return
    st = k["statistics"]
    print(f"Kênh:        {k['snippet']['title']}")
    print(f"ID kênh:     {k['id']}")
    print(f"Lập ngày:    {_ngay(k['snippet'].get('publishedAt'))}")
    print(f"Người theo dõi: {_so(st.get('subscriberCount'))}"
          + ("  (kênh đang ẩn số sub)" if st.get("hiddenSubscriberCount") else ""))
    print(f"Tổng lượt xem:  {_so(st.get('viewCount'))}")
    print(f"Số video:       {_so(st.get('videoCount'))}")


def lenh_video(args) -> None:
    yt = _yt()
    k = _kenh_cua_toi(yt)
    uploads = k["contentDetails"]["relatedPlaylists"]["uploads"]

    ids, token = [], None
    while len(ids) < args.so:
        r = yt.playlistItems().list(
            part="contentDetails", playlistId=uploads,
            maxResults=min(50, args.so - len(ids)), pageToken=token,
        ).execute()
        ids += [i["contentDetails"]["videoId"] for i in r.get("items", [])]
        token = r.get("nextPageToken")
        if not token:
            break

    if not ids:
        print("Kênh chưa có video nào.")
        return

    ds = []
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part="snippet,statistics,status", id=",".join(ids[i:i + 50])).execute()
        ds += r.get("items", [])

    if args.json:
        _in_json(ds)
        return

    print(f"{'NGÀY':<11} {'XEM':>9} {'THÍCH':>7} {'B.LUẬN':>7}  {'CHẾ ĐỘ':<9} TIÊU ĐỀ")
    print("-" * 100)
    for v in ds:
        s, st = v["snippet"], v.get("statistics", {})
        print(f"{_ngay(s.get('publishedAt')):<11} {_so(st.get('viewCount')):>9} "
              f"{_so(st.get('likeCount')):>7} {_so(st.get('commentCount')):>7}  "
              f"{v['status'].get('privacyStatus', '—'):<9} {_cat(s.get('title'), 45)}")
        print(f"{'':<11} https://youtu.be/{v['id']}")
    print(f"\nTổng: {len(ds)} video")


def lenh_so_lieu(args) -> None:
    den = dt.date.today()
    tu = den - dt.timedelta(days=args.ngay)
    if args.tu:
        tu = dt.date.fromisoformat(args.tu)
    if args.den:
        den = dt.date.fromisoformat(args.den)

    r = _analytics().reports().query(
        ids="channel==MINE",
        startDate=tu.isoformat(), endDate=den.isoformat(),
        metrics="views,estimatedMinutesWatched,averageViewDuration,"
                "subscribersGained,subscribersLost,likes,comments",
        dimensions="day", sort="day",
    ).execute()

    if args.json:
        _in_json(r)
        return

    hang = r.get("rows", [])
    if not hang:
        print(f"Không có dữ liệu từ {tu:%d/%m/%Y} đến {den:%d/%m/%Y}.")
        return

    print(f"Số liệu kênh: {tu:%d/%m/%Y} → {den:%d/%m/%Y}\n")
    print(f"{'NGÀY':<12}{'XEM':>8}{'PHÚT XEM':>10}{'TB (giây)':>11}{'+SUB':>6}{'-SUB':>6}{'THÍCH':>7}")
    print("-" * 60)
    for h in hang:
        print(f"{_ngay(h[0] + 'T00:00:00Z'):<12}{_so(h[1]):>8}{_so(h[2]):>10}"
              f"{_so(h[3]):>11}{_so(h[4]):>6}{_so(h[5]):>6}{_so(h[6]):>7}")
    print("-" * 60)
    c = lambda i: sum(x[i] for x in hang)
    print(f"{'TỔNG':<12}{_so(c(1)):>8}{_so(c(2)):>10}{'':>11}"
          f"{_so(c(4)):>6}{_so(c(5)):>6}{_so(c(6)):>7}")
    print(f"\nTăng ròng người theo dõi: {c(4) - c(5):+}")


def lenh_xem(args) -> None:
    ds = []
    yt = _yt()
    for i in range(0, len(args.video_id), 50):
        r = yt.videos().list(
            part="snippet,statistics,contentDetails,status",
            id=",".join(args.video_id[i:i + 50]),
        ).execute()
        ds += r.get("items", [])

    if args.json:
        _in_json(ds)
        return
    if not ds:
        print("Không tìm thấy video nào (kiểm tra lại ID).")
        return

    for v in ds:
        s, st = v["snippet"], v.get("statistics", {})
        print(f"\n{s.get('title')}")
        print(f"  Kênh:     {s.get('channelTitle')}")
        print(f"  Đăng:     {_ngay(s.get('publishedAt'))}")
        print(f"  Thời lượng: {v['contentDetails'].get('duration', '—').replace('PT', '').lower()}")
        print(f"  Xem:      {_so(st.get('viewCount'))}   "
              f"Thích: {_so(st.get('likeCount'))}   Bình luận: {_so(st.get('commentCount'))}")
        print(f"  Link:     https://youtu.be/{v['id']}")
        if s.get("tags"):
            print(f"  Tag:      {', '.join(s['tags'][:12])}")
        if s.get("description"):
            print(f"  Mô tả:    {_cat(s['description'], 160)}")


def lenh_tim(args) -> None:
    r = _yt().search().list(
        part="snippet", q=args.tu_khoa, type="video",
        maxResults=min(args.so, 50), order=args.sap_xep, regionCode="VN",
        relevanceLanguage="vi",
    ).execute()

    if args.json:
        _in_json(r.get("items", []))
        return

    for i, v in enumerate(r.get("items", []), 1):
        s = v["snippet"]
        print(f"{i:>2}. {_cat(s.get('title'), 70)}")
        print(f"    {s.get('channelTitle')} · {_ngay(s.get('publishedAt'))} "
              f"· https://youtu.be/{v['id']['videoId']}")

    print("\nLƯU Ý: mỗi lần tìm tốn 100 đơn vị hạn ngạch (1/100 hạn mức ngày).")


def lenh_binh_luan(args) -> None:
    try:
        r = _yt().commentThreads().list(
            part="snippet", videoId=args.video_id,
            maxResults=min(args.so, 100), order="time", textFormat="plainText",
        ).execute()
    except HttpError as e:
        if "commentsDisabled" in str(e):
            sys.exit("Video này đã tắt bình luận.")
        raise

    if args.json:
        _in_json(r.get("items", []))
        return

    items = r.get("items", [])
    if not items:
        print("Chưa có bình luận nào.")
        return
    for c in items:
        t = c["snippet"]["topLevelComment"]["snippet"]
        tra_loi = c["snippet"].get("totalReplyCount", 0)
        print(f"\n[{_ngay(t.get('publishedAt'))}] {t.get('authorDisplayName')} "
              f"({_so(t.get('likeCount'))} thích"
              + (f", {tra_loi} trả lời" if tra_loi else "") + ")")
        print(f"  {t.get('textDisplay')}")
    print(f"\nTổng: {len(items)} bình luận gốc")


def _chuan_hoa_id(x: str) -> str:
    """Nhận ID trần hoặc URL (youtu.be / watch?v= / shorts / embed) -> trả ID 11 ký tự."""
    x = x.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", x):
        return x
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/embed/|/live/)([A-Za-z0-9_-]{11})", x)
    if m:
        return m.group(1)
    sys.exit(f"Không nhận ra video ID từ: {x}")


def _vtt_sang_van_ban(vtt: str) -> str:
    """VTT -> văn bản liền mạch. Khử kiểu chữ chạy cuộn của phụ đề tự động."""
    tho = []
    for dong in vtt.splitlines():
        d = dong.strip()
        if not d or "-->" in d or d.isdigit():
            continue
        if d.startswith(("WEBVTT", "Kind:", "Language:", "NOTE", "STYLE", "::cue")):
            continue
        d = re.sub(r"<[^>]+>", "", d)          # bỏ <c>, <00:00:01.234>
        d = html.unescape(d).replace(" ", " ").strip()
        if d and (not tho or tho[-1] != d):
            tho.append(d)

    sach: list[str] = []
    for d in tho:
        if sach:
            truoc = sach[-1]
            if d.startswith(truoc) or truoc.endswith(d) or d in truoc:
                if len(d) > len(truoc):        # dòng sau là bản nối dài của dòng trước
                    sach[-1] = d
                continue
        sach.append(d)
    return " ".join(sach)


def _js_runtime() -> list[str]:
    """yt-dlp nay cần một máy chạy JavaScript, thiếu nó sẽ đọc hụt vài video."""
    for ten in ("deno", "node", "bun"):
        if shutil.which(ten):
            return ["--js-runtimes", ten]
    return []


def _chay_ytdlp(vid: str, them: list[str]) -> subprocess.CompletedProcess:
    lenh = [
        sys.executable, "-m", "yt_dlp", "--no-warnings", "--quiet",
        "--retries", "3", "--sleep-requests", "1",
        *_js_runtime(), *them,
        f"https://www.youtube.com/watch?v={vid}",
    ]
    return subprocess.run(lenh, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def _bao_loi_ytdlp(vid: str, loi: str) -> None:
    loi = (loi or "").strip()
    if "Private video" in loi:
        print(f"  {vid}: video RIÊNG TƯ — người ngoài không lấy được.")
    elif "Video unavailable" in loi or "not available" in loi:
        print(f"  {vid}: video đã gỡ, hoặc bị chặn theo khu vực/độ tuổi.")
    elif "429" in loi or "Too Many Requests" in loi:
        print(f"  {vid}: YouTube chặn tạm vì hỏi quá dồn. Đợi 5–10 phút rồi chạy lại.")
    elif "Sign in to confirm" in loi:
        print(f"  {vid}: YouTube nghi máy tự động, đòi đăng nhập. Đợi lát rồi thử lại.")
    else:
        print(f"  {vid}: yt-dlp lỗi — {_cat(loi, 200)}")


def _thong_tin_video(vid: str) -> dict | None:
    kq = _chay_ytdlp(vid, ["--dump-json", "--skip-download"])
    if kq.returncode != 0 or not kq.stdout.strip():
        _bao_loi_ytdlp(vid, kq.stderr or kq.stdout)
        return None
    try:
        return json.loads(kq.stdout.splitlines()[0])
    except json.JSONDecodeError:
        print(f"  {vid}: không đọc được thông tin video.")
        return None


def _la_ma_goc(ma: str, ng: str) -> bool:
    """'vi' / 'vi-orig' / 'vi-VN' là bản gốc; 'vi-en' là bản MÁY DỊCH từ tiếng Anh."""
    if ma.lower() in (ng, f"{ng}-orig"):
        return True
    m = re.fullmatch(rf"{re.escape(ng)}-([A-Za-z]+)", ma, re.IGNORECASE)
    return bool(m) and m.group(1).isupper()      # đuôi HOA = biến thể vùng


def _chon_ma_phu_de(info: dict, ng: str, cho_dich: bool) -> list[tuple[str, str]]:
    """Trả [(mã, mô tả)] — ưu tiên phụ đề người làm, rồi tới phụ đề tự động."""
    that = list((info.get("subtitles") or {}).keys())
    tu_dong = list((info.get("automatic_captions") or {}).keys())

    if ng == "all":
        chon = [(m, "người làm") for m in that][:10]
        return chon or [(m, "tự động") for m in tu_dong if "-" not in m][:5]

    for ma in that:
        if _la_ma_goc(ma, ng):
            return [(ma, "người làm")]
    for ma in tu_dong:
        if _la_ma_goc(ma, ng):
            return [(ma, "tự động nhận dạng")]
    if cho_dich:
        for ma in tu_dong:
            if ma.lower().startswith(f"{ng}-"):
                return [(ma, "MÁY DỊCH — có thể sai nhiều")]
    return []


def _goi_y_ngon_ngu(info: dict) -> None:
    that = list((info.get("subtitles") or {}).keys())
    tu_dong = [m for m in (info.get("automatic_captions") or {}) if "-" not in m]
    if that:
        print(f"  Phụ đề người làm có: {', '.join(that[:15])}")
    if tu_dong:
        print(f"  Phụ đề tự động có:   {', '.join(tu_dong[:15])}")
    if not that and not tu_dong:
        print("  Video này KHÔNG có phụ đề nào cả (kể cả tự động).")
    else:
        print("  Thêm --dich để lấy bản máy dịch sang tiếng Việt.")


def lenh_phu_de(args) -> None:
    dich = TAI_VE_DIR / "phu-de"
    dich.mkdir(parents=True, exist_ok=True)
    ng = args.ngon_ngu.lower()

    for x in args.video:
        vid = _chuan_hoa_id(x)
        print(f"\n▸ {vid}")

        info = _thong_tin_video(vid)
        if not info:
            if args.api:
                _thu_qua_api(vid, ng, dich)
            continue

        giay = int(info.get("duration") or 0)
        print(f"  {_cat(info.get('title'), 70)}")
        print(f"  Kênh: {info.get('uploader')} · {giay // 60}:{giay % 60:02d} · "
              f"{_so(info.get('view_count'))} lượt xem")

        ma_list = _chon_ma_phu_de(info, ng, args.dich)
        if not ma_list:
            print(f"  Không có phụ đề tiếng '{ng}'.")
            _goi_y_ngon_ngu(info)
            if args.api:
                _thu_qua_api(vid, ng, dich)
            continue

        for ma, loai in ma_list:
            for cu in dich.glob(f"{vid}*.vtt"):    # dọn file thừa của lần chạy trước
                cu.unlink()
            kq = _chay_ytdlp(vid, [
                "--skip-download", "--write-subs", "--write-auto-subs",
                "--sub-langs", ma, "--sub-format", "vtt",
                "-o", str(dich / "%(id)s"),
            ])
            vtts = sorted(dich.glob(f"{vid}*.vtt"))
            if not vtts:
                _bao_loi_ytdlp(vid, kq.stderr or kq.stdout)
                continue

            da_ghi: set[str] = set()
            for f in vtts:
                van_ban = _vtt_sang_van_ban(f.read_text(encoding="utf-8", errors="replace"))
                if van_ban in da_ghi:      # cùng nội dung, khác tên file
                    f.unlink()
                    continue
                da_ghi.add(van_ban)
                f_txt = dich / f"{f.stem.replace('.', '-')}.txt"
                f_txt.write_text(
                    f"# {info.get('title')}\n"
                    f"Kênh: {info.get('uploader')}\n"
                    f"Link: https://youtu.be/{vid}\n"
                    f"Phụ đề: {ma} ({loai})\n\n{van_ban}",
                    encoding="utf-8",
                )
                f.unlink() if not args.giu_vtt else None
                print(f"  [{ma}, {loai}] {_so(len(van_ban.split()))} từ  ->  {f_txt.name}")
                if args.in_ra:
                    print(f"\n{van_ban}\n")

    print(f"\nTất cả nằm ở: {dich}")


def _thu_qua_api(vid: str, ng: str, dich: Path) -> None:
    """Đường vòng cho video RIÊNG TƯ của chính kênh mình — yt-dlp không vào được."""
    try:
        yt = _yt()
        ds = yt.captions().list(part="snippet", videoId=vid).execute().get("items", [])
        if not ds:
            return
        chon = next((c for c in ds if c["snippet"].get("language") == ng), ds[0])
        noi_dung = yt.captions().download(id=chon["id"], tfmt="srt").execute()
        f = dich / f"{vid}-{chon['snippet'].get('language')}.srt"
        f.write_bytes(noi_dung)
        print(f"  Lấy được qua API (video của kênh mình): {f.name}")
    except HttpError:
        pass


# ============================ LỆNH ĐĂNG ============================
def lenh_dang(args) -> None:
    f = Path(args.duong_dan)
    if not f.exists():
        sys.exit(f"Không thấy file: {f}")

    mb = f.stat().st_size / 1024 / 1024
    tags = [t.strip() for t in (args.tag or "").split(",") if t.strip()]

    than = {
        "snippet": {
            "title": args.tieu_de[:100],
            "description": (args.mo_ta or "")[:5000],
            "tags": tags,
            "categoryId": args.danh_muc,
            "defaultLanguage": args.ngon_ngu,
            "defaultAudioLanguage": args.ngon_ngu,
        },
        "status": {
            "privacyStatus": args.che_do,
            "selfDeclaredMadeForKids": False,
            "madeForKids": False,
        },
    }
    if args.hen:
        than["status"]["privacyStatus"] = "private"   # hẹn giờ bắt buộc phải private
        than["status"]["publishAt"] = args.hen

    yt = _yt()
    k = _kenh_cua_toi(yt)   # in kênh đích để không đăng nhầm email

    print(f"ĐĂNG LÊN KÊNH: {k['snippet']['title']}   (tài khoản '{TAI_KHOAN}')")
    print(f"File:      {f.name}  ({mb:.1f} MB)")
    print(f"Tiêu đề:   {args.tieu_de}")
    print(f"Chế độ:    {args.che_do}" + (f"  (hẹn công khai {args.hen})" if args.hen else ""))
    print(f"Tag:       {', '.join(tags) or '—'}")
    if args.thu:
        print("\n[CHẠY KHÔ] Dừng ở đây, chưa đăng gì.")
        return

    print("\nĐang tải lên…")
    yc = yt.videos().insert(
        part="snippet,status", body=than,
        media_body=MediaFileUpload(str(f), chunksize=8 * 1024 * 1024, resumable=True),
    )

    kq, phan_tram_cu = None, -1
    while kq is None:
        try:
            tien_do, kq = yc.next_chunk()
        except HttpError as e:
            if e.resp.status in (500, 502, 503, 504):
                print("  (lỗi tạm thời của Google, đang thử lại…)")
                continue
            if e.resp.status == 403 and "quota" in str(e).lower():
                sys.exit("HẾT HẠN NGẠCH NGÀY. Mỗi lần đăng tốn 1.600/10.000 đơn vị "
                         "(khoảng 6 video/ngày). Đợi 14:00 giờ VN hôm sau hạn ngạch reset.")
            raise
        if tien_do:
            pt = int(tien_do.progress() * 100)
            if pt >= phan_tram_cu + 10:
                print(f"  {pt}%")
                phan_tram_cu = pt

    vid = kq["id"]
    print(f"\nĐĂNG XONG: https://youtu.be/{vid}")
    print(f"Sửa tại:   https://studio.youtube.com/video/{vid}/edit")

    if args.anh_bia:
        bia = Path(args.anh_bia)
        if not bia.exists():
            print(f"CẢNH BÁO: không thấy ảnh bìa {bia}, bỏ qua.")
        else:
            try:
                yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(bia))).execute()
                print("Đã đặt ảnh bìa.")
            except HttpError as e:
                print(f"CẢNH BÁO: đặt ảnh bìa thất bại — {e}")

    if args.playlist:
        try:
            yt.playlistItems().insert(
                part="snippet",
                body={"snippet": {"playlistId": args.playlist,
                                  "resourceId": {"kind": "youtube#video", "videoId": vid}}},
            ).execute()
            print("Đã thêm vào playlist.")
        except HttpError as e:
            print(f"CẢNH BÁO: thêm playlist thất bại — {e}")

    if args.che_do == "private" and not args.hen:
        print("\nVideo đang RIÊNG TƯ. Muốn công khai thì vào Studio đổi, "
              "hoặc đăng lại với --che-do public.")


# ============================ CLI ============================
def main() -> None:
    p = argparse.ArgumentParser(
        description="Công cụ YouTube cho Đức Lan — đọc dữ liệu và đăng video.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Chạy 'python tools/yt.py <lệnh> -h' để xem tham số từng lệnh.",
    )
    # tham số dùng chung cho mọi lệnh
    chung = argparse.ArgumentParser(add_help=False)
    chung.add_argument("--tk", default="chinh", metavar="TÊN",
                       help="Tài khoản (email) nào — mặc định 'chinh'")

    sp = p.add_subparsers(dest="lenh", required=True)
    _them = sp.add_parser
    sp.add_parser = lambda *a, **kw: _them(*a, parents=[chung], **kw)

    def them_json(x):
        x.add_argument("--json", action="store_true", help="Xuất JSON thay vì bảng")
        return x

    tk = sp.add_parser("tai-khoan", help="Liệt kê các tài khoản đã xin quyền")
    tk.set_defaults(func=lenh_tai_khoan)

    q = sp.add_parser("xin-quyen", help="Xin quyền OAuth (làm một lần cho mỗi email)")
    q.add_argument("--lai", action="store_true", help="Xin lại dù đã có token")
    q.set_defaults(func=lenh_xin_quyen)

    k = them_json(sp.add_parser("kenh", help="Thông tin kênh của mình"))
    k.set_defaults(func=lenh_kenh)

    v = them_json(sp.add_parser("video", help="Video của kênh mình + số liệu"))
    v.add_argument("--so", type=int, default=25, help="Lấy bao nhiêu video (mặc định 25)")
    v.set_defaults(func=lenh_video)

    s = them_json(sp.add_parser("so-lieu", help="Lượt xem / giờ xem / sub theo ngày"))
    s.add_argument("--ngay", type=int, default=28, help="Số ngày gần đây (mặc định 28)")
    s.add_argument("--tu", help="Từ ngày YYYY-MM-DD")
    s.add_argument("--den", help="Đến ngày YYYY-MM-DD")
    s.set_defaults(func=lenh_so_lieu)

    x = them_json(sp.add_parser("xem", help="Số liệu video bất kỳ theo ID"))
    x.add_argument("video_id", nargs="+")
    x.set_defaults(func=lenh_xem)

    t = them_json(sp.add_parser("tim", help="Tìm video công khai"))
    t.add_argument("tu_khoa")
    t.add_argument("--so", type=int, default=10)
    t.add_argument("--sap-xep", default="relevance",
                   choices=["relevance", "date", "viewCount", "rating"])
    t.set_defaults(func=lenh_tim)

    b = them_json(sp.add_parser("binh-luan", help="Đọc bình luận của một video"))
    b.add_argument("video_id")
    b.add_argument("--so", type=int, default=50)
    b.set_defaults(func=lenh_binh_luan)

    c = sp.add_parser("phu-de", help="Lấy phụ đề video BẤT KỲ (kể cả của người khác)")
    c.add_argument("video", nargs="+", help="ID hoặc link video, ghi được nhiều cái")
    c.add_argument("--ngon-ngu", default="vi", help="vi / en / all (mặc định vi)")
    c.add_argument("--dich", action="store_true",
                   help="Chấp nhận bản máy dịch nếu không có phụ đề gốc đúng tiếng")
    c.add_argument("--in-ra", action="store_true", help="In luôn nội dung ra màn hình")
    c.add_argument("--giu-vtt", action="store_true", help="Giữ lại file .vtt gốc có mốc thời gian")
    c.add_argument("--api", action="store_true",
                   help="Nếu yt-dlp không lấy được thì thử qua API (video riêng tư của kênh mình)")
    c.set_defaults(func=lenh_phu_de)

    d = sp.add_parser("dang", help="Đăng video lên kênh")
    d.add_argument("duong_dan", help="Đường dẫn file video")
    d.add_argument("--tieu-de", required=True, help="Tiêu đề (tối đa 100 ký tự)")
    d.add_argument("--mo-ta", default="", help="Mô tả (tối đa 5000 ký tự)")
    d.add_argument("--tag", default="", help="Các tag, phân tách bằng dấu phẩy")
    d.add_argument("--che-do", default="private", choices=["private", "unlisted", "public"],
                   help="Mặc định private cho an toàn")
    d.add_argument("--anh-bia", help="Đường dẫn ảnh bìa (jpg/png, dưới 2MB)")
    d.add_argument("--playlist", help="ID playlist muốn thêm video vào")
    d.add_argument("--hen", help="Hẹn giờ công khai, dạng 2026-08-05T09:00:00Z")
    d.add_argument("--danh-muc", default="22",
                   help="categoryId, mặc định 22 = People & Blogs")
    d.add_argument("--ngon-ngu", default="vi")
    d.add_argument("--thu", action="store_true", help="Chạy khô — in ra rồi dừng, không đăng")
    d.set_defaults(func=lenh_dang)

    args = p.parse_args()
    _dat_tai_khoan(args.tk)
    try:
        args.func(args)
    except HttpError as e:
        chi_tiet = str(e)
        if "quotaExceeded" in chi_tiet:
            sys.exit("HẾT HẠN NGẠCH NGÀY (10.000 đơn vị). Hạn ngạch reset lúc 14:00 giờ VN.")
        if e.resp.status == 401:
            sys.exit("Token không còn hiệu lực. Chạy:  python tools/yt.py xin-quyen --lai")
        if e.resp.status == 403 and "accessNotConfigured" in chi_tiet:
            sys.exit("API chưa được bật. Vào Google Cloud Console bật "
                     "'YouTube Data API v3' và 'YouTube Analytics API' cho project.")
        sys.exit(f"Lỗi từ YouTube API:\n{chi_tiet}")
    except KeyboardInterrupt:
        sys.exit("\nĐã dừng.")


if __name__ == "__main__":
    main()
