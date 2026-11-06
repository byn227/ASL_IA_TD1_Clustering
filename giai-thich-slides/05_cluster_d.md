# Chương 8 (phần cuối): Hierarchical Clustering, cách đo độ gần giữa hai cụm (slide 79 → 95)

> **Lưu ý về phạm vi:** Trong bộ slide này, các slide 79–95 **không** nói về DBSCAN hay đánh giá cụm (SSE/silhouette/entropy). Chúng là phần cuối của **Hierarchical Clustering (phân cụm phân cấp)**: các cách định nghĩa độ gần giữa hai cụm (*inter-cluster similarity*: MIN, MAX, Group Average, Distance between Centroids, Ward), so sánh các phương pháp, độ phức tạp, và hạn chế. Slide 95 là slide cuối của Chương 8 (slide 96 đã sang Association Analysis). Tài liệu này bám sát đúng nội dung đó.
>
> Ký hiệu: "(bổ sung)" = kiến thức ngoài slide (thường lấy từ sách Tan–Steinbach–Kumar) để bạn hiểu sâu hơn hoặc làm bài tập.

---

## 0. Nhắc lại ngữ cảnh (slide 68–78, các bạn khác phụ trách, chỉ tóm tắt để nối mạch)

- **Agglomerative (gộp dần từ dưới lên)**: ban đầu mỗi điểm là một cụm. Ở mỗi bước, **gộp hai cụm gần nhau nhất**, rồi **cập nhật ma trận khoảng cách (proximity matrix)**. Lặp lại tới khi còn 1 cụm (hoặc k cụm).
- Câu hỏi then chốt (slide 75–76): sau khi gộp C2 ∪ C5, **khoảng cách từ cụm mới tới các cụm khác tính thế nào?** Các cách trả lời khác nhau sinh ra **các thuật toán khác nhau**. Đó chính là nội dung slide 77–92.

```
Thuật toán Agglomerative (slide 71)
1. Tính proximity matrix giữa mọi cặp điểm
2. Mỗi điểm là 1 cụm
3. Repeat
4.     Gộp 2 cụm gần nhau nhất (theo tiêu chí linkage đã chọn)
5.     Cập nhật proximity matrix (hàng/cột của cụm mới)
6. Until chỉ còn 1 cụm
```

---

## 1. Năm cách định nghĩa độ gần giữa hai cụm (slide 76–80)

Slide 76–80 lặp lại cùng một khung, mỗi lần tô đỏ một tiêu chí, kèm hình hai "đám mây" điểm và các đường nối minh họa:

| Tiêu chí | Tên khác | Hình trên slide | Ý nghĩa |
|---|---|---|---|
| **MIN** (slide 77) | Single link | 1 mũi tên nối **hai điểm gần nhau nhất** của hai cụm | Khoảng cách cụm = khoảng cách **nhỏ nhất** giữa 2 điểm thuộc 2 cụm |
| **MAX** (slide 78) | Complete link / complete linkage | 1 mũi tên nối **hai điểm xa nhau nhất** | Khoảng cách cụm = khoảng cách **lớn nhất** |
| **Group Average** (slide 79) | Average link (UPGMA, bổ sung) | **Mọi** đường nối giữa mọi cặp điểm (nhiều đường vàng) | **Trung bình** khoảng cách của tất cả các cặp |
| **Distance Between Centroids** (slide 80) | Centroid linkage | Mũi tên nối **hai dấu ×** (tâm cụm) | Khoảng cách giữa hai **trọng tâm** |
| **Objective-function based** (slide 76–80, dòng cuối) | Ví dụ: **Ward's Method** "uses squared error" | — | Gộp cặp cụm làm **tăng ít nhất** một hàm mục tiêu (SSE) |

### Công thức (với $d(x,y)$ là khoảng cách giữa hai điểm, $C_i, C_j$ là hai cụm, $|C|$ là số điểm)

- MIN: $\displaystyle d_{\min}(C_i,C_j)=\min_{x\in C_i,\,y\in C_j} d(x,y)$
- MAX: $\displaystyle d_{\max}(C_i,C_j)=\max_{x\in C_i,\,y\in C_j} d(x,y)$
- Group average (slide 89): $\displaystyle \text{proximity}(C_i,C_j)=\frac{\sum_{p_i\in C_i,\ p_j\in C_j}\text{proximity}(p_i,p_j)}{|C_i|\cdot|C_j|}$
- Centroid: $d(C_i,C_j)=d(c_i,c_j)$ với $c_i=\frac{1}{|C_i|}\sum_{x\in C_i}x$ là trọng tâm (centroid)
- Ward (slide 92, công thức là bổ sung): $\Delta(C_i,C_j)=SSE(C_i\cup C_j)-SSE(C_i)-SSE(C_j)=\dfrac{|C_i||C_j|}{|C_i|+|C_j|}\,\|c_i-c_j\|^2$, với $SSE(C)=\sum_{x\in C}\|x-c\|^2$.

### Hình dung (analogy)
Hai làng A và B, mỗi làng có vài ngôi nhà:
- **MIN**: "hai làng gần nhau" nếu **có một cặp nhà** sát nhau (chỉ cần một cây cầu là đủ).
- **MAX**: hai làng chỉ gần nhau nếu **cả hai nhà xa nhất** cũng gần (mọi người đều phải gần nhau).
- **Group average**: lấy **trung bình** quãng đường giữa mọi cặp nhà.
- **Centroid**: khoảng cách giữa **hai trung tâm làng**.
- **Ward**: nếu sáp nhập hai làng thành một xã, **tổng bình phương quãng đường từ mỗi nhà đến trung tâm xã tăng thêm bao nhiêu**? Gộp cặp làng làm tăng ít nhất.

> ⚠️ **Similarity ngược với distance.** Slide 81/85/89 dùng **ma trận độ tương đồng (similarity)**: số càng **lớn** thì càng **gần**. Khi đó:
> - MIN (theo khoảng cách) tương ứng với **max similarity** giữa các cặp.
> - MAX (theo khoảng cách) tương ứng với **min similarity**.
> - Ở mỗi bước, gộp cặp cụm có **similarity lớn nhất** (= khoảng cách nhỏ nhất).

---

## 2. MIN / Single Link (slide 81–84)

### 2.1 Định nghĩa (slide 81)
"Độ tương đồng của hai cụm dựa trên **hai điểm giống nhau nhất (gần nhất)** thuộc hai cụm khác nhau. Nó được quyết định bởi **một cặp điểm**, tức là **một cạnh (link)** trong đồ thị lân cận (proximity graph)". Vì thế mới gọi là *single link*.

Liên hệ với đồ thị (bổ sung): single link tương đương với việc xây **cây khung nhỏ nhất (Minimum Spanning Tree, MST)** rồi lần lượt cắt các cạnh dài nhất. Đây cũng là MST-based divisive clustering trong sách.

### 2.2 Ví dụ trên slide 81: ma trận similarity 5 phần tử (I1…I5)

|    | I1 | I2 | I3 | I4 | I5 |
|----|----|----|----|----|----|
| I1 | 1.00 | **0.90** | 0.10 | 0.65 | 0.20 |
| I2 | 0.90 | 1.00 | 0.70 | 0.60 | 0.50 |
| I3 | 0.10 | 0.70 | 1.00 | 0.40 | 0.30 |
| I4 | 0.65 | 0.60 | 0.40 | 1.00 | **0.80** |
| I5 | 0.20 | 0.50 | 0.30 | 0.80 | 1.00 |

**Lần theo bằng tay (single link, similarity nên lấy MAX của các cặp):**

- **Bước 1:** cặp có similarity lớn nhất là (1,2) = 0.90. Gộp thành **{1,2}** tại mức 0.90.
  Cập nhật:
  - sim({1,2},3) = max(0.10, 0.70) = **0.70**
  - sim({1,2},4) = max(0.65, 0.60) = **0.65**
  - sim({1,2},5) = max(0.20, 0.50) = **0.50**
  - giữ nguyên: (3,4)=0.40, (3,5)=0.30, (4,5)=0.80
- **Bước 2:** lớn nhất là (4,5) = 0.80. Gộp **{4,5}** tại 0.80.
  - sim({1,2},{4,5}) = max(0.65, 0.20, 0.60, 0.50) = **0.65**
  - sim(3,{4,5}) = max(0.40, 0.30) = **0.40**
  - sim({1,2},3) = 0.70
- **Bước 3:** lớn nhất là 0.70. Gộp **{1,2,3}** tại 0.70.
- **Bước 4:** sim({1,2,3},{4,5}) = max(0.65, 0.40) = 0.65. Gộp tất cả tại 0.65.

Thứ tự gộp: {1,2}@0.90 → {4,5}@0.80 → {1,2,3}@0.70 → toàn bộ @0.65. **Khớp với dendrogram slide 81** (1–2 nối thấp nhất, 4–5 kế tiếp, 3 nhập vào {1,2}, rồi nối toàn bộ).

### 2.3 Slide 82: Hierarchical Clustering MIN trên 6 điểm
Hình trái (*Nested Clusters*) là các vòng lồng nhau, số đỏ là **thứ tự gộp**:
1 = {3,6}, 2 = {2,5}, 3 = {2,5,3,6}, 4 = thêm điểm 4, 5 = thêm điểm 1.
Hình phải là **dendrogram** (trục tung = khoảng cách lúc gộp, từ 0 đến khoảng 0.2), thứ tự lá: 3, 6, 2, 5, 4, 1.

**(bổ sung) Lần theo bằng tay với dữ liệu gốc trong sách Tan (Table 8.3–8.4).** Slide không ghi tọa độ, nhưng các dendrogram trên slide được vẽ từ bộ dữ liệu này:

Tọa độ: p1(0.40,0.53), p2(0.22,0.38), p3(0.35,0.32), p4(0.26,0.19), p5(0.08,0.41), p6(0.45,0.30).

Ma trận khoảng cách Euclid (theo sách, làm tròn 2 chữ số):

|    | p1 | p2 | p3 | p4 | p5 | p6 |
|----|----|----|----|----|----|----|
| p1 | 0 | 0.24 | 0.22 | 0.37 | 0.34 | 0.23 |
| p2 | 0.24 | 0 | 0.15 | 0.20 | **0.14** | 0.25 |
| p3 | 0.22 | 0.15 | 0 | 0.15 | 0.28 | **0.11** |
| p4 | 0.37 | 0.20 | 0.15 | 0 | 0.29 | 0.22 |
| p5 | 0.34 | 0.14 | 0.28 | 0.29 | 0 | 0.39 |
| p6 | 0.23 | 0.25 | 0.11 | 0.22 | 0.39 | 0 |

Single link (ở đây là khoảng cách nên lấy MIN):
1. Nhỏ nhất: d(3,6)=0.11. Gộp **{3,6}** @0.11.
2. Tiếp theo: d(2,5)=0.14. Gộp **{2,5}** @0.14.
3. Tính lại:
   - d({3,6},{2,5}) = min(0.15, 0.28, 0.25, 0.39) = **0.15**
   - d({3,6},4) = min(0.15, 0.22) = **0.15**
   - d({3,6},1) = min(0.22, 0.23) = 0.22
   - d({2,5},1) = min(0.24, 0.34) = 0.24
   - d({2,5},4) = min(0.20, 0.29) = 0.20
   - d(1,4) = 0.37

   Có **hoà (tie)** ở 0.15. Slide chọn gộp {3,6} với {2,5} trước: **{2,3,5,6}** @0.15.
4. d({2,3,5,6},4) = min(0.20, 0.15, 0.29, 0.22) = 0.15. Gộp điểm 4 @0.15.
5. d(rest,1) = min(0.24, 0.22, 0.37, 0.34, 0.23) = 0.22. Gộp điểm 1 @0.22.

Kết quả khớp slide 82 (bước 3 và 4 cùng ở mức khoảng 0.15 trên dendrogram).

### 2.4 Điểm mạnh của MIN (slide 83)
Hình: hai cụm, một cụm nhỏ bên trái và một cụm **to, hình dạng không đều** bên phải, cách nhau một khoảng trống rõ. MIN tách đúng thành 2 cụm (xanh/đỏ).
**"Can handle non-elliptical shapes"**: xử lý được cụm **không có dạng elip/cầu**, kể cả cụm dài, cong hay kích thước khác nhau, miễn là chúng **tách rời nhau**.
Lý do: chỉ cần các điểm "nối tiếp nhau" thành chuỗi là thuộc cùng cụm, không quan tâm hình dạng tổng thể.

### 2.5 Hạn chế của MIN (slide 84)
Hình: hai đám điểm nằm sát nhau, có **các điểm nhiễu rải rác ở giữa**. Kết quả 2 cụm của MIN bị sai, ranh giới xanh/đỏ không tự nhiên.
**"Sensitive to noise and outliers"**: vài điểm nhiễu nằm giữa hai cụm sẽ tạo thành **"cây cầu"**, và MIN gộp hai cụm thật làm một. Hiện tượng này gọi là **hiệu ứng dây chuyền (chaining effect)** (bổ sung).

Ví dụ 1D (bổ sung): A = {0, 1, 2}, B = {10, 11, 12}, nhiễu tại 4, 6, 8. Mọi khoảng cách liên tiếp đều ≤ 2, nên single link gộp **cả dãy thành một cụm** trước khi kịp tách A và B (khoảng cách xa nhất giữa hai điểm liên tiếp chỉ là 2).

---

## 3. MAX / Complete Linkage (slide 85–88)

### 3.1 Định nghĩa (slide 85)
"Độ tương đồng của hai cụm dựa trên **hai điểm ít giống nhau nhất (xa nhau nhất)** thuộc hai cụm. Nó được quyết định bởi **tất cả các cặp điểm** trong hai cụm." (Muốn hai cụm "gần" theo MAX thì **mọi** cặp đều phải gần, tức là cụm sau khi gộp phải có **đường kính (diameter)** nhỏ.)

### 3.2 Ví dụ slide 85 (cùng ma trận similarity, lấy MIN similarity của các cặp)
- **Bước 1:** {1,2} @0.90.
  - sim({1,2},3) = min(0.10, 0.70) = **0.10**
  - sim({1,2},4) = min(0.65, 0.60) = **0.60**
  - sim({1,2},5) = min(0.20, 0.50) = **0.20**
  - (3,4)=0.40, (3,5)=0.30, (4,5)=0.80
- **Bước 2:** {4,5} @0.80.
  - sim({1,2},{4,5}) = min(0.65, 0.20, 0.60, 0.50) = **0.20**
  - sim(3,{4,5}) = min(0.40, 0.30) = **0.30**
  - sim({1,2},3) = 0.10
- **Bước 3:** lớn nhất là 0.30. Gộp **{3,4,5}** @0.30. *(Khác single link: điểm 3 không về với {1,2} nữa, vì 3 rất khác 1, với sim(1,3)=0.10.)*
- **Bước 4:** sim({1,2},{3,4,5}) = min(0.10, 0.65, 0.20, 0.70, 0.60, 0.50) = 0.10. Gộp tất cả @0.10.

Thứ tự gộp khớp dendrogram slide 85: {1,2} và {4,5}, rồi 3 nhập {4,5}, rồi toàn bộ.

### 3.3 Slide 86: MAX trên 6 điểm
Thứ tự (số đỏ): 1 = {3,6}, 2 = {2,5}, 3 = {3,6,4}, 4 = {2,5,1}, 5 = toàn bộ. Dendrogram cao tới khoảng 0.4, thứ tự lá 3, 6, 4, 1, 2, 5.

**(bổ sung) Tính tay với bảng khoảng cách ở trên:**
1. {3,6} @0.11; 2. {2,5} @0.14.
3. Tính lại:
   - d({3,6},4) = max(0.15, 0.22) = **0.22**
   - d({3,6},1) = max(0.22, 0.23) = 0.23
   - d({2,5},4) = max(0.20, 0.29) = 0.29
   - d({2,5},1) = max(0.24, 0.34) = 0.34
   - d({3,6},{2,5}) = max(0.15, 0.28, 0.25, 0.39) = 0.39
   - d(1,4) = 0.37

   Gộp **{3,6,4}** @0.22.
4. Tính lại:
   - d({3,6,4},1) = max(0.22, 0.23, 0.37) = 0.37
   - d({3,6,4},{2,5}) = max(0.39, 0.29) = 0.39
   - d({2,5},1) = **0.34**

   Gộp **{1,2,5}** @0.34.
5. Gộp toàn bộ @0.39 (= d(5,6)).

Chú ý: ở bước 3 của single link, {3,6} và {2,5} gần nhau (0.15), nhưng với complete link chúng lại **xa nhất** (0.39), vì d(5,6)=0.39 kéo lên.

### 3.4 Điểm mạnh của MAX (slide 87)
Hình: cùng dữ liệu có nhiễu như slide 84. MAX cho 2 cụm hợp lý hơn.
**"Less susceptible to noise and outliers"**: một vài điểm nhiễu làm "cầu" không đủ để gộp hai cụm, vì MAX nhìn vào cặp **xa nhất**, mà cặp xa nhất giữa hai cụm thật vẫn rất xa.

### 3.5 Hạn chế của MAX (slide 88)
Hình: một cụm **nhỏ** bên trái và một cụm **rất lớn** (hình tròn) bên phải. Kết quả 2 cụm: cụm lớn **bị cắt đôi**, nửa trái của nó bị gộp với cụm nhỏ (màu xanh), nửa phải là màu đỏ.
- **"Tends to break large clusters"**: có xu hướng **bẻ gãy cụm lớn**.
- **"Biased towards globular clusters"**: thiên vị cụm **dạng cầu, tròn, cỡ tương tự nhau**.

**Vì sao?** Complete link tối thiểu hoá "đường kính" của cụm gộp. Cụm lớn có đường kính rất lớn, nên giữ nó nguyên vẹn rồi gộp với cụm nhỏ tạo ra đường kính khổng lồ. Ngược lại, chẻ đôi cụm lớn và ghép nửa trái với cụm nhỏ thì đường kính mỗi phần nhỏ hơn. Thuật toán tham lam (greedy) chọn phương án sau.

---

## 4. Group Average (slide 89–91)

### 4.1 Định nghĩa và công thức (slide 89)
"Độ gần của hai cụm là **trung bình các độ gần từng cặp** giữa các điểm của hai cụm":
$$\text{proximity}(C_i,C_j)=\frac{\displaystyle\sum_{p_i\in C_i,\ p_j\in C_j}\text{proximity}(p_i,p_j)}{|C_i|\cdot|C_j|}$$
- Tử số: tổng proximity của **tất cả** $|C_i|\times|C_j|$ cặp (mỗi cặp gồm một điểm bên này và một điểm bên kia).
- Mẫu số: số cặp.

**"Need to use average connectivity for scalability since total proximity favors large clusters"**: phải **chia cho số cặp** (lấy trung bình), vì nếu dùng **tổng** (total proximity), cụm càng to thì tổng càng lớn (nhiều cặp hơn). Khi đó cụm to luôn có vẻ "giống" mọi thứ hơn, và thuật toán sẽ cứ gộp thêm vào cụm to. Ví dụ: cụm 100 điểm, mỗi cặp sim 0.1, cho tổng = 10 với một điểm mới; cụm 2 điểm, mỗi cặp sim 0.9, chỉ cho tổng 1.8. Dùng tổng thì chọn sai; dùng trung bình (0.1 so với 0.9) thì chọn đúng.

**(bổ sung) Mẹo tính nhanh khi cập nhật:**
$$d(A\cup B,\,C)=\frac{|A|\,d(A,C)+|B|\,d(B,C)}{|A|+|B|}$$
(trung bình có trọng số theo kích thước). Như vậy không phải cộng lại mọi cặp từ đầu.

### 4.2 Lần theo trên ma trận slide 89 (similarity, gộp cặp có trung bình lớn nhất)
- **Bước 1:** {1,2} @0.90.
  - sim({1,2},3) = (0.10+0.70)/2 = **0.40**
  - sim({1,2},4) = (0.65+0.60)/2 = **0.625**
  - sim({1,2},5) = (0.20+0.50)/2 = **0.35**
  - (3,4)=0.40, (3,5)=0.30, (4,5)=0.80
- **Bước 2:** {4,5} @0.80.
  - sim({1,2},{4,5}) = (0.65+0.20+0.60+0.50)/4 = 1.95/4 = **0.4875**
  - sim(3,{4,5}) = (0.40+0.30)/2 = **0.35**
  - sim({1,2},3) = 0.40
- **Bước 3:** lớn nhất là 0.4875. Gộp **{1,2,4,5}** @0.4875.
- **Bước 4:** sim(3,{1,2,4,5}) = (0.10+0.70+0.40+0.30)/4 = 1.50/4 = 0.375. Gộp tất cả @0.375.

> ⚠️ **Mâu thuẫn trên slide:** Dendrogram vẽ ở slide 89 **giống hệt** slide 81 (single link: 3 nhập {1,2}, rồi mới gộp với {4,5}). Tính tay như trên (đã kiểm tra lại bằng chương trình) cho thấy với group average, {1,2} gộp với **{4,5}** trước (0.4875 > 0.40 > 0.35), và **3 nhập cuối cùng**. Nếu đề thi cho ma trận này, hãy **tin vào phép tính**, đừng chép dendrogram của slide 89.

So sánh 3 phương pháp trên cùng ma trận:

| | Bước 3 | Bước 4 (mức gộp cuối) |
|---|---|---|
| Single (MIN) | {1,2}+3 @0.70 | @0.65 |
| Complete (MAX) | 3+{4,5} @0.30 | @0.10 |
| Group Average | {1,2}+{4,5} @0.4875 | @0.375 |

Điểm 3 là "kẻ nước đôi": rất giống 2 (0.70) nhưng rất khác 1 (0.10). Single link chỉ thấy 0.70, complete link chỉ thấy 0.10, còn average thấy trung bình 0.40 và chọn phương án khác hẳn.

### 4.3 Slide 90: Group average trên 6 điểm
Hình slide 90: thứ tự 1 = {3,6}, 2 = {2,5}, 3 = {3,6,4}, 4 = {3,6,4,1}, 5 = toàn bộ. Dendrogram (thứ tự lá 3, 6, 4, 1, 2, 5) cao khoảng 0.27.

> ⚠️ **Mâu thuẫn trên slide:** Hình ở slide 90 **trùng với hình "Ward's Method" ở slide 93**, chứ không trùng với hình "Group Average" ở slide 93. Ở slide 93, Group Average có bước 4 là {3,6,4} ∪ {2,5} và điểm 1 vào cuối cùng. Tính tay (bổ sung, theo bảng khoảng cách của sách) xác nhận **phiên bản của slide 93**:

1. {3,6} @0.11; 2. {2,5} @0.14.
3. Tính lại:
   - d({3,6},4) = (0.15+0.22)/2 = **0.185**
   - d({3,6},1) = (0.22+0.23)/2 = 0.225
   - d({2,5},4) = (0.20+0.29)/2 = 0.245
   - d({3,6},{2,5}) = (0.15+0.28+0.25+0.39)/4 = 1.07/4 = 0.2675
   - d({2,5},1) = (0.24+0.34)/2 = 0.29

   Gộp **{3,6,4}** @0.185.
4. Tính lại:
   - d({3,6,4},1) = (0.22+0.23+0.37)/3 = 0.82/3 ≈ 0.273
   - d({3,6,4},{2,5}) = (0.15+0.28+0.25+0.39+0.20+0.29)/6 = 1.56/6 = **0.26**
   - d({2,5},1) = 0.29

   Gộp **{2,3,4,5,6}** @0.26.
5. d(1, rest) = (0.24+0.22+0.37+0.34+0.23)/5 = 1.40/5 = 0.28. Gộp điểm 1 @0.28.

(Kết quả này trùng với lời giải trong sách Tan.)

### 4.4 Đánh giá (slide 91)
- **"Compromise between Single and Complete Link"**: là **sự dung hoà** giữa single và complete link.
- **Strengths:** **ít nhạy với nhiễu và ngoại lai** (một điểm nhiễu chỉ đóng góp 1 phần trong rất nhiều cặp, nên bị "pha loãng").
- **Limitations:** **thiên vị cụm dạng cầu (globular)**.

---

## 5. Distance Between Centroids (slide 80)

Slide chỉ liệt kê tiêu chí này (hình: mũi tên giữa hai dấu × là hai trọng tâm), **không có slide riêng**.
$d(C_i,C_j)=\|c_i-c_j\|$.

**(bổ sung) Cạm bẫy: "đảo ngược" (inversion / non-monotonic).** Với centroid linkage, khoảng cách lúc gộp ở bước sau **có thể nhỏ hơn** bước trước, nên dendrogram bị "đi xuống". Ví dụ: A(0,0), B(2,0), C(1,1.8).
- d(A,B) = 2; d(A,C) = d(B,C) = √(1+3.24) ≈ 2.06. Gộp {A,B} @2.
- Centroid của {A,B} là (1,0), cách C đúng **1.8 < 2**, nên lần gộp thứ hai xảy ra ở mức **thấp hơn** lần đầu.

MIN, MAX, Group average và Ward thì không bị hiện tượng này (chúng có tính đơn điệu).

---

## 6. Ward's Method (slide 92)

### 6.1 Nội dung slide
- **"Similarity of two clusters is based on the increase in squared error when two clusters are merged"**: độ gần của hai cụm = **lượng SSE tăng thêm** khi gộp chúng. Gộp cặp làm SSE tăng **ít nhất**.
- **"Similar to group average if distance between points is distance squared"**: giống group average nếu dùng **bình phương khoảng cách**.
- **Less susceptible to noise and outliers** (ít nhạy nhiễu).
- **Biased towards globular clusters** (thiên vị cụm cầu).
- **"Hierarchical analogue of K-means"**: là **phiên bản phân cấp của K-means**. **"Can be used to initialize K-means"**: dùng để **khởi tạo** K-means.

### 6.2 Công thức (bổ sung)
$$SSE(C)=\sum_{x\in C}\|x-c\|^2,\qquad \Delta(A,B)=SSE(A\cup B)-SSE(A)-SSE(B)=\frac{|A|\,|B|}{|A|+|B|}\,\|c_A-c_B\|^2$$
- $c_A, c_B$: trọng tâm hai cụm; $|A|, |B|$: kích thước.
- Với hai điểm đơn: $\Delta = d^2/2$.
- Tổng mọi $\Delta$ dọc theo quá trình gộp = SSE của toàn bộ dữ liệu (vì ban đầu SSE = 0).

### 6.3 Lần theo tay, ví dụ 1D (bổ sung): điểm {0, 1, 3, 7, 10}
- Ban đầu (cặp kề nhau): Δ(0,1) = 1²/2 = **0.5**; Δ(1,3) = 4/2 = 2; Δ(3,7) = 16/2 = 8; Δ(7,10) = 9/2 = 4.5.
- **Bước 1:** gộp {0,1}, Δ = 0.5 (centroid 0.5, SSE = 0.5).
- **Bước 2:**
  - Δ({0,1},3) = (2·1/3)·(3−0.5)² = (2/3)·6.25 ≈ **4.167**
  - Δ(7,10) = 4.5
  - Δ(3,7) = 8

  Gộp **{0,1,3}**, Δ ≈ 4.167.
  Kiểm tra: centroid 4/3, SSE = (16+1+25)/9 = 42/9 ≈ 4.667 = 0.5 + 4.167 ✓.
- **Bước 3:**
  - Δ({0,1,3},7) = (3/4)·(7−4/3)² = 0.75·(17/3)² ≈ 24.08
  - Δ(7,10) = **4.5**

  Gộp **{7,10}**.
- **Bước 4:** Δ({0,1,3},{7,10}) = (3·2/5)·(8.5−4/3)² = 1.2·(43/6)² ≈ 1.2·51.36 ≈ **61.63**.
- Kiểm tra tổng: 0.5 + 4.167 + 4.5 + 61.63 ≈ 70.8. SSE toàn bộ: mean 4.2, độ lệch −4.2, −3.2, −1.2, 2.8, 5.8, bình phương 17.64 + 10.24 + 1.44 + 7.84 + 33.64 = **70.8** ✓.

### 6.4 Ward trên 6 điểm (slide 93, tính tay bổ sung từ tọa độ)
Bước 1–3 giống group average: {3,6}, {2,5}, {3,6,4}. **Bước 4 khác:**
- $c_{346}$ = (0.3533, 0.27); $c_{25}$ = (0.15, 0.395); p1 = (0.40, 0.53).
- Δ({3,4,6},1) = (3·1/4)·(0.0467² + 0.26²) = 0.75·0.0698 ≈ **0.0523**
- Δ({2,5},1) = (2·1/3)·(0.25² + 0.135²) = 0.667·0.0807 ≈ 0.0538
- Δ({3,4,6},{2,5}) = (3·2/5)·(0.2033² + 0.125²) = 1.2·0.0570 ≈ 0.0684

Vậy Ward gộp **{1,3,4,6}** (khớp slide 93 "Ward's Method"), còn group average gộp {2,5} với {3,4,6}. Hệ số $\frac{|A||B|}{|A|+|B|}$ "phạt" việc gộp hai cụm **cùng lớn**, nên Ward thích thêm 1 điểm lẻ vào cụm lớn hơn.

### 6.5 Vì sao "hierarchical analogue of K-means"?
K-means tối thiểu hoá **SSE** cho K cố định. Ward cũng hướng tới SSE nhỏ, nhưng làm **tham lam từng bước** (mỗi bước chọn phép gộp tăng SSE ít nhất). **Khởi tạo K-means:** cắt dendrogram Ward ở mức có K cụm, lấy **trọng tâm** của K cụm đó làm centroid ban đầu cho K-means. Cách này tránh khởi tạo ngẫu nhiên tệ, và K-means sau đó tinh chỉnh tiếp (sửa được những phép gộp sai mà phân cấp không "undo" được, xem slide 95).

---

## 7. So sánh tổng hợp (slide 93)

Slide 93 đặt 4 hình nested-cluster của **cùng 6 điểm** cạnh nhau:

| Phương pháp | Bước 1 | Bước 2 | Bước 3 | Bước 4 | Bước 5 |
|---|---|---|---|---|---|
| **MIN** | {3,6} | {2,5} | {2,5}∪{3,6} | +4 | +1 |
| **MAX** | {3,6} | {2,5} | {3,6}+4 | {2,5}+1 | tất cả |
| **Group Average** | {3,6} | {2,5} | {3,6}+4 | {3,6,4}∪{2,5} | +1 |
| **Ward** | {3,6} | {2,5} | {3,6}+4 | {3,6,4}+1 | +{2,5} |

Nhận xét:
- Hai bước đầu **luôn giống nhau** ở mọi phương pháp, vì khi các cụm chỉ có 1 điểm thì MIN = MAX = AVG = khoảng cách giữa hai điểm, và Ward = d²/2 nên cùng thứ tự.
- Khác biệt chỉ xuất hiện khi các cụm có **≥2 điểm**.
- Nếu cắt ở **2 cụm**: MIN cho {1} | {2,3,4,5,6} (điểm 1 bị tách riêng như một outlier); MAX cho {1,2,5} | {3,4,6}; Group average cho {1} | {2,3,4,5,6}; Ward cho {2,5} | {1,3,4,6}.

### Bảng tổng kết ưu/nhược

| | Ưu điểm | Nhược điểm |
|---|---|---|
| MIN (single) | Cụm hình dạng bất kỳ, không elip (slide 83) | Nhạy nhiễu/outlier, hiệu ứng dây chuyền (slide 84) |
| MAX (complete) | Ít nhạy nhiễu (slide 87) | Bẻ gãy cụm lớn, thiên vị cụm cầu (slide 88) |
| Group average | Dung hoà, ít nhạy nhiễu (slide 91) | Thiên vị cụm cầu (slide 91) |
| Ward | Ít nhạy nhiễu, tương tự K-means, dùng để khởi tạo K-means (slide 92) | Thiên vị cụm cầu (slide 92) |
| Centroid | Trực quan (bổ sung) | Có thể bị inversion (bổ sung) |

---

## 8. Độ phức tạp thời gian và bộ nhớ (slide 94)

- **Bộ nhớ $O(N^2)$**, vì phải lưu **proximity matrix** $N\times N$ ($N$ = số điểm). Ví dụ (bổ sung): N = 100 000, ma trận đối xứng chỉ lưu nửa, khoảng $5\times10^9$ số; với 8 byte/số là khoảng 40 GB. Không khả thi.
- **Thời gian $O(N^3)$** trong nhiều trường hợp: có **N bước** (chính xác là N−1 lần gộp), mỗi bước phải **tìm kiếm và cập nhật** ma trận kích thước $N^2$. Tổng là $N\cdot N^2$.
- Có thể giảm xuống **$O(N^2\log N)$** với một số cách tiếp cận (bổ sung: dùng hàng đợi ưu tiên/heap cho mỗi hàng để tìm cặp gần nhất nhanh hơn). Single link có thể làm $O(N^2)$ qua MST (bổ sung).

So với K-means: thời gian $O(I\cdot K\cdot N\cdot d)$, gần tuyến tính theo N (bổ sung). Vì vậy hierarchical **không dùng được cho dữ liệu lớn**, trong khi K-means thì dùng được.

---

## 9. Vấn đề và hạn chế của Hierarchical Clustering (slide 95)

1. **"Once a decision is made to combine two clusters, it cannot be undone"**: quyết định gộp **không thể hoàn tác**. Đây là thuật toán **tham lam (greedy)**: một lần gộp sai sớm (do nhiễu chẳng hạn) sẽ lan truyền đến cuối. *Khắc phục (bổ sung):* chạy K-means sau để tinh chỉnh (xem Ward → K-means).
2. **"No objective function is directly minimized"**: **không có hàm mục tiêu toàn cục** nào được tối thiểu hoá trực tiếp (khác K-means tối thiểu SSE). Ngay cả Ward cũng chỉ tối ưu **cục bộ** ở mỗi bước, không đảm bảo SSE toàn cục nhỏ nhất cho K cụm.
3. Các biến thể khác nhau gặp một hoặc vài vấn đề sau:
   - **Nhạy nhiễu và outlier** (MIN).
   - **Khó xử lý cụm khác kích thước và hình lồi (convex shapes)** (MAX, Average, Ward thiên vị cụm cầu, cùng cỡ).
   - **Bẻ gãy cụm lớn (breaking large clusters)** (MAX).

---

## 10. Phân tích sâu / đánh giá

- **Vì sao có nhiều linkage?** Agglomerative chỉ định nghĩa *khung* thuật toán. "Khoảng cách giữa hai cụm" là một **lựa chọn mô hình**, và mỗi lựa chọn ngầm giả định một kiểu cụm:
  - MIN: cụm = thành phần **liên thông** (connectivity).
  - MAX, Average, Ward: cụm = khối **gọn, cầu** (compactness).
- **Chọn linkage thế nào (bổ sung):**
  - Dữ liệu sạch, cụm hình dạng lạ, tách rời: **single**.
  - Có nhiễu, cụm gọn, cỡ tương tự: **complete / average / Ward**.
  - Muốn kết quả giống K-means, hoặc để khởi tạo K-means: **Ward**.
  - Average là lựa chọn "an toàn" mặc định.
- **Chọn số cụm:** không cần K trước (slide 69); **cắt dendrogram** ở mức phù hợp. Mẹo (bổ sung): cắt ở chỗ có **khoảng nhảy độ cao lớn** giữa hai lần gộp liên tiếp. Ví dụ với MAX trên 6 điểm, heights là 0.11, 0.14, 0.22, 0.34, 0.39; bước nhảy 0.22 → 0.34 lớn, nên cắt ở đó cho 3 cụm {3,4,6}, {2,5}, {1}.
- **Chỉ cần ma trận khoảng cách** (không cần tọa độ) cho MIN/MAX/Average. Do đó dùng được cho dữ liệu phi số (chuỗi, đồ thị…). Centroid và Ward **cần không gian Euclid** (cần tính trọng tâm).
- **Tie (hoà):** khi hai cặp có cùng khoảng cách, kết quả phụ thuộc cách phá hoà (thấy ở MIN, slide 82). Đề thi thường nói rõ quy tắc; nếu không thì ghi rõ lựa chọn của mình.
- **Liên hệ K-means:** K-means dạng phẳng (partitional), cần K, nhanh, khởi tạo ngẫu nhiên, có hàm mục tiêu SSE. Hierarchical thì lồng nhau, không cần K, chậm, tất định (deterministic), không có hàm mục tiêu toàn cục. Ward là cầu nối giữa hai bên.

---

## 11. Dễ nhầm lẫn

1. **MIN/MAX nói về khoảng cách, không phải similarity.** Với **ma trận similarity** (slide 81/85/89): single link lấy **max** similarity, complete link lấy **min** similarity, và luôn gộp cặp có **similarity lớn nhất**.
2. **"Complete link" không có nghĩa là "nối đầy đủ, nên gộp nhiều"**. Nó dùng cặp **xa nhất**, nên **khắt khe nhất** trong việc gộp.
3. **Single link nhạy nhiễu, complete link không** (đừng đảo ngược). Nhưng complete link lại **bẻ gãy cụm lớn**.
4. **Group average dùng trung bình, không phải tổng.** Dùng tổng sẽ thiên vị cụm lớn (slide 89).
5. **Group average ≠ Centroid.** Trung bình các khoảng cách giữa mọi cặp điểm khác với khoảng cách giữa hai trung bình. Ví dụ 1D: A = {0, 2}, B = {5}. Average = (5+3)/2 = 4; centroid = |1−5| = 4 (bằng nhau trong trường hợp 1D một phía). Nhưng A = {−1, 1}, B = {0}: Average = (1+1)/2 = 1, còn centroid = 0.
6. **Ward ≠ Centroid**, dù cả hai đều dùng trọng tâm. Ward nhân thêm $\frac{|A||B|}{|A|+|B|}$ và dùng **bình phương**.
7. **Hai bước đầu giống nhau** ở mọi linkage (cụm 1 điểm). Đừng ngạc nhiên khi các dendrogram chỉ khác nhau ở phía trên.
8. **Dendrogram slide 89 và hình slide 90 không khớp với phép tính** (xem §4.2, §4.3). Tin vào tính toán và hình slide 93.
9. **Độ phức tạp:** **bộ nhớ** là $O(N^2)$, **thời gian** là $O(N^3)$ (có thể giảm còn $O(N^2\log N)$). Đừng đảo hai cái này.
10. **"No objective function"** không có nghĩa là Ward không dùng SSE. Ward dùng SSE **cục bộ ở từng bước**, chứ không tối ưu toàn cục.

---

## 12. Câu hỏi có thể ra thi (kèm lời giải ngắn)

**Q1. Cho ma trận similarity (slide 81). Thực hiện single link, complete link, group average; vẽ dendrogram.**
→ Xem §2.2, §3.2, §4.2.
- Single: {1,2}@0.90, {4,5}@0.80, {1,2,3}@0.70, all@0.65.
- Complete: {1,2}@0.90, {4,5}@0.80, {3,4,5}@0.30, all@0.10.
- Average: {1,2}@0.90, {4,5}@0.80, {1,2,4,5}@0.4875, all@0.375.

**Q2. Cho ma trận khoảng cách 6 điểm (§2.3). Tính MIN/MAX/AVG. Cắt thành 2 cụm thì được gì?**
→
- MIN: {1} | {2,3,4,5,6}
- MAX: {1,2,5} | {3,4,6}
- AVG: {1} | {2,3,4,5,6}

**Q3. Vì sao single link xử lý được cụm không elip nhưng nhạy nhiễu?**
→ Chỉ cần **một cặp điểm gần** là gộp, nên các điểm nối thành chuỗi đi theo hình dạng bất kỳ. Nhưng cũng vì thế vài điểm nhiễu làm "cầu" là đủ nối hai cụm (chaining).

**Q4. Vì sao complete link bẻ gãy cụm lớn?**
→ Nó giảm thiểu đường kính cụm gộp. Gộp cụm nhỏ với cụm lớn nguyên vẹn cho đường kính rất lớn, nên nó chọn chẻ cụm lớn, ghép một phần với cụm nhỏ.

**Q5. Vì sao group average chia cho $|C_i||C_j|$?**
→ Tổng proximity tăng theo số cặp, nên cụm lớn sẽ luôn "thắng". Lấy trung bình để chuẩn hoá (slide 89).

**Q6. Ward's method là gì, liên hệ K-means ra sao?**
→ Gộp cặp làm **tăng SSE ít nhất**, $\Delta = \frac{|A||B|}{|A|+|B|}\|c_A-c_B\|^2$. Cùng hàm mục tiêu SSE với K-means, nên là "phiên bản phân cấp của K-means"; cắt ở K cụm và lấy centroid để khởi tạo K-means.

**Q7. Tính Δ Ward khi gộp A = {0,1} với B = {3} (1D).**
→ $c_A = 0.5$, $\Delta = \frac{2\cdot1}{3}(3-0.5)^2 = \frac{2}{3}\cdot6.25 \approx 4.17$. Kiểm tra: SSE({0,1,3}) = 42/9 ≈ 4.67; trừ SSE(A) = 0.5 còn 4.17 ✓.

**Q8. Độ phức tạp của agglomerative? Giải thích.**
→ Bộ nhớ $O(N^2)$ (ma trận khoảng cách). Thời gian $O(N^3)$: N−1 bước, mỗi bước tìm/cập nhật trên ma trận $N^2$. Có thể đạt $O(N^2\log N)$ với cấu trúc dữ liệu phù hợp.

**Q9. Nêu các hạn chế của hierarchical clustering.**
→ (slide 95)
- Gộp xong không hoàn tác được (greedy).
- Không tối ưu hàm mục tiêu toàn cục.
- Nhạy nhiễu (MIN).
- Khó với cụm khác kích thước và hình lồi.
- Bẻ gãy cụm lớn (MAX).
- (bổ sung) Chi phí $O(N^2)$ bộ nhớ, $O(N^3)$ thời gian.

**Q10. Tại sao mọi linkage đều cho cùng bước gộp đầu tiên?**
→ Khi mọi cụm chỉ có 1 điểm, MIN = MAX = AVG = centroid = $d(x,y)$, còn Ward = $d^2/2$ (đơn điệu theo d). Nên cặp gần nhất là như nhau.

**Q11 (bổ sung). Centroid linkage có nhược điểm gì đặc biệt?**
→ Có thể **inversion**: lần gộp sau ở mức thấp hơn lần gộp trước (ví dụ tam giác A(0,0), B(2,0), C(1,1.8): gộp AB @2, rồi gộp C @1.8).

**Q12. So sánh hierarchical và K-means.**
→
- Hierarchical: không cần K, cho cây lồng nhau (taxonomy), tất định, nhưng chậm ($O(N^3)$) và không hoàn tác được.
- K-means: nhanh, có hàm mục tiêu SSE, nhưng cần K và phụ thuộc khởi tạo.

---

## 13. Tóm tắt cho tờ A4

**Agglomerative:** mỗi điểm 1 cụm → lặp {gộp 2 cụm gần nhất; cập nhật ma trận} → còn 1 cụm. Cắt dendrogram để có K cụm.

**Linkage** ($d$ = khoảng cách; với **similarity** thì đảo min↔max và gộp cặp sim **lớn nhất**):
- **MIN/single:** $\min_{x\in A,y\in B} d(x,y)$. ✔ hình dạng bất kỳ; ✘ nhiễu, chaining.
- **MAX/complete:** $\max d(x,y)$. ✔ ít nhạy nhiễu; ✘ bẻ gãy cụm lớn, thiên cụm cầu.
- **Group avg:** $\frac{\sum_{x\in A,y\in B} d(x,y)}{|A||B|}$. Cập nhật: $d(A\cup B,C)=\frac{|A|d(A,C)+|B|d(B,C)}{|A|+|B|}$. Dung hoà; ✔ ít nhiễu; ✘ thiên cầu. Chia trung bình vì tổng thiên vị cụm lớn.
- **Centroid:** $\|c_A-c_B\|$. ✘ có thể inversion (bổ sung).
- **Ward:** $\Delta=SSE(A\cup B)-SSE(A)-SSE(B)=\frac{|A||B|}{|A|+|B|}\|c_A-c_B\|^2$ (2 điểm: $d^2/2$). ✔ ít nhiễu; ✘ thiên cầu; "K-means phân cấp", dùng khởi tạo K-means.

**Ví dụ sim 5×5** (12=.90, 13=.10, 14=.65, 15=.20, 23=.70, 24=.60, 25=.50, 34=.40, 35=.30, 45=.80):
- Single: 12@.90, 45@.80, 123@.70, all@.65
- Complete: 12, 45, 345@.30, all@.10
- Avg: 12, 45, 1245@.4875, all@.375 (dendrogram slide 89 sai!)

**6 điểm (slide 93):** 2 bước đầu chung {3,6}, {2,5}.
- MIN: +{2,5}∪{3,6}, +4, +1
- MAX: +4, {2,5}+1, all
- AVG: +4, ∪{2,5}, +1
- Ward: +4, +1, +{2,5}

**Độ phức tạp:** bộ nhớ $O(N^2)$; thời gian $O(N^3)$ (N bước × ma trận $N^2$), có thể $O(N^2\log N)$.

**Hạn chế:**
- Gộp không hoàn tác (greedy).
- Không tối ưu hàm mục tiêu toàn cục.
- Nhạy nhiễu.
- Khó với cụm khác cỡ/hình lồi.
- Bẻ gãy cụm lớn.

**Ưu điểm (slide 69):** không cần K; cho taxonomy (sinh học, phát sinh loài).
