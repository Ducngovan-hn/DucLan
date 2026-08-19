# dmo-routine.ps1 — Chạy báo cáo DMO qua Claude CLI (headless) cho Task Scheduler.
#   Dùng: powershell -ExecutionPolicy Bypass -File tools\dmo-routine.ps1 -Khung sang|trua|toi
# Claude sẽ đọc file DMO, tính %, ghi báo cáo lên Lịch Google (qua Composio), tạo DMO mai (khung toi).
param(
  [ValidateSet("sang","trua","toi")]
  [string]$Khung = "trua"
)

$ErrorActionPreference = "Stop"
$Vault = "C:\Users\admin\DucLan"
$Claude = "C:\Users\admin\.local\bin\claude.exe"
Set-Location $Vault

$Hom = Get-Date -Format "yyyy-MM-dd"
$Mai = (Get-Date).AddDays(1).ToString("yyyy-MM-dd")

switch ($Khung) {
  "sang" {
    $Prompt = @"
Đọc file production/dmo/DMO-$Hom.md trong vault này. Nếu chưa có, tạo bằng: python tools/dmo.py tao
Tóm tắt 6 việc hôm nay + khung giờ, nhắc 'ăn con ếch trước'. Ghi tóm tắt vào MÔ TẢ một event
Lịch Google tên '📊 Báo cáo DMO sáng' lúc 07:00 hôm nay (Composio googlecalendar account hn,
timezone Asia/Ho_Chi_Minh, create_meeting_room=false). Trả lời tiếng Việt, ngắn gọn.
"@
  }
  "trua" {
    $Prompt = @"
Trong vault này chạy: python tools/dmo.py bao-cao --ngay $Hom
Lấy dòng 'TIẾN ĐỘ: n/N việc · P%' và danh sách việc còn tồn. Ghi vào MÔ TẢ một event Lịch Google
tên '📊 Báo cáo DMO giữa ngày' lúc 12:00 hôm nay (Composio googlecalendar account hn,
Asia/Ho_Chi_Minh, create_meeting_room=false). Nêu rõ việc chưa xong. Trả lời tiếng Việt, ngắn gọn.
"@
  }
  "toi" {
    $Prompt = @"
Trong vault này, làm tuần tự:
1) python tools/dmo.py bao-cao --ngay $Hom  → lấy % cuối ngày + việc tồn.
2) python tools/dmo.py tao --ngay $Mai  → tạo DMO ngày mai.
3) python tools/dmo.py lich --ngay $Mai  → lấy JSON 6 việc, rồi tạo các event tương ứng trên Lịch Google
   (Composio googlecalendar account hn, Asia/Ho_Chi_Minh, create_meeting_room=false).
4) Ghi tổng kết % vào MÔ TẢ event '📊 Tổng kết DMO' lúc 22:00 hôm nay.
Trả lời tiếng Việt, ngắn gọn tình hình đã làm.
"@
  }
}

& $Claude -p $Prompt --permission-mode bypassPermissions
