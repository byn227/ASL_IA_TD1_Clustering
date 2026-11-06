# Chương 8 — Cluster Analysis (phần C): Hạn chế của K-means & Phân cụm phân cấp (slides 61–78)

> Phạm vi: slides 61 → 78 của `slides-dm.pdf`.
> - Slides 61–67: **hạn chế của K-means** (kích thước, mật độ, hình dạng khác nhau, outliers) và cách "vá" bằng cách dùng nhiều cụm.
> - Slides 68–70: **phân cụm phân cấp (hierarchical clustering)**, dendrogram, ưu điểm, hai loại agglomerative / divisive.
> - Slides 71–75: **thuật toán gộp (agglomerative)** và vấn đề cập nhật ma trận khoảng cách (proximity matrix).
> - Slides 76–78: các cách định nghĩa **khoảng cách giữa hai cụm**: MIN, MAX (và giới thiệu Group Average, Centroid, Ward — chi tiết nằm ở slides 79–95, phần của người khác).
>
> Quy ước: nội dung không có trên slide được ghi **(bổ sung)**.

---

## 0. Bức tranh tổng thể (đọc trước)

- K-means (các slide trước) là **phân cụm phân hoạch (partitional clustering)**: chia dữ liệu thành đúng $K$ nhóm rời nhau, mỗi nhóm đại diện bởi 1 tâm (centroid), tối thiểu hoá SSE.
- Slides 61–67 cho thấy K-means "thất bại" trong nhiều trường hợp thực tế → động lực để học các phương pháp khác.
- Phương pháp tiếp theo là **phân cụm phân cấp (hierarchical clustering)**: thay vì 1 phân hoạch, ta có **cả một cây** các cụm lồng nhau (nested clusters). Cắt cây ở độ cao nào thì được số cụm tương ứng.

Hình dung: K-means giống như "chia lớp học thành K tổ ngay lập tức"; hierarchical giống như "xây cây gia phả": từng cặp anh em ruột gộp lại thành gia đình, gia đình gộp thành họ, họ gộp thành dòng tộc...

---

## 1. Hạn chế của K-means (slides 61–64)

### Slide 61 — Limitations of K-means

Slide liệt kê: K-means gặp vấn đề khi các cụm có
- **kích thước khác nhau (differing sizes)**,
- **mật độ khác nhau (differing densities)**,
- **hình dạng không cầu / không lồi (non-globular shapes)**,

và khi dữ liệu chứa **ngoại lai (outliers)**.

**Tại sao? (bổ sung — giải thích gốc rễ)**
1. **Hàm mục tiêu SSE**: K-means tìm phân hoạch tối thiểu
   $$SSE=\sum_{i=1}^{K}\sum_{x\in C_i}\lVert x-c_i\rVert^2$$
   ($c_i$ = tâm cụm $i$, $\lVert\cdot\rVert$ = khoảng cách Euclid). SSE "thích" các cụm **tròn, cùng cỡ, cùng độ phân tán**. Nếu "cụm thật" không như vậy, phân hoạch có SSE nhỏ nhất **không phải** là phân hoạch tự nhiên.
2. **Ranh giới tuyến tính (Voronoi)**: mỗi điểm được gán cho tâm gần nhất ⇒ ranh giới giữa 2 cụm là **đường trung trực** của đoạn nối 2 tâm ⇒ mỗi cụm là một **đa giác lồi**. Hình trăng khuyết, xoắn ốc... không thể được biểu diễn bởi đa giác lồi.
3. **Trung bình (mean) không bền vững (not robust)**: một điểm ngoại lai rất xa kéo tâm lệch hẳn.

### Slide 62 — Differing Sizes

- **Original Points**: 3 cụm thật: một cụm nhỏ (xanh dương) bên trái quanh $x\approx-3.5$, một cụm **rất lớn** (đỏ) ở giữa, một cụm nhỏ (xanh lá) bên phải quanh $x\approx 3.5$.
- **K-means (3 Clusters)**: kết quả "cắt" cụm lớn: phần trái của cụm đỏ bị gộp với cụm nhỏ bên trái, phần phải bị gộp với cụm nhỏ bên phải, phần giữa-dưới thành 1 cụm. Các dấu "+" là centroid — chúng không nằm ở tâm các cụm thật.

**Ví dụ số (bổ sung, 1 chiều, đã kiểm tra bằng máy)**: cụm lớn = 11 điểm $\{0,1,\dots,10\}$, cụm nhỏ = $\{14,15\}$, $K=2$.
- Phân hoạch "đúng": $\{0..10\}$ (tâm 5, $SSE=2(1+4+9+16+25)=110$) và $\{14,15\}$ (tâm 14.5, $SSE=0.5$) → **tổng 110.5**.
- Phân hoạch "sai": $\{0..7\}$ (tâm 3.5, $SSE=42$) và $\{8,9,10,14,15\}$ (tâm 11.2, $SSE=38.8$) → **tổng 80.8 < 110.5**.

⇒ Ngay cả khi K-means tìm được **tối ưu toàn cục**, nó vẫn cắt đôi cụm lớn! Lỗi nằm ở **hàm mục tiêu**, không chỉ ở việc khởi tạo. (Cả hai phân hoạch đều là điểm dừng ổn định của K-means: với tâm 3.5 và 11.2, trung điểm 7.35 tách đúng 7|8.)

### Slide 63 — Differing Density

- **Original Points**: bên trái một cụm **thưa** (đỏ, rộng), bên phải hai cụm **dày đặc** nhỏ (xanh dương trên, xanh lá dưới).
- **K-means (3 Clusters)**: cụm thưa bị **chia làm 2** (xanh lá + xanh dương), còn **hai cụm dày bị gộp thành 1** (đỏ, một centroid nằm giữa hai cụm, $x\approx 6$).
- Lý do: cụm thưa đóng góp SSE rất lớn (các điểm cách tâm xa) → chia nó ra giảm SSE nhiều; hai cụm dày gần nhau, gộp lại chỉ tăng SSE một chút.

### Slide 64 — Non-globular Shapes

- **Original Points**: hai cụm hình **lưỡi liềm / chữ S lồng nhau** (đỏ và xanh dương), đan xen.
- **K-means (2 Clusters)**: K-means vẽ một **đường thẳng** cắt ngang (do ranh giới Voronoi tuyến tính) → mỗi cụm kết quả chứa một nửa của cả hai hình. Kết quả sai hoàn toàn.

### Outliers (slide 61, ý cuối)

**Ví dụ số (bổ sung)**: $\{1,2,3,\ 10,11,12,\ 100\}$, $K=2$.
- Cách "tự nhiên" $\{1,2,3\},\{10,11,12,100\}$: SSE $=2 + 5942.75 = 5944.75$ (tâm cụm 2 bị kéo tới 33.25!).
- Cách K-means chọn: $\{1,\dots,12\}$ (tâm 6.5, SSE 125.5) và $\{100\}$ (SSE 0) → tổng 125.5.

⇒ Ngoại lai "chiếm mất" một cụm, hai cụm thật bị gộp. Cách xử lý: tiền xử lý loại outliers (slide 58), dùng **K-medoids** (dùng điểm trung vị thay cho trung bình) **(bổ sung)**, hoặc dùng nhiều cụm hơn rồi bỏ cụm quá nhỏ.

---

## 2. Khắc phục hạn chế của K-means (slides 65–67)

### Slide 65 — Differing sizes, dùng nhiều cụm
- Cùng dữ liệu như slide 62, nhưng chạy K-means với **nhiều cụm** (khoảng 10 centroid "+" trên hình).
- Ghi chú trên slide: *"One solution is to use many clusters. Find parts of clusters, but need to put together."* → Dùng nhiều cụm: mỗi cụm K-means chỉ là **một mảnh** của một cụm thật, nhưng **thuần khiết** (không chứa điểm của 2 cụm thật khác nhau). Sau đó **phải ghép các mảnh lại**.

### Slide 66 — Differing density, dùng nhiều cụm
- Cụm thưa bên trái bị chia thành ~7–8 mảnh nhỏ; hai cụm dày bên phải mỗi cụm là **1 cụm riêng** (không còn bị gộp nhau).

### Slide 67 — Non-globular shapes, dùng nhiều cụm
- Mỗi lưỡi liềm bị chia thành nhiều mảnh nhỏ (~10 màu). Mỗi mảnh nhỏ gần như "tròn" cục bộ nên K-means xử lý tốt; mảnh nào cũng chỉ thuộc **một** hình.

**Phân tích sâu**
- Ý tưởng chính: **over-clustering (phân cụm thừa) + gộp lại (merge)**. Bước "put together" chính là một bài toán **phân cụm phân cấp gộp (agglomerative)** trên các mảnh nhỏ → chuyển tiếp tự nhiên sang slide 68.
- **(bổ sung)** Đây là ý tưởng của các phương pháp 2 pha: K-means với K lớn để tóm tắt dữ liệu (rẻ, $O(NKI)$), rồi agglomerative (ví dụ single link) trên K centroid (rẻ vì K ≪ N). Thuật toán CHAMELEON, BIRCH dùng ý tưởng tương tự.
- Nhược điểm: phải chọn K "đủ lớn", và cần một tiêu chí tốt để ghép (nếu ghép bằng khoảng cách centroid thì lại gặp vấn đề cũ).

---

## 3. Phân cụm phân cấp — Hierarchical Clustering (slide 68)

**Định nghĩa (slide 68)**:
- Tạo ra **một tập các cụm lồng nhau (nested clusters)** được tổ chức thành **cây phân cấp (hierarchical tree)**.
- Có thể biểu diễn bằng **dendrogram**: sơ đồ dạng cây ghi lại **thứ tự các lần gộp (merges) hoặc tách (splits)**.

**Giải thích hình (slide 68)** — 6 điểm, đánh số 1…6:
- Hình bên phải (**nested clusters / sơ đồ Venn**): các vòng lồng nhau, số đỏ là **thứ tự gộp**:
  1. gộp {1, 3}
  2. gộp {2, 5}
  3. gộp {4} với {2, 5} → {2, 4, 5}
  4. gộp {1, 3} với {2, 4, 5} → {1, 2, 3, 4, 5}
  5. gộp với {6} → tất cả
- Hình bên trái (**dendrogram**): trục ngang là các điểm, sắp theo thứ tự 1, 3, 2, 5, 4, 6 (sắp xếp để các nhánh không cắt nhau); trục đứng là **khoảng cách tại lúc gộp** (merge height). Đọc xấp xỉ từ hình: {1,3} ≈ 0.05; {2,5} ≈ 0.075; {2,5}+4 ≈ 0.17; {1,3}+{2,4,5} ≈ 0.175; +6 ≈ 0.21 (giá trị chính xác không ghi trên slide).

**Cách đọc dendrogram**
- Mỗi lá (leaf) = 1 điểm. Mỗi "chữ U ngược" (thanh ngang) = 1 lần gộp, nối 2 cụm con.
- **Độ cao** thanh ngang = khoảng cách giữa 2 cụm lúc gộp. Hai điểm gộp càng thấp thì càng giống nhau.
- **Thứ tự trái-phải của các lá không mang ý nghĩa** (có thể xoay các nhánh); chỉ cấu trúc cây và độ cao là quan trọng.
- Với N điểm có đúng **N−1 lần gộp** → N−1 nút trong.

**Liên hệ (bổ sung)**: dendrogram ↔ sơ đồ lồng nhau mang cùng thông tin về *cấu trúc*, nhưng dendrogram còn cho thêm *độ cao* (khoảng cách gộp). Sơ đồ lồng nhau chỉ dùng được cho dữ liệu 2D.

---

## 4. Ưu điểm của phân cụm phân cấp (slide 69)

1. **Không cần giả định trước số cụm** (khác K-means phải chọn K).
   - Muốn bao nhiêu cụm cũng được bằng cách **"cắt" (cutting) dendrogram** ở độ cao thích hợp: đường cắt ngang cắt qua bao nhiêu nhánh dọc thì có bấy nhiêu cụm.
   - Ví dụ slide 68: cắt ở độ cao 0.1 → cắt qua 4 nhánh: {1,3}, {2,5}, {4}, {6} → 4 cụm. Cắt ở 0.19 → {1,2,3,4,5}, {6} → 2 cụm.
2. **Có thể tương ứng với các phân loại có ý nghĩa (meaningful taxonomies)**: ví dụ sinh học — giới động vật (animal kingdom), tái dựng cây phát sinh loài (phylogeny reconstruction). Ví dụ: chó + sói gộp rất thấp, rồi + cáo, rồi + mèo (cùng bộ ăn thịt), rồi + người (cùng lớp thú)...

**(bổ sung)** Mẹo chọn chỗ cắt: cắt ở nơi có **"khoảng trống" lớn nhất** giữa hai độ cao gộp liên tiếp (các cụm tồn tại lâu nhất khi tăng ngưỡng).

---

## 5. Hai loại phân cụm phân cấp (slide 70)

| | **Gộp — Agglomerative** (bottom-up, "từ dưới lên") | **Tách — Divisive** (top-down, "từ trên xuống") |
|---|---|---|
| Khởi đầu | Mỗi điểm là 1 cụm riêng (N cụm) | 1 cụm chứa tất cả |
| Mỗi bước | **Gộp cặp cụm gần nhau nhất** | **Tách** một cụm thành 2 |
| Kết thúc | Còn 1 cụm (hoặc còn k cụm) | Mỗi cụm còn 1 điểm (hoặc có k cụm) |
| Phổ biến | Phổ biến hơn (slide 71) | Ít hơn; ví dụ: **Bisecting K-means** (slide 59), tách theo MST (bổ sung) |

- Các thuật toán phân cấp truyền thống dùng **ma trận tương đồng hoặc ma trận khoảng cách (similarity or distance matrix)**, và **gộp hoặc tách từng cụm một (one cluster at a time)**.

**(bổ sung)** Tại sao divisive ít dùng: có $2^{n-1}-1$ cách tách một cụm $n$ điểm thành 2 → không thể thử hết, cần heuristic (ví dụ bisecting K-means, hoặc xây cây khung nhỏ nhất MST rồi cắt cạnh dài nhất — cách này cho kết quả giống single link).

---

## 6. Thuật toán phân cụm gộp cơ bản (slide 71)

Slide 71: đây là kỹ thuật phân cấp **phổ biến hơn**; thuật toán đơn giản:

```
1. Tính ma trận khoảng cách (proximity matrix) N×N
2. Mỗi điểm dữ liệu là một cụm
3. Repeat
4.     Gộp hai cụm gần nhau nhất
5.     Cập nhật ma trận khoảng cách
6. Until chỉ còn một cụm
```

**Thao tác then chốt**: tính **khoảng cách (proximity) giữa hai cụm**. Các cách định nghĩa khác nhau ⇒ **các thuật toán khác nhau** (MIN, MAX, Group Average, ...).

**Pseudocode chi tiết hơn (bổ sung)**:
```
Input : ma trận khoảng cách D (N×N), hàm liên kết linkage ∈ {MIN, MAX, AVG, ...}
Output: danh sách N−1 lần gộp (cụm1, cụm2, độ cao) = dendrogram

clusters ← {{x1}, {x2}, ..., {xN}}
while |clusters| > 1:
    (Ci, Cj) ← argmin_{Ci≠Cj} d(Ci, Cj)          # tìm cặp gần nhất
    ghi lại (Ci, Cj, d(Ci, Cj))                     # một nút của dendrogram
    Cnew ← Ci ∪ Cj
    xoá hàng/cột Ci, Cj khỏi D; thêm hàng/cột Cnew
    for mỗi cụm Ck còn lại:
        d(Ck, Cnew) ← linkage(...)                  # ví dụ MIN: min(d(Ck,Ci), d(Ck,Cj))
    clusters ← clusters − {Ci, Cj} + {Cnew}
```
Nếu chỉ muốn $k$ cụm: dừng khi `|clusters| = k`.

**Độ phức tạp** (slide 94, thuộc phần sau; nhắc lại để thấy bức tranh): bộ nhớ $O(N^2)$ (ma trận khoảng cách); thời gian $O(N^3)$ với cài đặt ngây thơ (N−1 bước, mỗi bước quét ma trận $O(N^2)$), có thể giảm còn $O(N^2\log N)$ với hàng đợi ưu tiên (heap).
Ví dụ: N = 100 000 điểm → ma trận có $10^{10}$ ô ≈ 40 GB (float32) — không khả thi; K-means thì chỉ $O(N)$ bộ nhớ.

---

## 7. Minh hoạ các bước (slides 72–75)

### Slide 72 — Starting Situation (tình huống ban đầu)
- 12 điểm (vòng tròn trắng) p1…p12; mỗi điểm là 1 cụm.
- **Proximity matrix** kích thước 12×12: ô $(p_i,p_j)$ = khoảng cách giữa $p_i$ và $p_j$ (đối xứng, đường chéo = 0).
- Dưới cùng: 12 lá (chấm đỏ) — đáy của dendrogram tương lai.

### Slide 73 — Intermediate Situation (sau vài bước gộp)
- Còn 5 cụm C1…C5 (các "đám mây" xám). Ma trận khoảng cách giờ là 5×5 (giữa **các cụm**).
- Dưới: dendrogram từng phần — các lá p1…p12 đã được nối lên 5 nút xanh lá (mỗi nút = một cụm hiện tại; ví dụ p10, p11, p12 đã gộp thành 1 cụm).

### Slide 74 — Gộp hai cụm gần nhất
- Hai cụm gần nhất là **C2 và C5** (vòng elip chấm chấm). Trong ma trận, **hàng và cột của C2 và C5 được gạch chéo** — chúng sẽ bị xoá/thay thế.

### Slide 75 — After Merging (sau khi gộp)
- Có cụm mới **C2 ∪ C5**. Ma trận còn 4×4: C1, C2∪C5, C3, C4.
- Các ô trên hàng/cột **C2∪C5 là dấu "?"** — câu hỏi then chốt: **"Cập nhật ma trận khoảng cách thế nào?"** Các ô khác (ví dụ C1–C3) **không đổi**.
- Trả lời câu hỏi "?" chính là chọn **cách đo khoảng cách giữa các cụm** → slides 76–80.

Ví dụ nhỏ cho "?": giả sử $d(C1,C2)=7$, $d(C1,C5)=4$. Khi đó $d(C1, C2\cup C5)$ = 4 với MIN, = 7 với MAX, và với Group Average thì tuỳ số điểm mỗi cụm (nếu $|C2|=|C5|$ thì = 5.5).

---

## 8. Định nghĩa khoảng cách giữa hai cụm (slides 76–78)

Slide 76 ("How to Define Inter-Cluster Similarity") liệt kê 5 cách:
1. **MIN**
2. **MAX**
3. **Group Average**
4. **Distance Between Centroids**
5. **Các phương pháp dựa trên hàm mục tiêu (objective function)** — ví dụ **Ward's Method** dùng **sai số bình phương (squared error)**.

Ký hiệu: $C_i, C_j$ là hai cụm, $d(x,y)$ là khoảng cách giữa hai điểm, $|C|$ = số điểm trong cụm.

### 8.1 MIN — Single link (slide 77)
Hình: mũi tên vàng nối **cặp điểm gần nhau nhất** giữa hai cụm.
$$d_{MIN}(C_i,C_j)=\min_{x\in C_i,\ y\in C_j} d(x,y)$$
- Trực giác: "hai nhóm bạn được coi là thân nếu **có ít nhất một cặp** bạn thân với nhau". Chỉ cần 1 "cây cầu".
- Tên khác: **single link / single linkage**. (Theo slide 81 — phần sau: được quyết định bởi **một** cặp điểm, tức **một cạnh** trong đồ thị lân cận.)

### 8.2 MAX — Complete link (slide 78)
Hình: mũi tên vàng nối **cặp điểm xa nhau nhất** giữa hai cụm.
$$d_{MAX}(C_i,C_j)=\max_{x\in C_i,\ y\in C_j} d(x,y)$$
- Trực giác: "hai nhóm chỉ được coi là gần nếu **mọi** cặp thành viên đều gần" — đo bằng cặp tệ nhất.
- Tên khác: **complete link / complete linkage**. Kết quả: các cụm có **đường kính nhỏ**, gọn, tròn.

### 8.3 Ba cách còn lại (chỉ được liệt kê ở slide 76; chi tiết ở slides 79–92)
- **Group Average** (trung bình nhóm):
  $$d_{avg}(C_i,C_j)=\frac{\sum_{x\in C_i}\sum_{y\in C_j} d(x,y)}{|C_i|\cdot|C_j|}$$
- **Distance Between Centroids**: $d(c_i,c_j)$ với $c_i=\frac{1}{|C_i|}\sum_{x\in C_i}x$.
- **Ward**: độ tăng SSE khi gộp: $\Delta SSE = SSE(C_i\cup C_j)-SSE(C_i)-SSE(C_j)$; **(bổ sung)** công thức đóng: $\Delta SSE=\frac{|C_i||C_j|}{|C_i|+|C_j|}\lVert c_i-c_j\rVert^2$.

### 8.4 Ví dụ số: 5 cách đo trên cùng 2 cụm (đã kiểm tra bằng máy)
$C_1=\{a_1=(0,0),\ a_2=(0,2)\}$, $C_2=\{b_1=(3,0),\ b_2=(5,0)\}$, khoảng cách Euclid.

| cặp | khoảng cách |
|---|---|
| $a_1b_1$ | 3 |
| $a_1b_2$ | 5 |
| $a_2b_1$ | $\sqrt{9+4}=\sqrt{13}\approx3.606$ |
| $a_2b_2$ | $\sqrt{25+4}=\sqrt{29}\approx5.385$ |

- MIN = **3**
- MAX = **5.385**
- Group Average = $(3+5+3.606+5.385)/4 = 16.991/4 \approx$ **4.248**
- Centroid: $c_1=(0,1)$, $c_2=(4,0)$ → $\sqrt{16+1}=\sqrt{17}\approx$ **4.123**
- Ward: $SSE(C_1)=1+1=2$, $SSE(C_2)=1+1=2$; cụm gộp có tâm $(2,0.5)$, $SSE=4.25+6.25+1.25+9.25=21$ → $\Delta SSE=21-2-2=$ **17**; kiểm tra bằng công thức: $\frac{2\cdot2}{4}\cdot17=17$ ✓.

Luôn có: $\text{MIN}\le\text{Group Average}\le\text{MAX}$ (trung bình nằm giữa min và max).

### 8.5 Công thức cập nhật ma trận — Lance–Williams (bổ sung, rất tiện khi làm tay)
Khi gộp $C_i$ và $C_j$ thành $C_{ij}$, khoảng cách tới cụm $C_k$ khác:
- **MIN**: $d(C_k,C_{ij})=\min\big(d(C_k,C_i),\ d(C_k,C_j)\big)$
- **MAX**: $d(C_k,C_{ij})=\max\big(d(C_k,C_i),\ d(C_k,C_j)\big)$
- **Group Average**: $d(C_k,C_{ij})=\dfrac{|C_i|\,d(C_k,C_i)+|C_j|\,d(C_k,C_j)}{|C_i|+|C_j|}$ (**trung bình có trọng số theo số điểm**, không phải trung bình thường!)

Dạng tổng quát: $d(C_k,C_{ij})=\alpha_i d_{ki}+\alpha_j d_{kj}+\beta d_{ij}+\gamma|d_{ki}-d_{kj}|$; MIN: $\alpha_i=\alpha_j=\tfrac12,\beta=0,\gamma=-\tfrac12$; MAX: như trên nhưng $\gamma=+\tfrac12$ (vì $\frac{a+b}{2}\mp\frac{|a-b|}{2}=\min/\max(a,b)$).

⇒ Nhờ vậy **không cần quay về dữ liệu gốc**: chỉ cần ma trận hiện tại.

---

## 9. Bài tập mẫu làm tay: MIN và MAX trên ma trận 5×5 (dạng bài thi điển hình)

### Đề
Cho 5 điểm A, B, C, D, E với ma trận khoảng cách (đối xứng; đã kiểm tra thoả bất đẳng thức tam giác):

```
      A    B    C    D    E
A     0
B     2    0
C     6    5    0
D    10    9    4    0
E     9    8    7    3    0
```
Thực hiện phân cụm gộp với (a) MIN (single link), (b) MAX (complete link). Vẽ dendrogram. Cho kết quả khi cắt thành 2 cụm.

### (a) MIN — single link

**Bước 1.** Giá trị nhỏ nhất trong ma trận: $d(A,B)=2$ → gộp **{A,B} ở độ cao 2**.
Cập nhật (lấy min):
- $d(AB,C)=\min(6,5)=5$
- $d(AB,D)=\min(10,9)=9$
- $d(AB,E)=\min(9,8)=8$
```
      AB   C    D    E
AB    0
C     5    0
D     9    4    0
E     8    7    3    0
```
**Bước 2.** Nhỏ nhất: $d(D,E)=3$ → gộp **{D,E} ở độ cao 3**.
- $d(AB,DE)=\min(9,8)=8$
- $d(C,DE)=\min(4,7)=4$
```
      AB   C    DE
AB    0
C     5    0
DE    8    4    0
```
**Bước 3.** Nhỏ nhất: $d(C,DE)=4$ → gộp **{C,D,E} ở độ cao 4**.
- $d(AB,CDE)=\min(5,8)=5$
```
      AB   CDE
AB    0
CDE   5    0
```
**Bước 4.** Gộp **{A,B} với {C,D,E} ở độ cao 5**. Kết thúc.

Thứ tự gộp MIN: (A,B)@2 → (D,E)@3 → (C,DE)@4 → (AB,CDE)@5.

Dendrogram MIN:
```
   5 |    +----+-----+
   4 |    |       +--+---+
   3 |    |       |    +-+--+
   2 |  +-+--+    |    |    |
     |  |    |    |    |    |
     |  |    |    |    |    |
     +--------------------------
        A    B    C    D    E
```

**Kiểm tra nhanh (bổ sung)**: các độ cao gộp của single link = **các cạnh của cây khung nhỏ nhất (MST)**. MST ở đây: AB(2), DE(3), CD(4), BC(5) → độ cao 2, 3, 4, 5 ✓.

### (b) MAX — complete link

**Bước 1.** Như trên: gộp **{A,B} ở độ cao 2** (bước đầu luôn giống nhau với mọi linkage, vì các cụm đều là 1 điểm).
Cập nhật (lấy max):
- $d(AB,C)=\max(6,5)=6$
- $d(AB,D)=\max(10,9)=10$
- $d(AB,E)=\max(9,8)=9$
```
      AB   C    D    E
AB    0
C     6    0
D    10    4    0
E     9    7    3    0
```
**Bước 2.** Nhỏ nhất: $d(D,E)=3$ → gộp **{D,E} ở độ cao 3**.
- $d(AB,DE)=\max(10,9)=10$
- $d(C,DE)=\max(4,7)=7$
```
      AB   C    DE
AB    0
C     6    0
DE   10    7    0
```
**Bước 3.** Nhỏ nhất: $d(AB,C)=6$ → gộp **{A,B,C} ở độ cao 6**. (Chú ý: C gần D nhất (4) nhưng vì E ở xa C (7) nên với MAX, C lại về phía AB!)
- $d(ABC,DE)=\max(10,7)=10$

**Bước 4.** Gộp **{A,B,C} với {D,E} ở độ cao 10**.

Thứ tự gộp MAX: (A,B)@2 → (D,E)@3 → (AB,C)@6 → (ABC,DE)@10.

Dendrogram MAX:
```
  10 |        +----+-----+
     |        |          |
     |        |          |
     |        |          |
   6 |    +---+---+      |
     |    |       |      |
     |    |       |      |
   3 |    |       |    +-+--+
   2 |  +-+--+    |    |    |
     |  |    |    |    |    |
     |  |    |    |    |    |
     +--------------------------
        A    B    C    D    E
```

### Cắt thành 2 cụm
- MIN (cắt giữa 4 và 5, ví dụ ở 4.5): **{A,B} | {C,D,E}**
- MAX (cắt giữa 6 và 10, ví dụ ở 8): **{A,B,C} | {D,E}**
- Cắt thành 3 cụm (ví dụ ở 3.5 với cả hai): {A,B} | {C} | {D,E} — giống nhau.

⇒ **Cùng dữ liệu, linkage khác nhau cho cây khác nhau.** Điểm C "lưỡng lự" giữa hai nhóm, và quyết định phụ thuộc vào định nghĩa khoảng cách cụm.

### (c) Ghi chú về Group Average trên cùng ma trận (bổ sung — minh hoạ bẫy "hoà")
- Bước 1: AB@2; $d(AB,C)=(6+5)/2=5.5$, $d(AB,D)=9.5$, $d(AB,E)=8.5$.
- Bước 2: DE@3; $d(C,DE)=(4+7)/2=5.5$; $d(AB,DE)=(10+9+9+8)/4=9$.
- Bước 3: **hoà** $d(AB,C)=d(C,DE)=5.5$! Kết quả phụ thuộc quy tắc phá hoà (tie-breaking). Trên bài thi, nếu gặp hoà, **ghi rõ quy tắc mình chọn** (ví dụ "chọn cặp xuất hiện trước theo thứ tự chữ cái").
- Bước 4: cả hai trường hợp đều gộp cuối ở $47/6\approx7.83$.

### Bài tập luyện thêm (có lời giải) — hiện tượng "chuỗi" (chaining) của MIN
```
      A    B    C    D    E
A     0
B     1    0
C     9    8    0
D     4    5    6    0
E    10   11    7   12    0
```
**MIN**:
1. AB@1 → $d(AB,C)=8$, $d(AB,D)=4$, $d(AB,E)=10$.
2. Nhỏ nhất 4: (AB,D)@4 → $d(ABD,C)=\min(8,6)=6$, $d(ABD,E)=\min(10,12)=10$; $d(C,E)=7$.
3. Nhỏ nhất 6: (ABD,C)@6 → $d(ABCD,E)=\min(10,7)=7$.
4. (ABCD,E)@7.

```
   7 |            +----+----+
   6 |        +---+----+    |
     |        |        |    |
   4 |    +---+---+    |    |
     |    |       |    |    |
     |    |       |    |    |
   1 |  +-+--+    |    |    |
     |  |    |    |    |    |
     +--------------------------
        A    B    D    C    E
```
→ Mỗi bước chỉ "móc" thêm 1 điểm vào một cụm đang lớn dần: **chaining** (chuỗi).

**MAX**:
1. AB@1 → $d(AB,C)=\max(9,8)=9$, $d(AB,D)=\max(4,5)=5$, $d(AB,E)=11$.
2. Nhỏ nhất 5: (AB,D)@5 → $d(ABD,C)=\max(9,6)=9$, $d(ABD,E)=\max(11,12)=12$; $d(C,E)=7$.
3. Nhỏ nhất 7: (C,E)@7.
4. $d(ABD,CE)=\max(9,12)=12$ → gộp @12.

```
  12 |        +----+-----+
     |        |          |
     |        |          |
     |        |          |
     |        |          |
   7 |        |        +-+--+
     |        |        |    |
   5 |    +---+---+    |    |
     |    |       |    |    |
     |    |       |    |    |
     |    |       |    |    |
   1 |  +-+--+    |    |    |
     |  |    |    |    |    |
     +--------------------------
        A    B    D    C    E
```
→ 2 cụm: MIN cho {A,B,C,D} | {E}; MAX cho {A,B,D} | {C,E} — MAX cân bằng hơn.

### Quy trình làm bài tay (checklist)
1. Viết ma trận tam giác dưới; khoanh giá trị nhỏ nhất (nếu là **ma trận tương đồng / similarity** thì khoanh giá trị **lớn nhất**!).
2. Ghi "gộp (X,Y) @ h".
3. Viết lại ma trận: xoá hàng/cột X, Y, thêm hàng/cột XY. Chỉ hàng XY thay đổi; các ô khác **chép nguyên**.
4. Với mỗi cụm Z: MIN → min(d(Z,X), d(Z,Y)); MAX → max(...); AVG → trung bình **có trọng số** theo số điểm.
5. Lặp tới khi còn 1 cụm. Vẽ dendrogram với độ cao đúng tỉ lệ. Kiểm tra: N−1 lần gộp, độ cao **không giảm** (với MIN/MAX/AVG).

---

## 10. Phân tích sâu / đánh giá

**Vì sao phân cụm phân cấp tồn tại?**
- Không cần biết K trước; cho cấu trúc nhiều mức (taxonomy); chỉ cần ma trận khoảng cách (áp dụng được cho dữ liệu không phải vector: chuỗi ADN, văn bản, đồ thị — miễn có $d(x,y)$). K-means thì cần tính được trung bình (dữ liệu số).
- Kết quả **tất định (deterministic)** — không phụ thuộc khởi tạo ngẫu nhiên như K-means (trừ khi có hoà).

**MIN (single link)** — (chi tiết ở slides 83–84, phần sau)
- Mạnh: xử lý được hình dạng **không elip, kéo dài, cong** (vì chỉ cần "cầu" gần) → giải quyết đúng loại thất bại của K-means ở slide 64.
- Yếu: **nhạy cảm với nhiễu/ngoại lai**: một chuỗi điểm nhiễu nằm giữa hai cụm sẽ "bắc cầu" làm hai cụm dính vào nhau (**chaining effect**).

**MAX (complete link)** — (slides 87–88)
- Mạnh: ít nhạy với nhiễu, cho cụm gọn.
- Yếu: có xu hướng **cắt vỡ cụm lớn**, thiên về cụm **hình cầu (globular)** — gần với hành vi K-means.

**So với K-means**

| | K-means | Agglomerative |
|---|---|---|
| Cần K trước? | Có | Không (cắt dendrogram) |
| Kết quả | 1 phân hoạch phẳng | Cây cụm lồng nhau |
| Hàm mục tiêu | Tối thiểu SSE (toàn cục) | **Không** tối ưu hàm mục tiêu toàn cục; quyết định **tham lam (greedy)**, cục bộ |
| Có thể "sửa" quyết định? | Có (điểm đổi cụm qua các vòng lặp) | **Không** — gộp rồi không tách lại được (slide 95) |
| Bộ nhớ / thời gian | $O(N)$ / $O(NKId)$ | $O(N^2)$ / $O(N^3)$ (hoặc $O(N^2\log N)$) |
| Ngẫu nhiên | Có (khởi tạo) | Không |
| Dữ liệu lớn | Tốt | Kém |

- **Ward** là "phiên bản phân cấp của K-means" (slide 92) — cùng tiêu chí SSE; có thể dùng kết quả Ward để **khởi tạo K-means**.
- **Kết hợp**: K-means với nhiều cụm (slides 65–67) rồi agglomerative để ghép → tận dụng tốc độ của K-means và tính linh hoạt của hierarchical.

**Bẫy / trường hợp thất bại**
- Không có quy tắc chung chọn linkage: thử nhiều và đánh giá (cluster validity — phần sau của chương).
- Hoà (ties) → kết quả không duy nhất.
- Thang đo các thuộc tính khác nhau → **chuẩn hoá (normalize)** trước khi tính ma trận (slide 58).
- **(bổ sung)** Với centroid linkage, có thể xảy ra **đảo ngược (inversion)**: độ cao gộp sau nhỏ hơn bước trước → dendrogram "chồng ngược". MIN, MAX, Group Average, Ward không bị.

---

## 11. Dễ nhầm lẫn

1. **"MIN" / "MAX" nói về khoảng cách, không phải tương đồng.** Nếu đề cho **ma trận tương đồng (similarity)** (như slides 81, 85: I1…I5 với giá trị 1.00 trên đường chéo):
   - Luôn gộp cặp có **similarity lớn nhất**.
   - Single link (MIN) ⇒ $sim(C_i,C_j)=\max$ similarity giữa các cặp điểm.
   - Complete link (MAX) ⇒ $sim(C_i,C_j)=\min$ similarity.
   Ví dụ: sim(I1,I3)=0.10, sim(I2,I3)=0.70 → sau khi gộp {I1,I2}: single link $sim(\{I1,I2\},I3)=0.70$; complete link $=0.10$.
2. **Bước "gộp" luôn chọn cặp có khoảng cách nhỏ nhất — với cả MIN lẫn MAX.** MIN/MAX chỉ là cách **tính khoảng cách giữa cụm** khi cập nhật ma trận, không phải "gộp cặp xa nhất" với MAX.
3. **Group Average khi cập nhật** phải lấy trung bình **có trọng số theo số điểm**, không phải $(d_1+d_2)/2$ trừ khi hai cụm cùng kích thước.
4. **Group Average ≠ Distance between centroids** (ví dụ 8.4: 4.248 vs 4.123).
5. **Agglomerative ≠ divisive**: agglomerative = bottom-up (gộp); divisive = top-down (tách). Bisecting K-means là divisive.
6. **Thứ tự lá trong dendrogram** không có ý nghĩa; độ cao thì có. Hai điểm đứng cạnh nhau trên trục ngang chưa chắc gần nhau.
7. **Bước đầu tiên luôn giống nhau** với mọi linkage (gộp cặp điểm gần nhất) — khác biệt chỉ xuất hiện từ bước 2 trở đi.
8. **"Không cần chọn K"** không có nghĩa là không cần quyết định gì: vẫn phải chọn **chỗ cắt** và **linkage**.
9. **Single link ≠ "kém"**: nó tệ với nhiễu nhưng **tốt** với hình dạng không lồi — ngược với K-means/MAX.
10. Slide 65–67: dùng nhiều cụm **không** sửa hàm mục tiêu của K-means; nó chỉ tạo các mảnh thuần khiết, **vẫn cần bước ghép**.

---

## 12. Câu hỏi có thể ra thi (kèm lời giải ngắn)

**Q1.** Nêu 4 tình huống K-means hoạt động kém và giải thích nguyên nhân.
> Cụm khác kích thước, khác mật độ, không có dạng cầu, có ngoại lai. Nguyên nhân: tối thiểu SSE ưu tiên các cụm tròn cùng cỡ; ranh giới Voronoi tuyến tính (cụm lồi); trung bình nhạy với ngoại lai.

**Q2.** Đề xuất một cách khắc phục mà vẫn dùng K-means.
> Chạy K-means với K lớn hơn nhiều số cụm thật → các mảnh nhỏ thuần khiết, sau đó ghép các mảnh (ví dụ bằng agglomerative/single link trên các centroid). (slides 65–67)

**Q3.** Thế nào là dendrogram? Làm sao từ dendrogram có được 3 cụm?
> Cây ghi lại thứ tự và độ cao (khoảng cách) các lần gộp/tách. Cắt ngang ở độ cao sao cho đường cắt đi qua đúng 3 nhánh dọc (giữa độ cao lần gộp thứ N−3 và N−2).

**Q4.** Viết thuật toán phân cụm gộp cơ bản. Thao tác then chốt là gì?
> Xem mục 6. Then chốt: định nghĩa/tính khoảng cách giữa 2 cụm — chính nó phân biệt các thuật toán.

**Q5.** So sánh agglomerative và divisive.
> Bảng mục 5.

**Q6.** Định nghĩa MIN, MAX, Group Average, centroid; tính cho $C_1=\{(0,0),(0,2)\}$, $C_2=\{(3,0),(5,0)\}$.
> MIN=3; MAX=$\sqrt{29}\approx5.385$; AVG≈4.248; centroid=$\sqrt{17}\approx4.123$; Ward ΔSSE=17.

**Q7.** (Bài tính) Cho ma trận 5×5 ở mục 9, thực hiện single link và complete link, vẽ dendrogram, cho 2 cụm.
> MIN: AB@2, DE@3, C+DE@4, tất cả@5 → {A,B}|{C,D,E}. MAX: AB@2, DE@3, AB+C@6, tất cả@10 → {A,B,C}|{D,E}.

**Q8.** Cho ma trận tương đồng; single link gộp theo quy tắc nào?
> Gộp cặp similarity lớn nhất; similarity giữa 2 cụm = max similarity giữa các cặp điểm (tức khoảng cách nhỏ nhất).

**Q9.** Vì sao single link xử lý được hình dạng phức tạp nhưng nhạy với nhiễu? Complete link thì sao?
> Single: chỉ cần một cặp điểm gần → men theo hình dạng cong; nhưng vài điểm nhiễu tạo "cầu" nối hai cụm (chaining). Complete: dựa vào cặp xa nhất → cụm gọn, bền với nhiễu, nhưng hay cắt vỡ cụm lớn và thiên về cụm tròn.

**Q10.** Độ phức tạp của agglomerative? Vì sao không dùng được cho 1 triệu điểm?
> Bộ nhớ $O(N^2)$, thời gian $O(N^3)$ (hoặc $O(N^2\log N)$). Với $N=10^6$, ma trận có $10^{12}$ ô — quá lớn.

**Q11.** Đúng/Sai: "Phân cụm phân cấp tối thiểu hoá một hàm mục tiêu toàn cục." 
> Sai — quyết định tham lam, cục bộ, không thể hoàn tác (slide 95). (Ward tối thiểu *độ tăng* SSE ở mỗi bước, nhưng vẫn là tham lam.)

**Q12.** Cập nhật ma trận (dạng slide 75): $d(C1,C2)=7$, $d(C1,C5)=4$, $|C2|=3$, $|C5|=1$. Tính $d(C1,C2\cup C5)$ với MIN, MAX, AVG.
> MIN = 4; MAX = 7; AVG = $(3\cdot7+1\cdot4)/4 = 25/4 = 6.25$.

---

## 13. Tóm tắt cho tờ A4

**K-means hạn chế (sl.61–64)**: kích thước ≠, mật độ ≠, hình không cầu, outliers. Gốc: SSE thích cụm tròn đều; ranh giới Voronoi (trung trực) ⇒ cụm lồi; mean không bền.
**Khắc phục (sl.65–67)**: K lớn → mảnh nhỏ thuần → ghép lại (agglomerative).

**Hierarchical (sl.68)**: cụm lồng nhau, cây; **dendrogram** = thứ tự + độ cao gộp. Cắt ngang ở h → số nhánh bị cắt = số cụm. N điểm → N−1 lần gộp. Thứ tự lá vô nghĩa.
**Ưu (sl.69)**: không cần K; taxonomy (sinh học).
**Loại (sl.70)**: Agglomerative (bottom-up, gộp cặp gần nhất) / Divisive (top-down, tách; vd bisecting K-means). Dùng ma trận proximity, 1 cụm / bước.

**Thuật toán (sl.71)**: tính ma trận; mỗi điểm 1 cụm; REPEAT gộp 2 cụm gần nhất, cập nhật ma trận UNTIL 1 cụm. Then chốt: khoảng cách cụm.
**Chi phí**: bộ nhớ $O(N^2)$, thời gian $O(N^3)$ (heap: $O(N^2\log N)$).

**Khoảng cách cụm (sl.76–80)**:
- MIN/single: $\min_{x\in C_i,y\in C_j}d(x,y)$ — 1 cặp gần nhất; hình bất kỳ, nhạy nhiễu (chaining).
- MAX/complete: $\max d(x,y)$ — cặp xa nhất; bền nhiễu, cụm tròn, vỡ cụm lớn.
- AVG: $\frac{\sum\sum d(x,y)}{|C_i||C_j|}$ — trung gian.
- Centroid: $d(c_i,c_j)$ (có thể inversion).
- Ward: $\Delta SSE=\frac{n_in_j}{n_i+n_j}\lVert c_i-c_j\rVert^2$ — hierarchical K-means.
- MIN ≤ AVG ≤ MAX.

**Cập nhật khi gộp $i,j$** (với cụm $k$):
MIN: $\min(d_{ki},d_{kj})$; MAX: $\max(d_{ki},d_{kj})$; AVG: $\frac{n_id_{ki}+n_jd_{kj}}{n_i+n_j}$.

**Làm tay**: khoanh min (similarity → khoanh **max**) → ghi "gộp(X,Y)@h" → chép ma trận, chỉ đổi hàng XY → lặp. Bước 1 giống mọi linkage. Với similarity: single = max sim, complete = min sim. Hoà → ghi rõ quy tắc.
**Mẹo kiểm tra**: độ cao single link = các cạnh MST xếp tăng dần.

**Ví dụ thuộc lòng**: ma trận AB2 AC6 AD10 AE9 BC5 BD9 BE8 CD4 CE7 DE3 → MIN: AB2, DE3, C·DE4, all5; MAX: AB2, DE3, AB·C6, all10.

**Hạn chế chung (sl.95)**: gộp rồi không hoàn tác; không tối ưu hàm mục tiêu toàn cục; nhạy nhiễu / khó với cụm khác cỡ / vỡ cụm lớn (tuỳ linkage).
