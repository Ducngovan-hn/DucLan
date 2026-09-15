#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dựng biểu đồ đường tiền hàng trả khách mỗi ngày — ĐỌC TỪ DMO (không mò Zalo).

Đọc các file production/dmo/DMO-YYYY-MM-DD.md, lấy dòng "Số khách trả hàng":
- Nếu có "Tổng hàng trả X đ" → lấy X.
- Nếu không → cộng các số tiền ≥ 100.000 trong dòng (bỏ đơn giá kiểu 6.500, 8.500).
Xuất 1 file HTML có biểu đồ đường (SVG thuần, không cần internet).

Dùng: python tools/bieu_do_tra_hang.py 2026-09   (lọc theo tháng)
"""
import re, glob, os, sys, datetime

thang = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().strftime('%Y-%m')
files = sorted(glob.glob(f'production/dmo/DMO-{thang}-*.md'))

data = []
for f in files:
    ngay = os.path.basename(f)[len(f'DMO-{thang}-')-0:].split('-')[-1].replace('.md','')
    # lấy phần ngày (dd) từ tên file
    dd = os.path.basename(f).replace('.md','').split('-')[-1]
    txt = open(f, encoding='utf-8').read()
    m = re.search(r'Số khách trả hàng:.*', txt)
    tien = 0
    if m:
        dong = m.group(0)
        tong = re.search(r'Tổng hàng trả\s*([\d\.]+)', dong)
        if tong:
            tien = int(tong.group(1).replace('.', ''))
        else:
            nums = [int(n.replace('.', '')) for n in re.findall(r'\d{1,3}(?:\.\d{3})+', dong)]
            tien = sum(n for n in nums if n >= 100000)  # bỏ đơn giá (6.500, 8.500…)
    data.append((int(dd), tien))

data.sort()
labels = [f'{d}/9' for d, _ in data]
vals = [t for _, t in data]
mx = max(vals) if vals else 1
mx = max(mx, 1)

# --- Dựng SVG line chart ---
W, H = 900, 420
padL, padR, padT, padB = 70, 30, 40, 60
plotW, plotH = W - padL - padR, H - padT - padB
n = len(vals)
def X(i): return padL + (plotW * i / (n - 1) if n > 1 else plotW / 2)
def Y(v): return padT + plotH * (1 - v / mx)

pts = [(X(i), Y(v)) for i, v in enumerate(vals)]
poly = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)

# lưới ngang + nhãn trục tiền (triệu)
grid = ''
steps = 4
for s in range(steps + 1):
    v = mx * s / steps
    y = Y(v)
    grid += f'<line x1="{padL}" y1="{y:.1f}" x2="{W-padR}" y2="{y:.1f}" stroke="#E5E7EB" stroke-width="1"/>'
    grid += f'<text x="{padL-10}" y="{y+4:.1f}" text-anchor="end" font-size="12" fill="#6B7280">{v/1e6:.0f}tr</text>'

# nhãn trục ngày + điểm + giá trị
xaxis = ''
dots = ''
for i, (x, y) in enumerate(pts):
    xaxis += f'<text x="{x:.1f}" y="{H-padB+20}" text-anchor="middle" font-size="11" fill="#6B7280">{labels[i]}</text>'
    dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#1A56DB"/>'
    if vals[i] > 0:
        dots += f'<text x="{x:.1f}" y="{y-10:.1f}" text-anchor="middle" font-size="10" fill="#111827">{vals[i]/1e6:.2f}</text>'

tong = sum(vals)
ngay_co = sum(1 for v in vals if v > 0)
tb = tong / ngay_co if ngay_co else 0

html = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8">
<title>Biểu đồ tiền trả hàng tháng 9</title>
<style>body{{font-family:system-ui,'Segoe UI',sans-serif;background:#F9FAFB;color:#111827;margin:0;padding:24px}}
.card{{background:#fff;border:1px solid #E5E7EB;border-radius:12px;padding:20px;max-width:940px;margin:auto;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
h1{{font-size:20px;margin:0 0 4px}} .sub{{color:#6B7280;font-size:13px;margin-bottom:16px}}
.stats{{display:flex;gap:24px;margin-top:16px;flex-wrap:wrap}}
.stat b{{display:block;font-size:20px;color:#1A56DB}} .stat span{{font-size:12px;color:#6B7280}}</style></head>
<body><div class="card">
<h1>📈 Tiền hàng trả khách mỗi ngày — Tháng 9/2026</h1>
<div class="sub">Đơn vị: triệu đồng · Nguồn: DMO hằng ngày (Xưởng Dệt Bo Đức Lan)</div>
<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg">
{grid}
<polyline points="{poly}" fill="none" stroke="#1A56DB" stroke-width="2.5" stroke-linejoin="round"/>
{dots}{xaxis}
</svg>
<div class="stats">
<div class="stat"><b>{tong/1e6:.2f} tr</b><span>Tổng cả kỳ</span></div>
<div class="stat"><b>{ngay_co} ngày</b><span>Có trả hàng</span></div>
<div class="stat"><b>{tb/1e6:.2f} tr</b><span>TB/ngày có đơn</span></div>
<div class="stat"><b>{mx/1e6:.2f} tr</b><span>Ngày cao nhất</span></div>
</div></div></body></html>'''

out = f'production/dmo/bieu-do-tra-hang-{thang}.html'
open(out, 'w', encoding='utf-8').write(html)
print('Da tao', out)
for d, t in data: print(f'{d}/9: {t:,}'.replace(',', '.'))
print('TONG:', format(tong, ',').replace(',', '.'))
