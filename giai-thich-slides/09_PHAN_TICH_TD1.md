# Phân tích chi tiết đề TD1 Clustering (td-clustering.pdf)

> Ghi chú này để hiểu đề và lên kế hoạch, **không phải** rapport nộp. Mọi con số dưới đây đã được kiểm tra bằng một script chạy thử (numpy thuần), không phải tính nhẩm.

---

## 0. Yêu cầu nộp bài (đọc kỹ để không mất điểm hình thức)

| Yêu cầu | Chi tiết trong đề |
|---|---|
| Hình thức | 1 file nén (zip), tên `NOM-Prénom` (một mình) hoặc `NOM1-Prénom1_NOM2-Prénom2` (nhóm 2 người) |
| Code | Mã nguồn **chạy được trên Unix** |
| Rapport | **PDF** viết bằng **Markdown hoặc LaTeX** (cấm Word). Phải giải thích **cách dùng code để kiểm tra kết quả** + trả lời các câu hỏi |
| Thay thế | Có thể nộp **một file `.ipynb`** chứa cả code lẫn rapport |

→ Rapport phải có: (1) hướng dẫn chạy code, (2) kết quả và hình, (3) thảo luận ngắn cho từng câu.

## 0bis. Hiện trạng thư mục và môi trường (đã kiểm tra)

- Đã có: `data/Country-data.csv` (167 nước + 1 dòng header, 10 cột), `section2_hierarchique.py`, 2 hình `figures/s2_*.png`.
- `section2_hierarchique.py` **đúng**: mình đã tính tay lại cả 4 dendrogram và chúng khớp với hình trong đề (xem mục 2).
- Python 3.14.4, **numpy có** (cài bằng pip trong `~/.local`).
- **Thiếu: `scipy`, `matplotlib`, `scikit-learn`** → chưa chạy được Section 2, hình của Section 1 hay Ex4.
- **Thiếu: `pandoc`, LaTeX, `jupyter`** → chưa xuất được rapport PDF. Cần cài một trong số này hoặc chọn hình thức khác.

---

## 1. Section 1 — K-means

### Ex1. Tự cài đặt K-means

**Đề yêu cầu:**
- Điểm có số chiều tùy ý (1D, 2D, …), khoảng cách **Euclid**.
- Tham số: `data`, `k`, `init_centroids` (tùy chọn; `None` → chọn ngẫu nhiên).
- **Trả về SSE**, và **in ra mọi kết quả trung gian theo đúng định dạng mẫu**.

**Phân tích định dạng in ra (đây là chỗ dễ sai nhất):**

```
Iteration 1
Centroid [1]  Points [[1]]                 ← vòng 1 in tâm KHỞI TẠO, giữ nguyên kiểu (int → "[1]")
Centroid [2]  Points [[2]]
Centroid [18]  Points [[18], [20], [31]]
Iteration 2
Centroid [1.0]  Points [[1]]               ← từ vòng 2, tâm = trung bình → float ("[1.0]")
Centroid [2.0]  Points [[2]]
Centroid [23.0]  Points [[18], [20], [31]]
Fin clustering, erreur =  98.0             ← có 2 dấu cách sau "=" : print("...= ", sse)
```

**Suy ra điều kiện dừng chính xác từ mẫu:**
Ở mẫu 1, vòng 2 có tâm (1, 2, 23) **khác** tâm vòng 1 (1, 2, 18), nhưng thuật toán vẫn dừng ở vòng 2. Vậy điều kiện dừng **không phải** "tâm không đổi so với vòng trước", mà là:

> **Dừng khi phân hoạch (cách gán điểm vào cụm) không đổi so với vòng trước.**

Điều này tương đương với: "tâm mới tính lại = tâm hiện tại". Đây cũng là điều kiện trên slide 42 ("until centroids don't change").

Vòng lặp đúng:
```
centroids ← init (hoặc chọn ngẫu nhiên k điểm)
prev ← rỗng
lặp:
    gán mỗi điểm vào tâm gần nhất (Euclid)
    in "Iteration i" + từng (tâm, danh sách điểm)
    nếu phân hoạch == prev: dừng
    prev ← phân hoạch ; centroids ← trung bình từng cụm
SSE = Σ_cụm Σ_điểm ‖x − tâm‖²   (tính với tâm của vòng cuối)
in "Fin clustering, erreur = " SSE ; trả về SSE
```

**Kiểm tra:** với cách này, hai mẫu của đề cho đúng **98.0** và **2.5**, đúng số vòng (2 và 3) và đúng từng dòng in ra.
- Mẫu 1: SSE = 0 + 0 + (5² + 3² + 8²) = 98 → **cực tiểu cục bộ** (hai tâm "lãng phí" vào 1 và 2).
- Mẫu 2: SSE = (0.25 + 0.25) + (1 + 1) + 0 = 2.5 → tốt hơn nhiều. Cùng dữ liệu, cùng k, chỉ khác khởi tạo → minh họa đúng slide 44–49.

**Các quyết định thiết kế cần giải thích trong rapport:**
1. **Khởi tạo ngẫu nhiên:** chọn k điểm **khác nhau** trong dữ liệu (`random.sample`, phương pháp Forgy). Thêm tham số `seed` để chạy lại cho ra đúng kết quả cũ (reproductible).
2. **Hoà (tie):** khi một điểm cách đều hai tâm thì gán vào tâm có chỉ số nhỏ nhất. Đây là trường hợp có thật ở Ex2(a), xem bên dưới.
3. **Cụm rỗng:** có thể xảy ra (slide 56). Cách đơn giản là giữ nguyên tâm cũ, và ghi rõ trong rapport.
4. Không dùng numpy trong hàm của mình (list Python thuần, `math.dist`) để code bám sát thuật toán; numpy chỉ dùng ở Ex4 và Section 3.

### Ex2. Dữ liệu `[[2],[4],[6],[12],[24],[30]]`, k = 2

**(a) Tâm khởi tạo [2], [6]**: 4 vòng

| Vòng | Tâm | Cụm |
|---|---|---|
| 1 | 2, 6 | {2, 4} • {6, 12, 24, 30} ← điểm 4 **cách đều** 2 và 6 (hoà, gán vào tâm đầu) |
| 2 | 3.0, 18.0 | {2, 4, 6} • {12, 24, 30} |
| 3 | 4.0, 22.0 | {2, 4, 6, 12} • {24, 30} |
| 4 | 6.0, 27.0 | {2, 4, 6, 12} • {24, 30} → không đổi, dừng |

SSE = (16 + 4 + 0 + 36) + (9 + 9) = **74.0**

**(b) Tâm khởi tạo [12], [24]**: 2 vòng

| Vòng | Tâm | Cụm |
|---|---|---|
| 1 | 12, 24 | {2, 4, 6, 12} • {24, 30} |
| 2 | 6.0, 27.0 | giống vòng 1 → dừng |

SSE = **74.0**

**Thảo luận (phần đề yêu cầu "clustering nào tốt hơn"):**
- **Hai cách khởi tạo cho cùng một clustering, cùng SSE = 74.** Không cái nào tốt hơn về chất lượng. Khác biệt duy nhất là **tốc độ hội tụ**: (b) cần 2 vòng, (a) cần 4.
- Lý do: tâm (b) đã nằm sẵn ở hai phía "chỗ hở" lớn giữa 12 và 24. Tâm (a) cùng nằm bên trái, nên phải "trượt" dần sang phải qua từng vòng.
- Kiểm tra thêm: 74 là **tối ưu toàn cục** với k = 2. Các phân hoạch hợp lý khác đều tệ hơn, ví dụ {2, 4, 6} | {12, 24, 30} cho SSE = 8 + 168 = 176, và {2, …, 24} | {30} cho SSE = 315.2.
- Trường hợp hoà ở vòng 1 của (a): nếu gán 4 vào tâm 6 thì vẫn hội tụ về cùng kết quả. Có thể nhắc điều này để chứng tỏ đã kiểm tra.
- So với Ex1 (98 vs 2.5): ở đây khởi tạo "xấu" vẫn tự sửa được vì dữ liệu chỉ có 2 nhóm rõ rệt. Liên hệ slide 51–52: khởi tạo xấu đôi khi tự sửa được, đôi khi bị kẹt.

### Ex3. Trực quan hoá 2D qua từng vòng

**Tham số tùy chọn nên thêm** (đề yêu cầu giải thích từng tham số trong rapport):
- `names`: tên các điểm, dùng để ghi nhãn trên hình.
- `plot` (bool): có vẽ hình hay không.
- `fig_prefix` hoặc thư mục lưu: lưu mỗi vòng thành 1 file PNG (`ex3a_iter1.png`, …) để chèn vào rapport và tái tạo được.
- (cho Section 3) `verbose` để tắt phần in ra với 167 điểm, `plot_final_only` để chỉ vẽ hình cuối, `seed`.

**Quy ước hình theo đề:** điểm vẽ bằng `•` có ghi tên; tâm vẽ bằng `×`; cùng cụm thì cùng màu. Hình mẫu có thêm trục x = 0 và y = 0, khung [−3, 3] × [−3, 3]. Cụm 1 màu đỏ, cụm 2 màu xanh.

**Khởi tạo M1, M2**: 3 vòng (khớp 3 hình của đề)

| Vòng | Tâm | Đỏ | Xanh |
|---|---|---|---|
| 1 | (−2, 3), (−2, 1) | M1 | M2, M3, M4, M5, M6 |
| 2 | (−2, 3), (0.2, 0) | M1, M2 | M3, M4, M5, M6 |
| 3 | (−2, 2), (0.75, −0.25) | M1, M2 | M3, M4, M5, M6 → dừng |

SSE = **15.5**

**Khởi tạo M4, M6**: 3 vòng (khớp 3 hình của đề)

| Vòng | Tâm | Đỏ | Xanh |
|---|---|---|---|
| 1 | (2, −1), (1, 0) | M4 | M1, M2, M3, M5, M6 |
| 2 | (2, −1), (−0.6, 0.8) | M4, M5, M6 | M1, M2, M3 |
| 3 | (1.667, 0), (−2, 1) | M4, M5, M6 | M1, M2, M3 → dừng |

SSE = **10.67**

**Thảo luận:** khởi tạo M4, M6 cho clustering **tốt hơn** (10.67 < 15.5). Kết quả "trái / phải" này cũng tự nhiên với mắt nhìn. Khởi tạo M1, M2 đặt cả hai tâm ở cột trái, nên thuật toán bị kẹt ở **cực tiểu cục bộ**: M3 bị tách khỏi M1, M2. Đây là minh họa trực tiếp cho slide 44–49.

### Ex4. So sánh với scikit-learn

**Vì sao `[0 1 2 2 2]` và `[0 0 1 1 2]` là cùng clustering với Ex1:**
- `labels_[i]` = số thứ tự cụm của điểm thứ i. Số đó chỉ là **tên gọi**, không mang ý nghĩa.
- `[0 1 2 2 2]` → {1} | {2} | {18, 20, 31}, đúng như kết quả 1 của Ex1.
- `[0 0 1 1 2]` → {1, 2} | {18, 20} | {31}, đúng như kết quả 2.
- Hai clustering được coi là giống nhau nếu **phân hoạch giống nhau**, kể cả khi số nhãn bị hoán vị. Khi truyền `init`, sklearn đánh số cụm theo thứ tự tâm khởi tạo, nên ở đây số nhãn còn trùng luôn với thứ tự in của ta.

**Phải làm thêm:** chạy lại Ex2 (a, b) và Ex3 (2 khởi tạo) bằng sklearn, rồi so sánh với code của mình. Kết quả mong đợi (đã tính):

| Trường hợp | `labels_` mong đợi | `inertia_` (= SSE) |
|---|---|---|
| Ex2 (a) | [0 0 0 0 1 1] | 74 |
| Ex2 (b) | [0 0 0 0 1 1] | 74 |
| Ex3 M1, M2 | [0 0 1 1 1 1] | 15.5 |
| Ex3 M4, M6 | [1 1 1 0 0 0] | 10.67 |

Mẹo tăng giá trị cho rapport: so sánh thêm `inertia_` của sklearn với SSE của mình. Hai số này là cùng một đại lượng nên phải bằng nhau. Nên viết một hàm nhỏ kiểm tra "cùng phân hoạch" tự động, không cần nhìn bằng mắt.

**Lưu ý kỹ thuật:**
- Truyền `init` dưới dạng mảng **float**.
- Luôn để `n_init=1`, vì đã cho sẵn tâm khởi tạo.

---

## 2. Section 2 — Clustering phân cấp (SciPy)

**Ý chính:** `scipy.cluster.hierarchy.linkage` nhận 2 kiểu đầu vào:
1. Vector 1D = **ma trận khoảng cách dạng nén (condensed)**: các giá trị phía trên đường chéo, đọc theo từng hàng → dùng ở Section 2.
2. Ma trận 2D các điểm (n × d) → SciPy tự tính khoảng cách Euclid → dùng ở Section 3.

**Kiểm tra tay, ma trận khoảng cách (khớp hình đề):**
- Single: p1p2 @0.10 → p4p5 @0.20 → p3 nhập {p1, p2} @0.30 → tất cả @0.35 (= d(p1, p4)).
- Complete: p1p2 @0.10 → p4p5 @0.20 → p3 nhập {p4, p5} @0.70 → tất cả @0.90.
- Nhận xét để viết: **cùng dữ liệu nhưng hai cây khác nhau**. Single link cho p3 vào cùng nhóm với p1, p2; complete link cho p3 vào cùng nhóm với p4, p5. Đúng như slide 81–88.

**Ma trận độ tương đồng (similarity) → khoảng cách = 1 − sim:**

| | p2 | p3 | p4 | p5 |
|---|---|---|---|---|
| p1 | 0.90 | 0.59 | 0.45 | 0.65 |
| p2 | | 0.36 | 0.53 | 0.02 |
| p3 | | | 0.56 | 0.15 |
| p4 | | | | 0.24 |

- Single: p2p5 @0.02 → p3 @0.15 → p4 @0.24 → p1 @0.45 (dạng chuỗi, đặc trưng của single link).
- Complete: p2p5 @0.02 → p3 @0.36 → p1p4 @0.45 → tất cả @0.90.
- Cả hai khớp hình đề và lời giải của sách (sol.pdf, tr. 134).
- **Vì sao phải đổi:** `linkage` luôn gộp cặp có giá trị **nhỏ nhất**. Nếu đưa similarity vào trực tiếp, nó sẽ gộp p1–p2 (sim 0.10, tức là **kém** giống nhau nhất) trước tiên. Kết quả sai hoàn toàn.

**Code hiện có:** đúng. Có `assert` so với `squareform` để kiểm tra hàm tự viết `matrix_to_condensed`. Cần sửa nhỏ để **tái sử dụng** ở Section 3 (đề ghi rõ "réutilisez votre code de la Section 2"):
- Hàm vẽ phải nhận cả dữ liệu dạng điểm.
- Hàm vẽ phải vẽ **một** dendrogram lớn cho mỗi phương pháp, với `orientation="right"` (tên nước ở bên trái, giống Figure 3–4) và `figsize` đủ lớn cho 167 nhãn.

---

## 3. Section 3 — Case study Country-data

### Ex1. Chuẩn bị dữ liệu

**Đọc CSV:**
- Bỏ dòng header, giữ cột 0 làm `countries` và 9 cột còn lại (đổi sang float) làm `data_country`.
- Kiểm tra (đã chạy): đúng 167 dòng × 9 cột, dòng đầu `[90.2, 10.0, 7.58, 44.9, 1610.0, 9.44, 56.2, 5.82, 553.0]` ✔.
- Nên dùng module `csv`, vì có tên nước chứa dấu phẩy trong ngoặc kép, ví dụ "Congo, Dem. Rep.". Nếu `split(',')` thì sẽ vỡ dòng.

**Vì sao phải chuẩn hoá rồi mới PCA (đề có nêu, cần giải thích lại bằng lời của mình):**
- Thang đo các biến rất khác nhau: `income` và `gdpp` cỡ hàng nghìn đến hàng chục nghìn, `total_fer` cỡ 1–7. Khoảng cách Euclid sẽ gần như chỉ phản ánh `gdpp` và `income`.
- **Dữ liệu chuẩn hoá (centrées réduites):** $z = (x - \bar{x}) / \sigma$, sau đó mỗi biến có trung bình 0 và độ lệch chuẩn 1. Mọi biến được đối xử ngang nhau.
- **PCA:** 9 chiều thì không vẽ được. PCA chiếu dữ liệu lên 2 hướng giữ được nhiều phương sai (thông tin) nhất. Đó là 2 vector riêng của ma trận tương quan $R = Z^T Z / n$ ứng với 2 giá trị riêng lớn nhất.

**⚠️ 3 bẫy kỹ thuật trong khung code của thầy (đã phát hiện khi chạy thử):**

1. **`numpy.linalg.eig` không sắp xếp giá trị riêng.** Trên máy này thứ tự trả về là 4.136, 1.546, 1.170, 0.995, 0.661, 0.224, **0.067, 0.088, 0.113**, tức là không có thứ tự. Lần này 2 cột đầu tình cờ đúng là 2 giá trị lớn nhất, nhưng không có gì đảm bảo. Cách sửa: sắp xếp theo giá trị riêng giảm dần trước khi lấy 2 vector riêng (hoặc dùng `eigh`, hàm dành cho ma trận đối xứng).
2. **`eig` trả về kiểu số phức** (`complex128`, phần ảo = 0). Nếu để nguyên thì matplotlib, SciPy và k-means sẽ gặp lỗi hoặc cảnh báo. Cách sửa: lấy `.real`, hoặc dùng `eigh` (luôn trả về số thực).
3. **Dấu của vector riêng là tùy ý** ($v$ và $-v$ đều là vector riêng). Trên máy này kết quả là `[[-2.91, 0.10], [0.43, -0.59], …]`, tức là **ngược dấu cả hai trục** so với đề (`[[2.91, -0.1], [-0.43, 0.59], …]`).
   - Hệ quả: hình bị lật như qua gương, nhưng khoảng cách giữa các điểm **không đổi**, nên clustering không đổi.
   - Để hình giống thầy: đổi dấu sao cho Afghanistan có PC1 > 0. Rapport nên ghi rõ việc đổi dấu này kèm lý do.

**Thông tin giữ lại sau PCA (nên đưa vào rapport, đề không hỏi nhưng thể hiện tư duy):**
- PC1 giữ **46.0%** phương sai, PC2 giữ **17.2%** → hình 2D chỉ giữ **≈ 63%** thông tin.
- Khoảng 37% thông tin bị mất, nên hai nước trông gần nhau trên hình 2D có thể vẫn khác nhau trong 9D.
- Clustering ở đây được làm **trên dữ liệu 2D**, không phải trên 9 chiều gốc.

**Ý nghĩa 2 trục** (hệ số, theo chiều dấu của thầy):
- **PC1 (trục X):** dương ↔ `child_mort` (+0.42), `total_fer` (+0.40) cao; âm ↔ `life_expec` (−0.43), `income` (−0.40), `gdpp` (−0.39) cao.
  → X càng lớn thì nước càng **kém phát triển**. Châu Phi cận Sahara nằm bên phải, Na Uy và Thụy Sĩ nằm bên trái.
- **PC2 (trục Y):** chủ yếu do `imports` (−0.67) và `exports` (−0.61).
  → Y càng âm thì nền kinh tế càng **mở cửa thương mại**. Singapore, Luxembourg, Malta nằm sát đáy hình là các nền kinh tế nhỏ có xuất nhập khẩu > 100% GDP.

### Ex2. Clustering + thảo luận

**Cần tạo ít nhất 2 hình cho mỗi loại:**
- K-means k = 2 và k = 3, dùng lại code Section 1, chỉ vẽ hình cuối, có tên nước.
- Phân cấp single link và complete link, dùng lại code Section 2, với `labels = countries`.

**Các ý thảo luận đề yêu cầu (và hướng trả lời dự kiến, sẽ xác nhận khi có hình thật):**

1. **Cân bằng giữa các cụm:**
   - K-means cho các cụm có kích thước tương đối cân bằng. Lý do: SSE "thích" các cụm tròn, cỡ đều (slide 61–64).
   - Single link rất **mất cân bằng**: một cụm khổng lồ, và các outlier (Singapore, Luxembourg, Malta, Seychelles, Ireland…) chỉ nhập vào ở cuối. Đó là hiệu ứng chuỗi (chaining) của MIN.
   - Complete link cân bằng hơn: nhóm châu Phi nghèo (xanh lá), nhóm outlier (cam), và phần còn lại tách thành giàu / trung bình.
2. **Gần nhau trong cụm so với gần nhau trên bản đồ:**
   - Các cụm phản ánh **mức độ phát triển** (sức khoẻ, thu nhập, sinh sản), không phải địa lý.
   - Tuy vậy, địa lý vẫn "lộ ra" gián tiếp vì phát triển có tương quan với vùng: châu Phi cận Sahara, Tây Âu / Bắc Âu.
3. **Gần nhau bất ngờ hoặc đúng dự đoán:**
   - Đúng dự đoán: các nước Bắc Âu ở cạnh nhau; Mỹ ở gần Nhật Bản.
   - Bất ngờ: Qatar và Kuwait cùng nhóm với các nước châu Âu giàu (vì giàu nhờ dầu mỏ). Ở single link, Việt Nam xuất hiện gần Hà Lan / Bỉ (vì độ mở thương mại cao trên PC2). Haiti và Nigeria thành outlier riêng.
   - Phải kiểm chứng lại trên hình thật trước khi viết.
4. **K-means khởi tạo ngẫu nhiên có cho kết quả khác hẳn hình của thầy không?**
   - Có thể. Nên chạy nhiều `seed`, ghi lại SSE và kích thước cụm để chứng minh bằng số.
   - Với k = 2, ranh giới "giàu / nghèo" khá ổn định.
   - Với k = 3, nếu một tâm khởi tạo rơi vào Singapore, Luxembourg hoặc Malta, k-means có thể dành nguyên một cụm cho 3 outlier này (SSE khác, cụm rất lệch). Liên hệ slide 61 (outliers) và slide 50 (xác suất chọn được tâm tốt).

---

## 4. Kế hoạch làm (đúng thứ tự đề) và cấu trúc file đề xuất

```
ASL_IA_TD1_Clustering/
├── data/Country-data.csv
├── section1_kmeans.py        # Ex1 (hàm kmeans) + Ex2 + Ex3 (hình qua từng vòng)
├── section1_sklearn.py       # Ex4 (so sánh scikit-learn, kiểm tra tự động)
├── section2_hierarchique.py  # đã có; sửa nhẹ để tái sử dụng
├── section3_etude_de_cas.py  # đọc CSV + PCA + k-means k=2,3 + single/complete
├── figures/                  # mọi hình được sinh tự động
└── rapport.md → rapport.pdf  # viết bằng tiếng Pháp, giọng sinh viên
```

Thứ tự thực hiện:
1. Section 1 Ex1 → Ex2 → Ex3 → Ex4.
2. Section 2 (rà lại code có sẵn).
3. Section 3 Ex1 → Ex2.
4. Rapport.

Mỗi bước gồm: code → chạy → đối chiếu với đề → ghi kết quả và giải thích ngắn "vì sao làm vậy".

## 5. Cần chốt trước khi bắt đầu

1. **Cài thư viện thiếu** (`scipy`, `matplotlib`, `scikit-learn`). Có hai cách:
   - `pip install --user scipy matplotlib scikit-learn` (giống cách numpy đang được cài)
   - `sudo apt install python3-scipy python3-matplotlib python3-sklearn` (như thầy gợi ý)
2. **Hình thức nộp:** scripts + `rapport.md` xuất PDF (cần cài `pandoc` + LaTeX), hay một file Jupyter `.ipynb` (cần cài `jupyter`)?
3. **Ngôn ngữ rapport:** tiếng Pháp (mặc định, vì là môn ở INSA)?
4. Làm một mình hay nhóm 2 người (để đặt tên file zip)?
