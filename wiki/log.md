---
tieu_de: Nhật ký hoạt động
loai: tong-quan
ngay_tao: 2026-07-06
ngay_cap_nhat: 2026-07-17
nguon: []
tags:
  - nhat-ky
  - log
---

# Nhật ký hoạt động (append-only — chỉ thêm, không sửa mục cũ)

> Nhật ký **CHỈ-THÊM**, theo thời gian. Không sửa mục cũ — chỉ thêm mục mới ở cuối.
> Mỗi mục bắt đầu bằng tiền tố `## [YYYY-MM-DD] <loại> | ...` để grep được.
> Lấy 5 mục gần nhất: `grep "^## \[" wiki/log.md | tail -5`.
>
> Các loại: `ingest` (nạp nguồn) · `query` (truy vấn đáng lưu vết) · `lint` (rà soát) · `init` (khởi tạo hệ thống).

---

## [2026-07-06] init | Khởi tạo hệ thống "Bộ Não Thứ Hai" (lần đầu)
Tạo cấu trúc ba tầng (`raw/`, `wiki/`, `production/`), schema `CLAUDE.md`, và các file khởi tạo `wiki/index.md`, `wiki/log.md`, `wiki/tong-quan.md`.

## [2026-07-17] init | Khởi tạo lại hệ thống hôm nay — thay thế toàn bộ file schema
Thiết lập lại toàn bộ hệ thống theo yêu cầu: ghi đè `CLAUDE.md`, `wiki/index.md`, `wiki/log.md`, `wiki/tong-quan.md` bằng phiên bản mới; đảm bảo đủ các thư mục `wiki/thuc-the/`, `wiki/khai-niem/`, `wiki/tom-tat-nguon/`, `wiki/so-sanh/`, `raw/assets/`, `production/`. Wiki hiện rỗng; `raw/` chưa có file `.srt` nào — sẵn sàng nạp nguồn đầu tiên.

## [2026-07-25] update | Thêm 3 thư mục nghiệp vụ + format họp cho Query
Tạo `wiki/products/`, `wiki/customers/`, `wiki/competitors/` và ba `loai` tương ứng (`san-pham`, `khach-hang`, `doi-thu`) trong `CLAUDE.md` + `wiki/index.md`. Bổ sung mục 6.1 vào quy trình TRUY VẤN: format đầu ra "Tóm tắt 1 trang cho cuộc họp" (khung Mục tiêu / Bối cảnh / Điểm chính / Số liệu / Rủi ro / Đề xuất hành động / Câu hỏi mở, giới hạn 1 trang, vẫn trích dẫn đầy đủ, lưu ra `production/` nếu cần).

## [2026-07-27] query | Tóm tắt chi tiết bài học sách 'Cào Cào Lên Dốc' (Phạm Thành Long, flipbook long.aflip.in/caocao.html) thành 6 file Word theo Phần, lưu tại raw/sách-Thầy-Phạm-Thành-Long/

## [2026-07-27] lint | Rà soát 6 file Word tóm tắt so với 22 trang "Sổ Tay Đường Đời" gốc
Đối chiếu từng mục (bài học / chiến lược / việc cụ thể / thước đo / lời dặn). Mọi mô hình và con số đều đủ và đúng. Bổ sung 3 ý bị sót rồi build lại file: Chương 1 (lời dặn "bỏ qua bước định vị thì mọi bước sau đều trượt"), Chương 7 (tục ngữ "một nghề thì sống, đống nghề thì chết"), Chương 20 ("tiền khôn nhất là tiền vừa đẻ ra tiền, vừa làm ra điều có ý nghĩa"). Không phát hiện lỗi số liệu.

## [2026-07-27] ingest | Sách "Cào Cào Lên Dốc" — Phạm Thành Long (6 file Word trong raw/sách-Thầy-Phạm-Thành-Long/)
Tạo 17 trang mới: 1 tóm tắt nguồn ([[sach-cao-cao-len-doc]]); 2 thực thể ([[pham-thanh-long]], [[danh-thuc-su-giau-co]]); 13 khái niệm ([[bon-nac-thang-giau-co]], [[tai-san-va-tieu-san]], [[nhiet-ke-tai-chinh]], [[kim-tu-do]], [[nep-ngay-dmo]], [[diem-a-diem-b]], [[sau-cai-lo]], [[chon-ngach-5-yeu-to]], [[quy-trinh-ban-hang]], [[nam-don-bay-doanh-so]], [[doanh-nghiep-tu-van-hanh]], [[marketing-giang-luoi]], [[thuong-hieu-ca-nhan]], [[don-bay-muon-suc]], [[fan-cuong]], [[dau-tu-de-hat-nay-mam]], [[cho-di]]); 1 trang so sánh ([[bon-nac-thang-ap-vao-det-bo-duc-lan]]). Cập nhật `index.md` (mục lục nhóm theo nấc thang) và `tong-quan.md` (hiện trạng nguồn + khoảng trống dữ liệu).
Không phát hiện mâu thuẫn với nguồn cũ (wiki trước đó rỗng). Ghi rõ nguồn gốc mô hình theo Phụ lục sách: Kiyosaki (tài sản–tiêu sản, Kim Tứ Đồ), T. Harv Eker (6 cái lọ JARS). Các phần suy luận áp vào nghiệp vụ Đức Lan đều gắn nhãn "nhận định của LLM", kèm 3 câu hỏi mở cần anh Đức trả lời để thành dữ kiện.

## [2026-07-27] query | Báo cáo rà soát 2 tuần (13/07–27/07/2026) + đánh giá chiến lược
Tổng hợp từ ba nguồn dấu vết: file trong `raw/` (6 hóa đơn chính thức 00000022–00000027, 7 nháp, mẫu GDO80x16, `tai-san.xlsx`), git log hai vault (`DucLan`, `my-life`), và transcript 24 phiên Claude trong 14 ngày. Số liệu tài chính tính từ `raw/tai-san.xlsx`: tổng tài sản 5,053 tỷ — còn nợ 660 tr — tài sản ròng 4,393 tỷ; tiền mặt 0.
Ba phát hiện chính (nhận định của LLM): (1) wiki 24 trang đều về sách, ba thư mục `products/`/`customers/`/`competitors/` vẫn rỗng trong khi `raw/` có 5.090 file — hạ tầng dựng xong nhưng chưa nạp dữ liệu của chính xưởng; (2) đang ở nấc 2 nhưng tiêu thời gian vào việc nấc 3 (web/nhận diện/video) trong khi chưa đo bất kỳ chỉ số nào của [[nam-don-bay-doanh-so]]; (3) rủi ro bảo mật — mật khẩu và JWT token bị dán vào transcript ngày 21/7.
Sản phẩm: `production/bao-cao-2-tuan-2026-07-13-den-2026-07-27.md`.

## [2026-07-27] ingest | Sổ sách HKD — 26 hoá đơn bán hàng PDF + 16 hoá đơn nháp + thông báo thuế (raw/xưởng  bo Đức Lan/Sổ sách HKD/Hóa đơn bán hàng/)
Nạp nguồn kinh doanh ĐẦU TIÊN vào wiki — trước phiên này toàn bộ 24 trang wiki đều nói về một cuốn sách, ba thư mục `products/`, `customers/`, `competitors/` rỗng hoàn toàn.

**Đã đọc:** 26 hoá đơn chính thức `2C26TYY_00000001`–`00000027` (26/05/2026 → 23/07/2026), 16 hoá đơn nháp, và `Thông báo ko cấp mã.pdf`.

**Sản phẩm ra lò:** `production/bang-so-van-hanh.xlsx` — 4 sheet (Hoá đơn / Theo tuần / Theo khách / Hướng dẫn cập nhật), 225 công thức, quy ước màu đồng bộ `raw/tai-san.xlsx` (chữ xanh dương = nhập tay, chữ xanh lá = công thức, nền vàng = ô anh Đức cần điền).

**Trang mới — 7:** 5 khách hàng ([[co-huyen]], [[c-nhi]], [[c-vi]], [[hieu]], [[cty-bform]]) + 2 sản phẩm ([[gdo80x16]], [[ga90x12]]). Cập nhật `index.md` hai hạng mục Sản phẩm và Khách hàng.

**Sáu con số của 2 tuần 13/07–27/07/2026 (dữ kiện, tính từ hoá đơn):** doanh thu 38.092.500 đ · 6 đơn · 3 pháp nhân (4 tên gọi) · đơn trung bình 6.348.750 đ · chi phí CHƯA CÓ · lãi gộp CHƯA TÍNH ĐƯỢC. Doanh thu luỹ kế toàn kỳ 26/05–23/07: 158.736.500 đ / 26 đơn / 10 khách.

**Bốn phát hiện then chốt:**
1. **"cô Huyền" và "c Huyền" LÀ MỘT NGƯỜI** — cả 4 hoá đơn + 3 nháp đều ghi cùng CÔNG TY TNHH ĐỒNG PHỤC HÀ ANH, MST 0111018330, cùng địa chỉ. Đã kiểm chứng, không phải suy đoán.
2. **"c Nhi" và "c Vi" cùng một pháp nhân** — CÔNG TY TNHH LAIFUDE VINA, MST 0108137401 (mã LFD). Là hai đầu mối liên hệ, không phải hai khách. Tách hai trang wiki nhưng ghi rõ quan hệ. Hoá đơn 00000011 tên file ghi "c Vi" nhưng ô người mua ghi "C Nhi" → chưa kết luận được là một hay hai người, để thành câu hỏi mở.
3. **Hoá đơn số 00000021 bị thiếu — đã tìm ra lý do.** Cơ quan thuế ra Thông báo 262050412090 ngày 15/07/2026 từ chối cấp mã, lỗi 20019 "Chữ ký chưa được đăng ký". Đơn đó chính là nháp `C Huyền 15.7` (10.045.000 đ), được xuất lại thành hoá đơn 00000022 ngày 16/7. Không mất doanh thu, nhưng lỗi cấu hình chữ ký số chưa rõ đã xử lý dứt điểm chưa.
4. **Cty Bform vẫn chưa có hoá đơn chính thức nào tính đến 27/07/2026.** Nháp 22/7 (600 Bộ × 6.000 = 3,6 tr) ĐÃ HUỶ (anh Đức xác nhận 27/7); nháp đang dùng là 27/7 (1.200 Bộ × 6.000 = 7,2 tr) — gấp đôi số lượng, giữ nguyên giá. File nháp 22.7 giữ nguyên trong `raw/` theo quy tắc bất biến, chỉ ghi nhận việc huỷ tại trang wiki.

**Khoảng trống dữ liệu đã ghi nhận (không bịa số):** (a) hoá đơn MISA KHÔNG ghi mã mẫu dệt / khổ / màu → không nối được mẫu với khách, cột "Mẫu/Khổ" và "Màu" để trống nền vàng; (b) chưa có dữ liệu chi phí tuần → cột lãi gộp để công thức sẵn nhưng trống; (c) chưa có giá vốn của [[gdo80x16]] và [[ga90x12]] → hai trang sản phẩm để bảng giá vốn TRỐNG kèm 9 và 10 câu hỏi cụ thể.

**Mâu thuẫn số liệu cần anh Đức phân xử:** hoá đơn 00000017 là hoá đơn điều chỉnh cho 00000012 (sai đơn vị tính Bộ→Cái) nhưng ghi "điều chỉnh TĂNG 84.000". Đang tính cả hai vào doanh thu (868.000 đ cho [[c-vi]], 158.736.500 đ toàn kỳ). Nếu chỉ là sửa đơn vị tính thì phải trừ 84.000 → 784.000 đ và 158.652.500 đ.

**Ghi chú kỹ thuật:** máy không có LibreOffice lẫn Excel COM nên KHÔNG chạy được recalc để nạp giá trị đệm vào file xlsx. Đã bù bằng hai việc: (1) đặt `fullCalcOnLoad = True` để Excel tự tính lại khi mở; (2) viết script kiểm tra độc lập bằng Python — đối chiếu từng phạm vi tham chiếu, kiểm tra tổng doanh thu theo tuần khớp tổng toàn kỳ, tổng số khách/tuần khớp helper column, thứ tự sắp xếp giảm dần theo doanh thu. Tất cả đều khớp.

## [2026-07-28] update | Tự động hoá bước 3 và bước 6 của quy trình đơn hàng

Anh Đức chốt lại quy trình 7 bước và giao cho LLM đúng **hai** việc: bước 3 (ảnh cú pháp đặt bo → Excel đơn hàng) và bước 6 (nhóm Zalo "Trả hàng" → sổ thật). Các bước còn lại anh Đức tự làm, kể cả việc lên cú pháp và gửi tin nhắn Zalo. Cả hai việc chạy **khi anh gõ lệnh**, không tự động theo giờ.

**Đã dựng:**
- `tools/dh.py` — CLI duy nhất, mọi thao tác ghi Excel đi qua đây. Lệnh: `anh-moi`, `don-them`, `tra-them`, `them-khach`, `them-alias`, `mo-rong-thu-nhap`, `sua-file-don`, `soat`, `xay-tu-dien`, `ma-det`. Thêm `--thu` để chạy khô.
- `tools/tu-dien.json` — 835 mã dệt có thật (quét từ `raw/.../Thiết kế/`), 44 mã KH, 12 mã chi phí, 262 alias tên khách.
- `.claude/skills/don-hang/SKILL.md` — quy trình gọn cho mỗi phiên.
- Ba trang khái niệm: [[quy-trinh-don-hang]], [[cu-phap-dat-bo]], [[doanh-thu-that]].

**Bốn quy tắc anh Đức xác nhận 28/07/2026:**
1. Đuôi mã dệt: "Trơn"→`T`, "Kẻ"→`K`, "2 kẻ chân"→`TH`, còn lại→không đuôi + `(usb)`. Bẫy: phải kiểm "2 kẻ chân" TRƯỚC "kẻ".
2. **1 bộ = cổ + tay** → mỗi dòng "N bộ" tách thành 2 dòng; khổ tay mặc định `72x3`, kiểu tay theo kiểu của cổ.
3. Mỗi màu ghi một dòng riêng trong ô Màu sắc.
4. Thiếu khổ thì vẫn ghi đơn, ô Mẫu dệt để trống + đánh dấu `⚠ THIẾU KHỔ`.

**Phát hiện quan trọng — doanh thu thật khác số nộp thuế hơn 7 lần.** Sổ `Xưởng Dệt Bo Đức Lan 2026.xlsx` ghi doanh thu 2026 lũy kế **1.158.185.500 đ**, trong khi 26 hoá đơn chỉ có 158.736.500 đ. Anh Đức xác nhận hoá đơn **chỉ để tổng hợp tiền nộp thuế**, không phải doanh thu. Hệ quả: `production/bao-cao-2-tuan-2026-07-13-den-2026-07-27.md` và `production/bang-so-van-hanh.xlsx` dựng trên số hoá đơn → mọi con số "doanh thu" trong đó thực chất là số thuế. Đã ghi cảnh báo tại [[doanh-thu-that]].

**Phẫu thuật sheet THU NHẬP (chạy một lần).** Sheet có 31 khách kín chỗ ở r3–r33, ô tổng r34 = `SUM(x3:x33)`, và **13 công thức bên ngoài** trỏ thẳng vào r34 (`LỢI NHUẬN!B4..M4` và `CHI PHÍ!Q5`). Không dời thì không thêm được khách mới, mà thêm sai thì doanh thu khách mới **biến mất khỏi bảng lãi lỗ**. Đã dời khối tổng xuống r60, nới vùng cộng thành r3:r59 (chừa 26 chỗ), trỏ lại đủ 13 công thức. Kiểm chứng: mô phỏng lại toàn bộ công thức bằng Python, doanh thu 7 tháng và tổng năm khớp **tuyệt đối** với giá trị Excel đang cache, không lệch một đồng.

**Ba lớp an toàn khi ghi:** sao lưu trước mỗi lần ghi (giữ 30 bản trong `production/don-hang/sao-luu/`); chặn khi file đang mở trong Excel (dò file khoá `~$`); không đoán bừa — mã dệt lạ hoặc tên khách khớp mờ dưới 85% thì không ghi, chỉ cảnh báo. Ngưỡng 85% chọn có căn cứ: ở mức 72% thì "Mai Liên" bị khớp sai thành "C Hà Liên".

**Chống trùng hai lớp cho đơn hàng:** SHA1 của ảnh (mỗi ảnh đọc đúng một lần vĩnh viễn) + khoá nghiệp vụ `ngày + mã KH + mã dệt + màu + SL`. Đã kiểm: chạy lệnh hai lần liên tiếp thì lần hai báo 0 dòng mới.

**Sửa file đơn hàng 2026:** đổi tên sheet thành `Đơn hàng 2026`, xoá khối tổng lỗi `#REF!` đang chắn giữa vùng dữ liệu ở H6:J9, dựng lại khối tổng ở N4:P11 bằng `SUMIF` ngoài vùng dữ liệu, thêm cột L `Mã KH` để nối được với sổ thật.

**Cú pháp đặt bo — hoá ra là ảnh chụp tin nhắn Zalo, không phải chữ viết tay.** Hai ảnh đầu tiên rất nhỏ (339×109 và 552×201 px) nên chỉ tốn ~150–250 token/ảnh, rẻ hơn nhiều so với dự tính ban đầu (1.500 token).

**Việc còn treo:** (a) sổ trả hàng dừng ở 18/07, còn 10 ngày chưa vào sổ; (b) đơn Bform 28/7 thiếu khổ, cần anh Đức điền; (c) `Ga50x12` và `Ga80x9` trong sổ cũ vẫn không có file thiết kế nào; (d) Ms59 vẫn chưa rõ của khách nào.

## [2026-07-28] ingest | Nhóm Zalo "TRẢ HÀNG" 18–27/07 → sổ thật

Lần đầu chạy bước 6 của [[quy-trinh-don-hang]]. Đọc nhóm Zalo "❌: 📔 TRẢ HÀNG 💵💵💵" qua Chrome, lấy các lần trả hàng từ mốc 18/07 tới nay.

**Kết quả:** ghi **18 dòng, tổng 88.661.500 đ** vào `production/Xưởng Dệt Bo Đức Lan 2026.xlsx`, sheet `TỔNG HỢP` khối TRẢ HÀNG (hàng 237–254). Sổ tăng từ 236 lên 254 dòng; doanh thu 2026 từ 1.158.185.500 đ lên **1.246.847.000 đ**, tháng 7 từ 154.496.500 đ lên **243.158.000 đ**. Chống trùng loại đúng 3 dòng ngày 18/07 đã có sẵn; chạy lại lần hai loại sạch cả 21 dòng.

**Hai khách mới phải thêm vào sổ:** `bform` = Cty Bform, `hieu` = Hiếu. Trước đó phải mổ sheet `THU NHẬP` một lần — 31 khách kín chỗ r3–r33, ô tổng r34 bị 13 công thức ngoài trỏ vào. Đã dời khối tổng xuống r60, nới vùng cộng r3:r59, trỏ lại đủ 13 công thức. Mô phỏng lại toàn bộ: doanh thu 7 tháng và tổng năm khớp tuyệt đối trước/sau khi mổ.

**Sổ ĐÃ THIẾU 2 lần trả hàng ngày 18/07** mà trước nay không ai biết: c Tuấn Huyền 947.500 đ và c Hằng 975.000 đ. Nếu không đọc lại Zalo thì hai khoản này mất hẳn.

**Ba lỗi tự tìm ra và sửa trong phiên:**
1. `anh-moi` chạy lần hai vẫn báo còn ảnh cần đọc — file trạng thái lưu hash rút gọn 10 ký tự nhưng so bằng hash đầy đủ 40 ký tự. Hậu quả nếu để sót: mỗi lần chạy đọc lại toàn bộ ảnh cũ, tốn token vô ích.
2. `them-khach` báo "chưa mở rộng THU NHẬP" dù đã mở rộng — dùng "D34 rỗng" làm dấu hiệu, nhưng r34 bị chính khách mới đầu tiên chiếm chỗ. Đổi sang nhận diện bằng sự có mặt của khối tổng ở r60.
3. Regex mã KH chỉ cho chữ thường, trong khi sổ có sẵn mã viết hoa `Nhungth`.

**Một báo động giả cần ghi lại để không lặp:** phép đối chiếu mã KH ban đầu phân biệt hoa/thường nên báo `Nhungth` bị rơi 2,6 tr khỏi `THU NHẬP`. Thực tế **SUMIFS của Excel KHÔNG phân biệt hoa/thường** — sheet Code ghi `Nhungth`, THU NHẬP ghi `nhungth`, vẫn cộng đúng. Đã sửa `soat` so khớp hạ chữ thường và thêm hẳn phép kiểm "mã KH có giao dịch nhưng thiếu dòng THU NHẬP → tiền không lên LỢI NHUẬN".

**Phát hiện lớn — nhóm CV Xưởng Bo là nguồn tốt hơn ảnh.** Chi tiết ở [[cu-phap-dat-bo]]. Hai hệ quả: (a) quy ước "khổ tay mặc định 72x3" là SAI, Bform dùng `Ta75x3`; (b) mã `Ms<n>` thật đã tới **Ms81** trong khi script cấp từ Ms61 nên hai đơn vừa ghi (Ms61 Hoàng Giang, Ms62 Bform) mang mã không đúng thực tế. Anh Đức quyết: vẫn đọc từ ảnh, việc lệch mã Ms để xử lý sau.

**Bước 3 cũng chạy trong phiên:** ghi 4 dòng (2 đơn) vào `Tong-hop-don-hang-Xbo-Duc-Lan-2026.xlsx` từ 2 ảnh trong `raw/xưởng  bo Đức Lan/Đơn hàng/`. Ảnh là ảnh chụp tin nhắn Zalo, rất nhỏ (339×109 và 552×201 px) nên chỉ tốn ~150–250 token/ảnh.

## [2026-07-28] lint | Đính chính mục ingest cùng ngày — 2 dòng trả hàng bị ghi trùng

Anh Đức phát hiện và báo. Hai điều mục ingest phía trên ghi SAI:

**1. KHÔNG có chuyện "sổ thiếu 2 lần trả hàng ngày 18/07".** Sổ đã có sẵn đủ 5 dòng ngày 18/07 tại hàng 232–236. Khi kiểm tra, chỉ nhìn 3 dòng cuối (234–236) rồi kết luận sổ chỉ có 3 dòng — sai. Hai dòng r232 (`huyen`, 947.500 đ) và r233 (`hangvp`, 975.000 đ) vẫn nằm đó từ trước.

**Hậu quả:** đã ghi thêm 2 dòng trùng ở r237–r238, cộng khống **1.922.500 đ** vào doanh thu tháng 7. Đã xoá bằng lệnh mới `dh.py xoa-tra 237 238`. Số đúng sau khi sửa: tháng 7 = **241.235.500 đ**, cả năm 2026 = **1.244.924.500 đ** (không phải 243.158.000 và 1.246.847.000 như mục trước).

**Nguyên nhân gốc — khoá chống trùng quá chặt.** Khoá cũ gồm cả nội dung: `ngày + mã KH + nội dung + thành tiền`. Cùng một lần trả hàng nhưng anh Đức viết trong sổ và viết trên Zalo khác nhau — `xanh biển 150b` so với `xanh biển 150 bộ`, `bo áo khoác 4.5kg + trắng 110 cổ` so với `bo áo khoác sz90: 53 + sz50: 25 = 4,5kg + trắng 110 cổ`. Khoá không khớp nên lọt. Đã đổi khoá thành `ngày + mã KH + thành tiền`, bỏ hẳn nội dung. Chạy lại kiểm chứng: cả 21 dòng đều bị loại đúng.

**2. Khối tổng sheet THU NHẬP đặt sai chỗ.** Việc dời khối tổng xuống r60 (chừa 26 hàng trống cho khách mới) khiến hàng tổng cách dòng khách cuối tận 24 hàng trống — anh Đức mở file ra tưởng mất hàng tổng. Công thức vẫn đúng nhưng bố cục không dùng được.

Đã sửa cách khác: khối tổng luôn nằm **ngay dưới dòng khách cuối cùng**. Khách mới chiếm đúng hàng đang chứa khối tổng, rồi đẩy khối tổng xuống 1 hàng và trỏ lại 13 công thức ngoài (`LỢI NHUẬN!B4..M4`, `CHI PHÍ!Q5`). Thêm lệnh `dh.py gon-thu-nhap` để kéo khối tổng về sát dữ liệu. Hiện khối tổng ở **r36** (`=SUM(D3:D35)`), ngay dưới `Hiếu` ở r35; hàng cộng theo quý ở r37.

**Bài học ghi lại:** khi kiểm tra một ngày đã có trong sổ hay chưa, phải quét TOÀN BỘ các dòng của ngày đó, không được suy từ vài dòng cuối. Và với sổ tiền, khoá chống trùng nên dựa vào các trường KHÔNG do người gõ tự do (ngày, mã, số tiền), tránh trường mô tả.

## [2026-07-28] lint | Dọn hàng trống khối TRẢ HÀNG + đồng bộ sheet THU NHẬP

Anh Đức yêu cầu dọn nốt hai chỗ còn dở sau lần đính chính ở trên.

**1. Xoá hẳn hàng trống r237–r238.** Sau khi `xoa-tra` xoá 2 dòng ghi trùng, hai hàng đó để trống giữa vùng dữ liệu. Đã thêm lệnh `dh.py don-tra` dồn khối TRẢ HÀNG lên: 248 dòng dữ liệu nay nằm liền mạch ở r5–r252, không còn hàng trống ở giữa.

**KHÔNG dùng `delete_rows`** — lý do phải ghi lại: cột `A` có công thức `=MONTH(B)` trải sẵn tới hàng 637, và khối CHI PHÍ (`L–P`) nằm **cùng hàng nhưng hoàn toàn độc lập** với khối TRẢ HÀNG. Xoá cả hàng sẽ kéo lệch cả hai. Nên `don-tra` chỉ dịch dữ liệu trong đúng 4 cột `B–E`. Đã kiểm chứng: khối CHI PHÍ giữ nguyên vị trí.

**2. Đồng bộ sheet THU NHẬP.** Hai lỗi:
- **STT lộn xộn:** r31=30, r32=31, r33=`'29'` (kiểu CHUỖI chứ không phải số), r34=32, r35=33. Đã đánh lại liền mạch 1–33, tất cả là số nguyên.
- **Định dạng dòng Cty Bform (r34) sai nặng:** chữ xanh trên nền cam ở cột tháng, chữ vàng trên nền đỏ ở cột tổng năm. Nguyên nhân: r34 **trước đây chính là hàng TỔNG** (có định dạng nổi bật); khi thêm khách mới vào đúng hàng đó thì giá trị bị ghi đè nhưng định dạng cũ vẫn còn.

Đã thêm lệnh `dh.py dong-bo-thu-nhap`: lấy một dòng khách sạch làm mẫu rồi chép nguyên `StyleArray` sang toàn bộ vùng khách, hàng TỔNG và hàng cộng theo quý. Phải chép cả StyleArray chứ không dựng `Font()` mới — màu chữ trong sổ dùng theme/indexed color, dựng font mới sẽ làm mất màu gốc.

**Kiểm chứng:** tiền không đổi sau cả hai thao tác — cả năm **1.244.924.500 đ**, tháng 7 **241.235.500 đ**. `soat` báo không thấy vấn đề.

## [2026-07-28] lint | Lỗi công thức gốc làm mất doanh thu mã `giang` — đã sửa

Anh Đức phát hiện mã `giang` (c Giang, Thanh Hóa) bị thiếu doanh thu. Truy ra **lỗi có sẵn trong sổ từ trước**, không phải do lần nhập này.

**Bệnh gốc:** cột `A` (tháng của khối TRẢ HÀNG) và cột `L` (tháng của khối CHI PHÍ) dùng công thức `=MONTH(B)` trải sẵn xuống tận hàng 637 và 365. Ở các hàng chưa có dữ liệu, ô ngày rỗng nên `MONTH(0)` trả về **1** — sinh ra **367 số 1 rác ở cột A** và **270 ở cột L**.

**Vì sao mất tiền:** sheet `THU NHẬP` có **116 ô** dùng dạng `SUMIFS(..., $A:$A, lookup(D$2, $A:$A))` thay vì so trực tiếp. Hàm `LOOKUP` đòi vector tra cứu phải **sắp xếp tăng dần**; đám số 1 rác ở đuôi cột A phá vỡ điều đó, nên `LOOKUP` chạy tìm kiếm nhị phân trên vector không sắp xếp và cho **kết quả không xác định**. Mã `giang` chỉ có đúng **một** giao dịch (14/04/2026, "cam, đỏ", 30.000.000 đ) nên khi cột tháng 4 tra sai là mất trắng cả dòng.

**Đã sửa** bằng lệnh mới `dh.py chuan-hoa-cong-thuc`:
- 976 ô cột tháng: `=MONTH(B)` → `=IF(B="","",MONTH(B))` — hết số 1 rác, vẫn giữ sẵn công thức cho hàng tương lai.
- 116 ô SUMIFS: bỏ `lookup()`, dùng dạng phẳng `SUMIFS(..., $A:$A, D$2)`. Ngắn hơn và đúng vì header tháng ở hàng 2 vốn đã là **số nguyên** (không phải chuỗi như nghi ban đầu).

Cũng sửa `dh.py` chỗ ghi dòng mới quá vùng công thức: nay bù bằng dạng `IF` thay vì `=MONTH(B)`.

**Kiểm chứng bằng mô phỏng SUMIFS trên bản copy:** `c Giang` ra đúng **30.000.000 đ** ở tháng 4; tổng theo từng khách cộng lại khớp tuyệt đối với tổng thô ở cả 7 tháng và cả năm (**1.244.924.500 đ**). Số ô công thức từng sheet không đổi.

**Bài học:** công thức trải sẵn xuống vùng trống là bẫy im lặng — `MONTH` của ô rỗng ra 1 chứ không ra rỗng. Và không dùng `LOOKUP` để so tháng khi đã có `SUMIFS` so trực tiếp; `LOOKUP` trên vector không sắp xếp hỏng âm thầm, không báo lỗi.

## [2026-07-28] query | Báo cáo 2 tuần 14/07–28/07 dựng lại trên SỐ THẬT — thay thế bản 13/07–27/07

Bản báo cáo trước lấy doanh thu từ hoá đơn (số nộp thuế) nên sai nguồn theo [[doanh-thu-that]]. Bản mới tính trực tiếp từ khối TRẢ HÀNG và CHI PHÍ của sổ thật.

**Số thật 14/07–28/07:** doanh thu **145.751.500 đ** · 30 lần trả hàng · **16 khách** · trung bình 4.858.383 đ/lần · chi phí ghi nhận **180.000 đ** (1 dòng). So với bản cũ dựng trên hoá đơn (38.092.500 đ / 6 đơn / 3 khách) thì chênh 3,8 lần doanh thu và 5,3 lần số khách — mọi kết luận cũ về "6 khách im lặng" và "tập trung rủi ro 71%" đều là ảo ảnh do nhìn nhầm nguồn.

**Cả năm 2026 (7 tháng):** doanh thu 1.244.924.500 đ · chi phí ghi nhận 409.568.000 đ. Tháng 7 là tháng bận nhất năm (54 lần trả hàng, 241.235.500 đ, còn 3 ngày mới hết tháng).

**Ba phát hiện chính (nhận định của LLM):**
1. **Sổ chi phí bị bỏ hoang.** 248 dòng trả hàng so với 91 dòng chi phí; tháng 5 có 25 dòng trả hàng nhưng đúng 1 dòng chi phí. Sợi cả năm chỉ ghi 3 lần (13,7% doanh thu, ngành thường 40–55%); lương nhân viên cả năm 13.992.000 đ trong khi riêng lương c Thu tháng 5 đã 4.500.000 đ; khấu hao 0 dòng dù có 10 máy. → Con số chênh 835.356.500 đ KHÔNG phải lợi nhuận.
2. **Khối THU TIỀN (cột G–J) chưa dùng một dòng nào** → không biết ai còn nợ bao nhiêu. Mâu thuẫn với bảng tài sản: sổ chênh 835 tr nhưng ngân hàng 0 đồng, còn nợ 660 tr. Nhận định: tiền có thể đang nằm ở công nợ khách chưa thu.
3. **Trộn mua tài sản vào chi phí** — mục `máy dệt` 87.000.000 đ ghi thẳng vào chi phí thay vì khấu hao, làm méo đường lợi nhuận theo tháng.

**Đánh giá nấc thang cập nhật:** với số thật, anh Đức đang ở **chân nấc 3** (không phải nấc 2 như bản cũ kết luận), nhưng nền nấc 1 bị khuyết ở khâu đo tiền.

Sản phẩm: `production/bao-cao-2-tuan-2026-07-14-den-2026-07-28.md`.


## [2026-07-29] query | Sắp xếp lại Bucket List theo 4 tầng + đánh giá đối chiếu thực trạng

**Việc 1 — sắp xếp bảng.** `production/Bucket List - Những việc muốn làm trong đời.xlsx`
xếp lại 40 mục theo thứ tự ưu tiên anh Đức đưa: **Tôi là… (10) → Tôi xây dựng/tạo ra… (11)
→ Tôi hoàn thành… (15) → Tôi sở hữu… (4)**. Đánh số chạy 1–40, mỗi nhóm chừa 3 dòng trống,
giữ font Times New Roman của bản gốc. Bản gốc đã sao lưu ra scratchpad.

Vài quyết định phân loại: "mỗi năm 1 huy chương FM" → tầng *Tôi là* (cam kết lặp lại, không
phải mốc một lần); "nghỉ 60 ngày xưởng vẫn chạy" → tầng *Xây dựng* (phép thử hệ thống);
"hoàn thành cuốn sách đầu tiên" → tầng *Xây dựng* (giá trị để lại, dù chữ "hoàn thành" nằm
trong câu).

**Việc 2 — đánh giá khách quan.** Đối chiếu bảng với sổ thật và `raw/tai-san.xlsx`.
Sản phẩm: [[danh-gia-bucket-list]].

**Năm khoảng cách chính (nhận định của LLM):**
1. Mục tiêu 100 tỷ lơ lửng vì chưa biết biên lãi thật — xem [[doanh-thu-that]].
2. Doanh thu 2,13 tỷ/năm → 100 tỷ/năm là ×47 lần, cần +47%/năm suốt 10 năm; gia công B2B
   biên mỏng gần như không đạt nếu không đổi mô hình.
3. Quỹ thời gian: riêng các cam kết định kỳ trong bảng đã ~29 h/tuần, cộng điều hành xưởng
   50–60 h/tuần → không còn chỗ cho YouTube + sách + HSK4.
4. Tầng "Sở hữu" có 3/4 mục là **tiêu sản** theo [[tai-san-va-tieu-san]].
5. Định vị lệch nấc: theo tài sản ròng 4,393 tỷ là **nấc 3**; theo tài sản sinh dòng tiền
   (≈ 0) vẫn là **nấc 1** — [[bon-nac-thang-giau-co]].

**Con số đáng nhớ:** bỏ đất ra, máy 580 tr trừ nợ 660 tr = **âm 80 triệu**.

**Bốn mục bảng đang thiếu:** trả hết 660 tr nợ · người thay ở xưởng · biên lợi nhuận (không
chỉ doanh thu) · cho đi định kỳ (mới 1/40 mục).

**Định hướng chốt:** 12 tháng tới chỉ làm 3 mục — (1) lắp hai đồng hồ chi phí + công nợ và
ra giá vốn 1 mét bo, (2) HM T10/2026 → FM T3/2027, (3) trả xong nợ xã hội 200 tr. Hoãn
YouTube 100.000 USD (0 video sau 2 lần thử). Chèn bậc thang giữa cho các mục lớn — hiện chỉ
6/40 mục (15%) có mốc thời gian.
