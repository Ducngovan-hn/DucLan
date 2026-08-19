---
tieu_de: Quy trình đơn hàng — nhận đơn đến trả hàng
loai: khai-niem
ngay_tao: 2026-07-28
ngay_cap_nhat: 2026-07-28
nguon: []
tags:
  - quy-trinh
  - don-hang
  - van-hanh
---

# Quy trình đơn hàng — nhận đơn đến trả hàng

Bảy bước, anh Đức xác nhận 28/07/2026. **LLM chỉ làm bước 3 và bước 6.**

| Bước | Việc | Ai làm |
|---|---|---|
| 1 | Khách nhắn đơn lên nhóm Zalo riêng → anh Đức lên [[cu-phap-dat-bo]] | Anh Đức |
| 2 | Chụp ảnh cú pháp, thả vào `raw/xưởng  bo Đức Lan/Đơn hàng/` | Anh Đức |
| **3** | Ảnh → `production/Tong-hop-don-hang-Xbo-Duc-Lan-2026.xlsx`, chống trùng | **LLM** |
| 4 | Sản xuất, dệt bo | Anh Đức |
| 5 | Lên cú pháp trả hàng trên nhóm Zalo **"Trả hàng"** | Anh Đức |
| 6 | Nhóm Zalo "Trả hàng" → `production/Xưởng Dệt Bo Đức Lan 2026.xlsx` | **LLM** |
| 7 | (đã gộp vào bước 3 và 6) | — |

Cả hai bước của LLM đều **chạy khi anh Đức gõ lệnh**, không tự động theo giờ:
`tổng hợp đơn hàng` và `tổng hợp trả hàng`.

## Công cụ

Mọi việc ghi Excel đi qua `tools/dh.py`. Quy trình chi tiết ở
`.claude/skills/don-hang/SKILL.md`.

| Lệnh | Việc |
|---|---|
| `anh-moi` | Lọc ảnh chưa đọc (theo SHA1), thu nhỏ, in đường dẫn |
| `don-them --json F` | Ghi đơn hàng, tự cấp mã `Ms<n>`, chống trùng 2 lớp |
| `tra-them --json F` | Ghi trả hàng vào khối TRẢ HÀNG của sổ thật |
| `them-khach <mã> <tên>` | Thêm khách mới vào sheet `Code` + `THU NHẬP` |
| `soat` | Rà soát: ngày chưa vào sổ, ảnh chưa đọc, mã dệt lạ, thiếu khổ |
| `xay-tu-dien` | Dựng lại `tools/tu-dien.json` |
| `sua-kho <Ms> <họ> <khổ>` | Điền khổ cho đơn bị THIẾU KHỔ, dựng lại mã dệt |
| `xoa-tra <hàng>...` | Xoá dòng trong khối TRẢ HÀNG (khi lỡ ghi trùng) |
| `don-tra` | Dồn khối TRẢ HÀNG, lấp hàng trống ở giữa |
| `gon-thu-nhap` | Kéo khối tổng THU NHẬP về sát dòng khách cuối |
| `dong-bo-thu-nhap` | Đánh lại STT + đồng bộ định dạng sheet THU NHẬP |

**Vì sao không dùng `delete_rows` khi xoá dòng trả hàng:** cột `A` có công thức `=MONTH(B)`
trải sẵn tới hàng 637, và khối CHI PHÍ (`L–P`) nằm **cùng hàng nhưng độc lập** với khối
TRẢ HÀNG. Xoá cả hàng sẽ kéo lệch cả hai. Nên `xoa-tra` chỉ xoá nội dung 4 ô `B–E`, còn
`don-tra` dồn dữ liệu trong đúng 4 cột đó.

Thêm `--thu` để chạy khô, không ghi gì.

## Ba lớp an toàn

1. **Sao lưu trước mỗi lần ghi** → `production/don-hang/sao-luu/`, giữ 30 bản.
2. **Chặn khi file đang mở trong Excel** — phát hiện qua file khoá `~$<tên>.xlsx`.
3. **Không đoán bừa.** Mã dệt không có trong 835 mã thật, hoặc tên khách khớp mờ dưới
   85% → **không ghi**, in cảnh báo chờ anh Đức xác nhận.

## Chống trùng

- **Đơn hàng:** (a) SHA1 của ảnh — mỗi ảnh đọc đúng một lần vĩnh viễn;
  (b) khoá nghiệp vụ `ngày + mã KH + mã dệt + màu + SL`.
- **Trả hàng:** khoá `ngày + mã KH + thành tiền` — **cố ý KHÔNG có nội dung**. Cùng một
  lần trả hàng, anh Đức viết trong sổ và viết trên Zalo khác nhau (`xanh biển 150b` so với
  `xanh biển 150 bộ`); đưa nội dung vào khoá thì không bắt được trùng và tiền bị cộng đôi.
  Cộng thêm mốc ngày đã đọc lưu trong `production/don-hang/da-xu-ly.json`.

## Nguyên tắc tiết kiệm token

Việc duy nhất tốn token là **đọc chữ trên ảnh và trên tin nhắn Zalo**. Mọi việc còn lại
do script làm. Ảnh chụp Zalo rất nhỏ (339×109 và 552×201 px) nên chỉ ~150–250 token/ảnh.

Xem thêm [[cu-phap-dat-bo]] · [[doanh-thu-that]].
