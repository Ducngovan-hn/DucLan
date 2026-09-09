---
description: Cất footage iPhone vào kho theo ngày, tự phân loại xưởng-bo / cá-nhân (my-life), verify hash. Chạy tối sau khi quay.
argument-hint: "[đường dẫn thư mục nguồn — bỏ trống = tự chép từ iPhone]"
---

# /offload $ARGUMENTS

Cất footage hôm nay cho an toàn + **tách 2 kho**: content xưởng ↔ ảnh/video cá nhân.
**Không tự đăng, không xoá nguồn iPhone.**

## Hai kho đích
| Kho | Đường dẫn | Chứa |
|---|---|---|
| Cá nhân (mặc định) | `C:\Users\admin\footage-content\my-life` | gia đình, em bé, ăn uống, chạy bộ, mua sắm... |
| Xưởng bo | `C:\Users\admin\footage-content\2026-content-xuong-bo` | vải/bo/cổ/cạp, máy dệt, sợi, kho hàng, Zalo/chuyển khoản đơn hàng, sổ ghi việc xưởng, nhuộm... |

Tiêu chí xưởng (đã chốt với anh Đức): mọi thứ **liên quan công việc/kinh doanh xưởng** →
xưởng; **hoá đơn ăn uống/nhà hàng, screenshot & ghi chú cá nhân (marathon, học tiếng Trung,
cộng đồng PTL), đời sống gia đình** → my-life. **Không chắc → để my-life** (an toàn đời tư).

## Cách chạy (Claude làm tuần tự)

1. **Lấy footage về thư mục tạm.**
   - Có `$ARGUMENTS` → dùng làm nguồn.
   - Bỏ trống → tự chép từ iPhone qua MTP (PowerShell `Shell.Application`, `Namespace(17)` →
     `Apple iPhone` → `Internal Storage` → thư mục tháng `YYYYMM__`, lọc file **hôm nay** theo
     ngày sửa) sang `C:\Users\admin\iphone-tam`. Chép nền nếu nặng, chờ đủ số file.

2. **Đổ vào my-life + sinh bản nhẹ** (Python, không token):
   ```
   PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python tools/to_chuc_kho.py --from "<nguồn>" --drive "C:\Users\admin\footage-content\my-life" --root-name ""
   ```
   → tách `photo/ video/ audio/<ngày>/iphone/`, index EXIF, bản nhẹ. Chờ `✅ VERIFY ĐỦ`.

3. **Tạo lưới phân loại** (Python, không token) — chỉ ngày vừa offload:
   ```
   PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python tools/phanloai_montage.py --kho "C:\Users\admin\footage-content\my-life" --ngay <YYYY-MM-DD>
   ```

4. **Claude đọc lưới** `my-life\_phanloai\<ngày>\grid-NN.jpg` (Read) đối chiếu `map.json`,
   ghi `my-life\_phanloai\<ngày>\quyet-dinh.json` = `{"xuong":[ô...], "khong_chac":[ô...]}`.
   Chỉ liệt kê ô **chắc chắn** là xưởng vào `xuong`.
   - **Ảnh ủy nhiệm chi / biên lai chuyển khoản thanh toán** (screenshot app ngân hàng —
     Techcombank/Vietcombank "Chuyển thành công"...) → **XÓA, KHÔNG LƯU** (anh Đức chốt 05/09).
     Nếu cần số cho chi tiêu, ĐỌC số ghi vào nhật ký trước rồi xóa file (full-res + bản nhẹ).
     Ghi các ô này vào nhóm `"xoa":[ô...]` trong quyet-dinh.json để xóa khỏi kho.
   - **Nếp tự động (script lo):** có bản chỉnh sửa `IMG_E<num>` thì bản gốc `IMG_<num>` đã bị
     `to_chuc_kho.py` loại từ bước 2 — chỉ còn bản edit.

5. **Xóa ảnh ủy nhiệm chi** (nhóm `xoa`): rm full-res + bản nhẹ của các ô đó trong my-life,
   rồi `reindex_kho.py`. **Tách phần xưởng sang kho xưởng** (Python, không token):
   ```
   PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python tools/phanloai_apdung.py --tu "C:\Users\admin\footage-content\my-life" --den "C:\Users\admin\footage-content\2026-content-xuong-bo" --nhom xuong
   ```
   → chờ `✅ VERIFY ĐỦ` (tổng file trước=sau). Phần không phải xưởng ở lại my-life.

6. **Dọn** `my-life\_phanloai\<ngày>` sau khi verify. **Báo cáo** anh Đức: số file mỗi kho,
   danh sách `khong_chac` để soát.

## Sau khi xong
Gợi ý `/kich-ban-dung` để dựng video + xuất 3 gói đăng (từ footage kho xưởng).

## Luật cứng
- Chưa `✅ VERIFY ĐỦ` → chưa an toàn. Script **không bao giờ xoá nguồn iPhone**.
- Chưa có backup #2 → **giữ nguyên footage trên iPhone**.
- Không chắc xưởng hay cá nhân → **để my-life**, đưa vào `khong_chac` cho anh Đức soát.
- Muốn kéo 1 mục cá nhân ngược về xưởng (hoặc ngược lại): chạy `phanloai_apdung.py` với
  `--nhom`/`--tu`/`--den` phù hợp.
