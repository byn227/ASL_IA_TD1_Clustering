# Chương 8 – Phân tích cụm (Cluster Analysis), phần B: K-means chi tiết (slide 43 → 60)

> Phạm vi: slide 43–60. Nội dung: chi tiết thuật toán K-means, độ đo SSE, vấn đề chọn tâm khởi tạo (initial centroids), xác suất chọn "trúng", ví dụ 10 cụm, các giải pháp, cụm rỗng (empty clusters), cập nhật tăng dần (incremental update), tiền/hậu xử lý (pre/post-processing), và **Bisecting K-means**.
> Slide 61 ("Limitations of K-means") thuộc phần tiếp theo (do người khác trình bày).
> Những gì **không có trên slide** mà mình thêm vào được đánh dấu **(bổ sung)**.

---

## 0. Nhắc lại nhanh: thuật toán K-means cơ bản (slide 42 – ngữ cảnh)

Slide 42 (ngay trước phần này) cho thuật toán gốc:

```
1: Chọn K điểm làm tâm khởi tạo (initial centroids)
2: repeat
3:    Tạo K cụm bằng cách gán mỗi điểm vào tâm gần nhất
4:    Tính lại tâm (centroid) của mỗi cụm
5: until các tâm không thay đổi nữa
```

- K-means là phương pháp **phân cụm phân hoạch (partitional clustering)**: mỗi điểm thuộc đúng 1 cụm, các cụm không lồng nhau.
- Mỗi cụm gắn với 1 **tâm (centroid)**; **K phải được cho trước**.

Toàn bộ các slide 43–60 trả lời câu hỏi: *"Thuật toán đơn giản này có những chi tiết gì, hỏng ở đâu, và sửa thế nào?"*

---

## 1. Slide 43 – K-means Clustering: Details (các chi tiết)

Slide liệt kê 6 ý:

### 1.1 "Initial centroids are often chosen randomly" – Tâm khởi tạo thường chọn ngẫu nhiên
- Thường chọn ngẫu nhiên K điểm trong dữ liệu làm tâm ban đầu.
- **Hệ quả**: *"Clusters produced vary from one run to another"* – mỗi lần chạy có thể ra kết quả khác nhau → K-means **không tất định (non-deterministic)** nếu không cố định seed.
- Ví dụ trực quan: giống như thả K viên bi lên một địa hình gồ ghề – bi rơi vào hố nào phụ thuộc vào chỗ thả.

### 1.2 "The centroid is (typically) the mean of the points in the cluster" – Tâm là trung bình
Với cụm $C_i$ gồm $m_i$ điểm:
$$c_i = \frac{1}{m_i}\sum_{x\in C_i} x$$
(trung bình từng tọa độ). Ví dụ: cụm $\{(1,1),(2,1),(1,2)\}$ → tâm $= \left(\frac{1+2+1}{3},\frac{1+1+2}{3}\right) = (1.33, 1.33)$.

- Chữ "typically" (thường là) vì với độ đo khác có thể dùng đại diện khác. **(bổ sung, theo sách Tan)**: với khoảng cách Manhattan ($L_1$) thì đại diện tối ưu là **trung vị (median)**; với Euclid bình phương hoặc cosine thì là **trung bình (mean)**.
- Lưu ý: tâm **không nhất thiết là một điểm dữ liệu thật** (khác với *medoid* trong K-medoids – bổ sung).

### 1.3 "'Closeness' is measured by Euclidean distance, cosine similarity, correlation, etc."
Mức độ "gần" có thể đo bằng:
- **Khoảng cách Euclid**: $d(x,y)=\sqrt{\sum_k (x_k-y_k)^2}$ → dữ liệu số trong không gian.
- **Độ tương tự cosine (cosine similarity)**: $\cos(x,y)=\frac{x\cdot y}{\|x\|\|y\|}$ → hay dùng cho văn bản (document vectors).
- **Hệ số tương quan (correlation)**.

Ví dụ Euclid: $d((1,1),(4,5)) = \sqrt{3^2+4^2}=5$.

### 1.4 "K-means will converge for common similarity measures mentioned above" – K-means hội tụ
- Với các độ đo thông dụng trên, thuật toán **chắc chắn dừng** sau hữu hạn bước.
- **Vì sao? (bổ sung – lập luận trực giác)**: mỗi bước (gán điểm vào tâm gần nhất, rồi tính lại tâm = trung bình) đều **không làm tăng SSE**. Số cách chia n điểm vào K cụm là hữu hạn, nên SSE không thể giảm mãi → phải dừng.
- **Nhưng**: hội tụ **tới một cực tiểu cục bộ (local optimum)**, *không đảm bảo* tối ưu toàn cục (global optimum). Đây chính là lý do các slide 44–55 tồn tại.

### 1.5 "Most of the convergence happens in the first few iterations" – Phần lớn hội tụ xảy ra ở vài vòng đầu
- Các tâm "chạy" rất nhiều ở vài vòng đầu, sau đó chỉ nhích nhẹ.
- Vì vậy điều kiện dừng thường được nới lỏng thành: **"Until relatively few points change clusters"** – dừng khi chỉ còn rất ít điểm đổi cụm (ví dụ < 1% điểm), thay vì chờ tâm đứng yên tuyệt đối → tiết kiệm thời gian.

### 1.6 Độ phức tạp: $O(n \times K \times I \times d)$
- $n$ = số điểm, $K$ = số cụm, $I$ = số vòng lặp (iterations), $d$ = số thuộc tính (attributes/chiều).
- Giải thích: mỗi vòng, với **mỗi** điểm ($n$) tính khoảng cách đến **mỗi** tâm ($K$), mỗi khoảng cách tốn $d$ phép tính → $nKd$ mỗi vòng, nhân với $I$ vòng.
- Ví dụ số: $n=10\,000$, $K=5$, $I=20$, $d=10$ → $10^4\cdot5\cdot20\cdot10 = 10^7$ phép tính → rất nhanh.
- **Phân tích sâu**: tuyến tính theo $n$ (vì $K, I, d$ thường nhỏ so với $n$) → K-means rất hiệu quả với dữ liệu lớn. **(bổ sung)** So sánh: phân cụm phân cấp (hierarchical) cơ bản cần $O(n^2)$ bộ nhớ và $O(n^3)$ (hoặc $O(n^2\log n)$) thời gian. Bộ nhớ K-means chỉ $O((n+K)d)$.

### Mã giả đầy đủ (gộp slide 42 + 43)
```
Input: tập D gồm n điểm, số cụm K
1. Chọn ngẫu nhiên K điểm của D làm tâm c_1..c_K
2. repeat
3.    for mỗi điểm x trong D:
4.        gán x vào cụm j = argmin_i dist(x, c_i)
5.    for i = 1..K:
6.        c_i = trung bình các điểm thuộc cụm i
7. until (không điểm nào đổi cụm)  hoặc (rất ít điểm đổi cụm)
Output: K cụm + K tâm
```

### Ví dụ chạy tay (hand-trace) – 6 điểm 2D, K = 2
Điểm: A(1,1), B(2,1), C(1,2), D(5,4), E(6,5), F(5,5). Tâm khởi tạo (cố tình chọn "xấu"): $c_1 = A(1,1)$, $c_2 = B(2,1)$. Dùng **bình phương khoảng cách Euclid** (so sánh bình phương cũng như so sánh khoảng cách).

**Vòng 1 – gán:**

| Điểm | $d^2$ tới $c_1(1,1)$ | $d^2$ tới $c_2(2,1)$ | Cụm |
|---|---|---|---|
| A(1,1) | 0 | 1 | 1 |
| B(2,1) | 1 | 0 | 2 |
| C(1,2) | 1 | 2 | 1 |
| D(5,4) | 25 | 18 | 2 |
| E(6,5) | 41 | 32 | 2 |
| F(5,5) | 32 | 25 | 2 |

Cập nhật tâm: $c_1 = $ mean(A,C) $= (1, 1.5)$; $c_2 =$ mean(B,D,E,F) $= (18/4, 15/4) = (4.5, 3.75)$.

**Vòng 2 – gán:**

| Điểm | $d^2$ tới $c_1(1,1.5)$ | $d^2$ tới $c_2(4.5,3.75)$ | Cụm |
|---|---|---|---|
| A | 0.25 | 19.81 | 1 |
| B | 1.25 | 13.81 | 1 ← **đổi cụm** |
| C | 0.25 | 15.31 | 1 |
| D | 22.25 | 0.31 | 2 |
| E | 37.25 | 3.81 | 2 |
| F | 28.25 | 1.81 | 2 |

Cập nhật: $c_1 = $ mean(A,B,C) $=(4/3,4/3)\approx(1.33,1.33)$; $c_2=$ mean(D,E,F) $=(16/3,14/3)\approx(5.33,4.67)$.

**Vòng 3**: gán lại → không điểm nào đổi cụm → **dừng**. Kết quả: {A,B,C} và {D,E,F}. (Ở ví dụ dễ này dù khởi tạo xấu vẫn tìm ra kết quả tốt – giống slide 45–46.)

---

## 2. Slide 44 – Two different K-means Clusterings (Hai kết quả K-means khác nhau)

Hình gồm 3 biểu đồ trên cùng một tập điểm 2D:
- **Original Points** (điểm gốc): 3 nhóm tự nhiên – một nhóm lớn, thưa ở phía trên (khoảng $x\approx0$, $y\approx2$), một nhóm nhỏ ở dưới-trái ($\approx(-1,0)$), một nhóm nhỏ ở dưới-phải ($\approx(1,0)$).
- **Optimal Clustering** (phân cụm tối ưu): K-means (K=3) tìm đúng 3 nhóm tự nhiên.
- **Sub-optimal Clustering** (phân cụm dưới tối ưu): nhóm lớn phía trên bị **chia đôi** thành 2 cụm (xanh dương + xanh lá), còn **hai nhóm nhỏ phía dưới bị gộp** thành 1 cụm (đỏ).

**Thông điệp**: cùng dữ liệu, cùng K, cùng thuật toán – chỉ khác **tâm khởi tạo** → kết quả khác hẳn. Kết quả dưới tối ưu vẫn là một điểm hội tụ hợp lệ (cực tiểu cục bộ) – K-means không "biết" mình sai.

---

## 3. Slides 45–46 – Importance of Choosing Initial Centroids (khởi tạo "may mắn")

- Slide 45: kết quả ở **Iteration 6** – 3 cụm đúng (đỏ ở trên, xanh lá dưới-trái, xanh dương dưới-phải), dấu "+" là tâm.
- Slide 46: 6 hình từ **Iteration 1 → 6** cho thấy quá trình:
  - Iteration 1: cả 3 tâm (dấu +) đều nằm ở vùng nhóm lớn phía trên (hình nhỏ, đọc gần đúng); các nhóm nhỏ phía dưới bị gán theo tâm gần nhất (xanh lá/xanh dương).
  - Iteration 2–3: hai tâm dần **trượt xuống** về phía hai nhóm nhỏ dưới (vì trung bình của cụm bị các điểm phía dưới "kéo" xuống).
  - Iteration 4–6: mỗi tâm nằm gọn trong một nhóm tự nhiên → hội tụ đúng.

**Bài học**: đôi khi tâm khởi tạo dù không "đẹp" vẫn tự điều chỉnh về đúng chỗ (*"sometimes the initial centroids will readjust themselves in the 'right' way"* – sẽ gặp lại ở slide 50).

**Trực giác (bổ sung)**: một tâm chỉ "di chuyển" được nhờ các điểm được gán cho nó. Nếu một tâm "nhìn thấy" (được gán) một phần của nhóm khác, trung bình sẽ bị kéo về phía nhóm đó → tâm bò sang. Nếu không có điểm nào kéo, tâm đứng yên.

---

## 4. Slide 47 – Evaluating K-means Clusters (Đánh giá cụm K-means): SSE

### 4.1 Định nghĩa
Độ đo phổ biến nhất là **tổng bình phương sai số – Sum of Squared Error (SSE)**:
- Với mỗi điểm, *sai số (error)* = khoảng cách tới **tâm cụm gần nhất**.
- SSE = bình phương các sai số rồi cộng lại:

$$SSE = \sum_{i=1}^{K}\sum_{x\in C_i} dist^2(m_i, x)$$

Ký hiệu:
- $K$: số cụm; $C_i$: cụm thứ $i$;
- $x$: một điểm dữ liệu thuộc cụm $C_i$;
- $m_i$: **điểm đại diện (representative point)** của cụm $C_i$;
- $dist$: thường là khoảng cách Euclid.

Slide ghi: *"can show that $m_i$ corresponds to the center (mean) of the cluster"* – có thể chứng minh $m_i$ tối ưu chính là trung bình của cụm.

### 4.2 Chứng minh "tâm = trung bình làm SSE nhỏ nhất" (slide chỉ nói "can show"; chứng minh là bổ sung)
Xét 1 cụm, 1 chiều cho gọn: tìm $c$ để $f(c)=\sum_{x\in C}(c-x)^2$ nhỏ nhất.
$$f'(c) = \sum_{x\in C} 2(c-x) = 0 \;\Rightarrow\; m\,c = \sum_{x\in C} x \;\Rightarrow\; c=\frac{1}{m}\sum_{x\in C}x$$
($f''=2m>0$ nên đây là cực tiểu.) Làm từng chiều độc lập → đúng cho nhiều chiều. ⇒ Bước "tính lại tâm = trung bình" của K-means chính là bước **giảm SSE tối ưu khi cố định phép gán**; bước "gán điểm vào tâm gần nhất" là bước **giảm SSE tối ưu khi cố định tâm**. K-means = luân phiên tối ưu 2 thứ (bổ sung).

### 4.3 Ví dụ số
Tiếp ví dụ ở mục 1: cụm 1 = {A(1,1), B(2,1), C(1,2)}, tâm $(4/3,4/3)$:
- A: $(1/3)^2+(1/3)^2 = 2/9$; B: $(2/3)^2+(1/3)^2=5/9$; C: $(1/3)^2+(2/3)^2=5/9$ → tổng $12/9 = 4/3$.

Cụm 2 = {D(5,4),E(6,5),F(5,5)}, tâm $(16/3,14/3)$: tương tự $5/9+5/9+2/9 = 4/3$.

$$SSE = 4/3 + 4/3 = 8/3 \approx 2.67$$

Nếu thay vào đó chia {A,C} | {B,D,E,F} (kết quả vòng 1) thì SSE lớn hơn nhiều: cụm {A,C} tâm (1,1.5): 0.25+0.25=0.5; cụm {B,D,E,F} tâm (4.5,3.75): 13.81+0.31+3.81+1.81=19.75 → SSE = 20.25. ⇒ SSE nhỏ hơn = phân cụm tốt hơn.

### 4.4 Cách dùng SSE (theo slide)
- *"Given two clusters, we can choose the one with the smallest error"* – giữa hai kết quả phân cụm (cùng K), chọn cái có SSE nhỏ hơn. → Cách dùng thực tế: **chạy K-means nhiều lần, giữ lần có SSE nhỏ nhất**.
- *"One easy way to reduce SSE is to increase K"* – tăng K thì SSE giảm (cực đoan: $K=n$ → mỗi điểm 1 cụm → SSE = 0).
- *"A good clustering with smaller K can have a lower SSE than a poor clustering with higher K"* – một phân cụm tốt với K nhỏ có thể có SSE thấp hơn một phân cụm tồi với K lớn. (Ví dụ cụ thể ở mục 11, Câu 6.)

### Phân tích sâu / đánh giá
- SSE đo **độ gắn kết (cohesion)** bên trong cụm: càng nhỏ → các điểm càng sát tâm.
- **Không dùng SSE để chọn K** một cách ngây thơ (vì luôn giảm khi K tăng). **(bổ sung)**: người ta vẽ SSE theo K và tìm "khuỷu tay" (*elbow method*) – chỗ mà tăng K thêm không còn giảm SSE đáng kể.
- SSE dùng **bình phương** → điểm xa (outlier) đóng góp rất lớn → SSE và K-means **nhạy với ngoại lai (outliers)**.
- SSE ưu tiên cụm dạng "cầu" (globular), kích thước tương đương → liên hệ với phần "Limitations of K-means" (slide 61+).

---

## 5. Slides 48–49 – Importance of Choosing Initial Centroids … (khởi tạo "xui")

- Slide 48: kết quả **Iteration 5** với khởi tạo khác: nhóm lớn phía trên bị chia làm 2 cụm (xanh lá ở trên, xanh dương ở dưới, mỗi phần một dấu +), còn **hai nhóm nhỏ ở dưới bị gộp** thành 1 cụm đỏ, với tâm (dấu +) nằm **ở khoảng trống giữa hai nhóm** ($\approx(0,0)$) – nơi không có điểm dữ liệu nào!
- Slide 49: Iteration 1 → 5: ngay từ đầu, 2 tâm nằm trong nhóm lớn phía trên và 1 tâm nằm giữa 2 nhóm nhỏ phía dưới (đọc gần đúng từ hình nhỏ). Qua các vòng, cấu hình gần như không đổi – các tâm chỉ nhích nhẹ rồi "kẹt".

**Vì sao kẹt?** Tâm đỏ ở giữa là trung bình của hai nhóm dưới; mỗi điểm ở nhóm dưới vẫn gần tâm đỏ hơn hai tâm phía trên → không có điểm nào đổi cụm → thuật toán dừng. Đây là **cực tiểu cục bộ** (local minimum) đúng như "Sub-optimal clustering" ở slide 44.

### Ví dụ số 1D minh họa cực tiểu cục bộ (bổ sung, cùng tinh thần slide 48)
Điểm: $\{0, 1, 10, 11, 20, 21\}$, K=3. Tối ưu rõ ràng là {0,1}, {10,11}, {20,21} với SSE $= 6\times0.25 = 1.5$.

Khởi tạo xui: $c_1=0$, $c_2=1$, $c_3=15$.
- Vòng 1: 0→$c_1$; 1→$c_2$; 10: $|10-1|=9$, $|10-15|=5$ → $c_3$; 11 → $c_3$; 20, 21 → $c_3$. Tâm mới: $c_1=0$, $c_2=1$, $c_3=(10+11+20+21)/4=15.5$.
- Vòng 2: 10: $|10-1|=9 > |10-15.5|=5.5$ → vẫn $c_3$. Không đổi → **dừng**.
- SSE $= 0 + 0 + (5.5^2+4.5^2+4.5^2+5.5^2) = 101$ ≫ 1.5.

Hai tâm "chen chúc" ở nhóm {0,1}, một tâm đứng giữa {10,11} và {20,21} – y hệt hình slide 48.

---

## 6. Slide 50 – Problems with Selecting Initial Points (Vấn đề chọn điểm khởi tạo)

### 6.1 Ý chính
Nếu có K cụm "thật" (real clusters) thì **xác suất chọn được đúng 1 tâm trong mỗi cụm là nhỏ**, đặc biệt **khi K lớn**.

Nếu các cụm có cùng kích thước $n$ (tổng cộng $Kn$ điểm):

$$P = \frac{\text{số cách chọn 1 tâm từ mỗi cụm}}{\text{số cách chọn } K \text{ tâm}} = \frac{K!\,n^K}{(Kn)^K} = \frac{K!}{K^K}$$

Giải thích từng thành phần:
- Tử số $K!\,n^K$: chọn 1 điểm trong mỗi cụm có $n$ cách → $n^K$; và vì ta chọn K tâm *có thứ tự* (tâm thứ 1, 2, …), cụm "trúng" của tâm thứ 1, 2,… có thể hoán vị theo $K!$ cách.
- Mẫu số $(Kn)^K$: mỗi tâm trong K tâm có thể là bất kỳ điểm nào trong $Kn$ điểm.
- $n$ triệt tiêu → $P$ **chỉ phụ thuộc K**.
- **(bổ sung)** Đây là công thức xấp xỉ (coi như chọn có hoàn lại, có thứ tự); khi $n$ lớn thì xấp xỉ rất tốt.

### 6.2 Ví dụ số
| K | $P=K!/K^K$ |
|---|---|
| 2 | $2/4 = 0.5$ |
| 3 | $6/27 \approx 0.222$ |
| 4 | $24/256 \approx 0.094$ |
| 5 | $120/3125 \approx 0.038$ |
| 10 | $10!/10^{10} = 3\,628\,800/10^{10} \approx 0.00036$ (slide) |

⇒ Với K=10 chỉ có ~0.036% cơ hội khởi tạo "hoàn hảo".

**(bổ sung)** Nếu chạy $R$ lần độc lập, xác suất có ít nhất 1 lần hoàn hảo $= 1-(1-P)^R$. Với K=10, để đạt 50% cần $R \approx \ln 0.5/\ln(1-0.00036)\approx 1910$ lần → đó là ý của slide 55 "probability is not on your side".

### 6.3 Hai ý cuối của slide
- *"Sometimes the initial centroids will readjust themselves in 'right' way, and sometimes they don't"* – khởi tạo không hoàn hảo **chưa chắc** cho kết quả xấu (slide 45–46 là ví dụ tự sửa được; slide 48–49 là ví dụ không sửa được).
- *"Consider an example of five pairs of clusters"* → dẫn sang ví dụ 10 cụm (slide 51–54).

---

## 7. Slides 51–54 – 10 Clusters Example (Ví dụ 10 cụm)

**Dữ liệu**: 10 nhóm tự nhiên xếp thành **5 cặp** theo trục x ($x\approx 2, 6, 10, 14, 18$); mỗi cặp gồm 1 nhóm trên ($y\approx 1.5$) và 1 nhóm dưới ($y\approx -1$). Hai nhóm trong cùng cặp khá gần nhau theo chiều dọc; các cặp cách nhau theo chiều ngang. K = 10.

### 7.1 Slides 51–52: "Starting with two initial centroids in one cluster of each pair of clusters"
- Khởi tạo: **mỗi cặp nhận đúng 2 tâm**, nhưng cả 2 tâm đều nằm trong **cùng một nhóm** của cặp (ví dụ cả hai ở nhóm trên).
- Iteration 1 → 4 (slide 52): trong mỗi cặp, một tâm "trượt" sang nhóm còn lại của cặp (vì nhóm kia gần và các điểm của nó kéo tâm về). Đến **Iteration 4** (slide 51) → mỗi nhóm có đúng 1 tâm → **kết quả đúng 10 cụm**.
- Bài học: khởi tạo *không* hoàn hảo (không phải 1 tâm/nhóm) nhưng **vẫn tự sửa được**, vì số tâm trong mỗi cặp là đúng (2) và hai nhóm trong cặp đủ gần để tâm di chuyển.

### 7.2 Slides 53–54: "Starting with some pairs of clusters having three initial centroids, while other have only one"
- Khởi tạo: một số cặp nhận **3 tâm**, một số cặp chỉ nhận **1 tâm** (tổng vẫn 10).
- Kết quả Iteration 4 (slide 53, đọc từ hình): cặp ở $x\approx6$ chỉ có 1 tâm → **hai nhóm trên/dưới bị gộp thành 1 cụm** (màu xanh dương, tâm nằm ở giữa khoảng trống, $y\approx0$); cặp ở $x\approx18$ có thừa tâm → **một nhóm tự nhiên bị chia đôi** (nhóm trên có 2 dấu +, hai màu). Các cặp còn lại đúng.
- Qua Iteration 1→4 (slide 54) cấu hình gần như không đổi → **kẹt ở cực tiểu cục bộ**.
- **Vì sao không tự sửa?** Tâm dư ở cặp x=18 muốn sang cặp x=6 thì phải "đi qua" các cặp ở giữa, nhưng các điểm của cặp giữa luôn gần tâm riêng của chúng hơn → không có điểm nào kéo tâm dư đi xa. Tâm K-means chỉ di chuyển **cục bộ**.

**Tổng kết slides 50–54**: điều quan trọng không phải "mỗi nhóm có đúng 1 tâm", mà là số tâm phân bố đúng giữa các **vùng tách biệt xa nhau**; tâm có thể tự điều chỉnh trong vùng nhưng **không di chuyển được giữa các vùng xa**.

---

## 8. Slide 55 – Solutions to Initial Centroids Problem (Giải pháp cho vấn đề tâm khởi tạo)

| Giải pháp (slide) | Ý nghĩa | Ghi chú / đánh giá |
|---|---|---|
| **Multiple runs** (chạy nhiều lần) | Chạy K-means nhiều lần với khởi tạo ngẫu nhiên khác nhau, giữ kết quả SSE nhỏ nhất | *"Helps, but probability is not on your side"* – có ích nhưng khi K lớn, xác suất gặp khởi tạo tốt rất nhỏ (xem slide 50: K=10 → 0.036%/lần) |
| **Sample + hierarchical clustering** | Lấy mẫu nhỏ dữ liệu, chạy phân cụm phân cấp (hierarchical clustering) trên mẫu để có K cụm, lấy tâm các cụm đó làm tâm khởi tạo cho K-means | (bổ sung) Hiệu quả khi mẫu nhỏ (vài trăm–vài nghìn điểm, vì hierarchical tốn $O(n^2)$) và K nhỏ so với kích thước mẫu |
| **Select more than k initial centroids, then select among them** | Chọn nhiều hơn K tâm ứng viên, rồi chọn ra K tâm **cách xa nhau nhất (most widely separated)** | (bổ sung) Ví dụ thủ tục "farthest-first": tâm 1 ngẫu nhiên (hoặc tâm toàn dữ liệu), mỗi tâm tiếp theo là điểm xa nhất với các tâm đã chọn. Nhược: dễ chọn trúng **ngoại lai**; tốn chi phí → thường làm trên mẫu. Ý tưởng gần với **K-means++** (bổ sung, không có trên slide) |
| **Postprocessing** (hậu xử lý) | Sau khi chạy, sửa kết quả: tách/gộp/xóa cụm | Xem slide 58 |
| **Bisecting K-means** | Biến thể chia đôi dần | *"Not as susceptible to initialization issues"* – ít nhạy với khởi tạo hơn (xem slide 59–60) |

---

## 9. Slide 56 – Handling Empty Clusters (Xử lý cụm rỗng)

### 9.1 Vấn đề
*"Basic K-means algorithm can yield empty clusters"* – có thể xảy ra tình huống **một tâm không được gán điểm nào** → không tính được trung bình (chia cho 0) → cụm rỗng, và ta mất đi 1 cụm.

Ví dụ: điểm $\{1,2,3,10,11,15\}$, K=3, tâm khởi tạo $c_1=2$, $c_2=11$, $c_3=50$ (tâm 3 chọn ngẫu nhiên trong không gian, ở xa). Mọi điểm đều gần $c_1$ hoặc $c_2$ hơn → cụm 3 **rỗng**. (Cũng có thể xảy ra ở các vòng sau khi một tâm bị các tâm khác "giành hết" điểm.)

### 9.2 Các chiến lược (slide)
1. **Chọn điểm đóng góp nhiều nhất vào SSE** (*the point that contributes most to SSE*) làm tâm thay thế – tức điểm **xa tâm của nó nhất**.
2. **Chọn một điểm từ cụm có SSE cao nhất** (*a point from the cluster with the highest SSE*) – việc này thường sẽ **tách** cụm "lỏng lẻo" đó, giảm SSE tổng.
3. **Nhiều cụm rỗng** → lặp lại thủ tục trên nhiều lần.

### 9.3 Ví dụ số tiếp theo
Với $c_1=2$, $c_2=11$: cụm 1 = {1,2,3} → tâm 2; cụm 2 = {10,11,15} → tâm 12.
- Đóng góp SSE từng điểm: 1→1, 2→0, 3→1, 10→4, 11→1, **15→9** (lớn nhất).
- SSE theo cụm: cụm 1 = 2, **cụm 2 = 14** (lớn nhất).
- Cả hai chiến lược đều dẫn tới chọn **15** làm tâm mới $c_3=15$.
- Vòng tiếp: tâm (2, 12, 15) → {1,2,3}, {10,11}, {15}; tâm (2, 10.5, 15); SSE $= 2 + 0.5 + 0 = 2.5$ (giảm mạnh từ 16).

**Phân tích**: thay vì "lãng phí" một tâm, ta đặt nó vào chỗ đang "tệ nhất" → vừa sửa lỗi cụm rỗng, vừa giảm SSE.

---

## 10. Slide 57 – Updating Centers Incrementally (Cập nhật tâm tăng dần)

### 10.1 Hai cách cập nhật
- **Cơ bản (batch)**: tâm chỉ được cập nhật **sau khi tất cả** các điểm đã được gán.
- **Tăng dần (incremental)**: cập nhật tâm **ngay sau mỗi lần gán** một điểm.

### 10.2 Đặc điểm của cách tăng dần (slide)
- **"Each assignment updates zero or two centroids"** – mỗi lần gán cập nhật 0 hoặc 2 tâm: nếu điểm *vẫn ở cụm cũ* → 0 tâm thay đổi; nếu điểm *chuyển cụm* → 2 tâm thay đổi (cụm cũ mất điểm, cụm mới thêm điểm).
- **"More expensive"** – tốn kém hơn (phải tính lại tâm nhiều lần).
- **"Introduces an order dependency"** – kết quả phụ thuộc **thứ tự** xét các điểm.
- **"Never get an empty cluster"** – không bao giờ có cụm rỗng. (Giải thích – bổ sung: một cụm chỉ còn 1 điểm thì tâm của nó trùng đúng điểm đó (khoảng cách 0) → điểm đó luôn ở lại → cụm không bao giờ về 0. Ngoài ra khi khởi tạo, mỗi cụm bắt đầu với ít nhất 1 điểm.)
- **"Can use 'weights' to change the impact"** – có thể dùng trọng số để điều chỉnh mức ảnh hưởng của mỗi điểm lên tâm.

### 10.3 Công thức cập nhật (bổ sung)
Cụm có $m$ điểm, tâm $c$:
- Thêm điểm $x$: $c_{new} = c + \dfrac{x - c}{m+1}$
- Bớt điểm $x$: $c_{new} = c - \dfrac{x - c}{m-1}$ (với $m>1$)
- Dạng có trọng số (weights / learning rate $\alpha$): $c_{new} = c + \alpha(x-c)$ – $\alpha$ lớn → điểm mới ảnh hưởng mạnh.

**Ví dụ số**: cụm A = {1, 2, 3} (tâm 2, m=3), cụm B = {8, 9, 4} (tâm 7, m=3). Xét điểm 4: $|4-2|=2 < |4-7|=3$ → chuyển 4 từ B sang A, cập nhật ngay **2 tâm**:
- $c_A = 2 + (4-2)/4 = 2.5$ (kiểm tra: mean{1,2,3,4} = 2.5 ✓)
- $c_B = 7 - (4-7)/2 = 8.5$ (kiểm tra: mean{8,9} = 8.5 ✓)

Điểm tiếp theo được xét sẽ so với tâm *mới* (2.5 và 8.5) – đây là nguồn gốc của "phụ thuộc thứ tự".

### Phân tích sâu
- Batch: đơn giản, không phụ thuộc thứ tự, nhưng có thể gặp cụm rỗng.
- Incremental: hội tụ "mượt" hơn từng bước, phù hợp **dữ liệu dạng luồng (streaming / online)** (bổ sung), nhưng tốn và phụ thuộc thứ tự.

---

## 11. Slide 58 – Pre-processing and Post-processing (Tiền xử lý và hậu xử lý)

### 11.1 Tiền xử lý (Pre-processing)
- **Normalize the data (chuẩn hóa dữ liệu)**: khoảng cách Euclid phụ thuộc thang đo. Ví dụ: thuộc tính tuổi (20–60) và thu nhập (10 000–100 000 €) → khoảng cách gần như chỉ do thu nhập quyết định. Sau chuẩn hóa (vd. z-score $x'=(x-\mu)/\sigma$ hoặc min-max $x'=(x-\min)/(\max-\min)$ – bổ sung) các thuộc tính có ảnh hưởng ngang nhau.
  - Ví dụ: A(25 tuổi, 30 000), B(60 tuổi, 31 000): $d \approx 1000.6$ → gần như bỏ qua chênh lệch 35 tuổi.
- **Eliminate outliers (loại ngoại lai)**: vì SSE dùng bình phương, một outlier có thể kéo lệch tâm hoặc chiếm hẳn 1 cụm riêng. Ví dụ: {1,2,3,100}, tâm = 26.5 → tâm không đại diện cho ai cả.

### 11.2 Hậu xử lý (Post-processing)
- **Eliminate small clusters that may represent outliers** – xóa các cụm rất nhỏ (có thể là ngoại lai).
- **Split 'loose' clusters** – tách các cụm "lỏng lẻo", tức cụm có **SSE tương đối cao**.
- **Merge clusters that are 'close' and that have relatively low SSE** – gộp các cụm **gần nhau** và có **SSE tương đối thấp**.
- **Can use these steps during the clustering process** – có thể áp dụng các bước này ngay **trong** quá trình phân cụm → ví dụ thuật toán **ISODATA** (biến thể K-means tự tách/gộp cụm, nên K có thể thay đổi – bổ sung).

**(bổ sung, theo sách Tan)**: nguyên tắc là cân bằng giữa SSE và số cụm: tách cụm làm tăng K nhưng giảm SSE; gộp cụm giảm K nhưng tăng SSE – ta chọn tách cụm có SSE lớn nhất và gộp hai cụm mà việc gộp làm SSE tăng ít nhất.

---

## 12. Slide 59 – Bisecting K-means (K-means chia đôi)

### 12.1 Ý tưởng
*"Variant of K-means that can produce a partitional or a hierarchical clustering"* – biến thể của K-means, có thể cho kết quả **phân hoạch (partitional)** hoặc **phân cấp (hierarchical)**.

Trực giác: thay vì đặt K tâm cùng lúc (rất dễ đặt sai, xem slide 50), ta **chỉ chia đôi (bisect)** – mỗi lần chỉ cần đặt **2 tâm** (K=2 → xác suất "trúng" $2!/2^2 = 0.5$, lại thử nhiều lần) – rồi lặp lại cho đến khi đủ K cụm. Giống như cắt một chiếc bánh: mỗi lần chỉ cắt đôi một miếng.

### 12.2 Thuật toán (đúng như slide)
```
1: Khởi tạo danh sách cụm chỉ gồm 1 cụm chứa TẤT CẢ các điểm
2: repeat
3:    Chọn một cụm từ danh sách cụm (và lấy nó ra khỏi danh sách)
4:    for i = 1 to number_of_iterations do
5:        Chia đôi cụm đã chọn bằng K-means cơ bản (K = 2)
6:    end for
7:    Thêm vào danh sách 2 cụm của lần chia đôi có SSE thấp nhất
8: until danh sách có đủ K cụm
```
Chú ý quan trọng:
- **Dòng 4: `number_of_iterations` = số LẦN THỬ chia đôi** (mỗi lần với khởi tạo ngẫu nhiên khác) – *không phải* số vòng lặp bên trong K-means. Đây là "multiple runs" áp dụng cho bài toán K=2.
- **Dòng 3: chọn cụm nào?** Slide chỉ ghi "select a cluster". **(bổ sung, theo sách Tan)**: thường chọn **cụm lớn nhất (largest size)**, hoặc **cụm có SSE lớn nhất**, hoặc kết hợp.
- **(bổ sung)** Có thể dùng các tâm cuối cùng của bisecting K-means làm **tâm khởi tạo cho K-means cơ bản** để tinh chỉnh (vì kết quả bisecting không nhất thiết là cực tiểu cục bộ của SSE toàn cục).

### 12.3 Ví dụ chạy tay – 1D, 6 điểm, K = 3
Dữ liệu: $\{1, 2, 3, 8, 9, 20\}$. Quy tắc chọn cụm: SSE lớn nhất. `number_of_iterations` = 2.

**Bước 1** – Danh sách = { {1,2,3,8,9,20} }. Chọn cụm duy nhất, thử chia đôi 2 lần:
- *Thử 1*: tâm khởi tạo 1 và 20.
  - Gán: 1,2,3,8,9 → tâm 1 (vd. 9: $|9-1|=8 < |9-20|=11$); 20 → tâm 20. Tâm mới: $43-20=23$, $23/5=4.6$ và 20.
  - Gán lại: 8: $|8-4.6|=3.4 < 12$, 9: $4.4<11$ → không đổi. Kết quả {1,2,3,8,9} | {20}.
  - SSE $= (3.6^2+2.6^2+1.6^2+3.4^2+4.4^2) + 0 = 12.96+6.76+2.56+11.56+19.36 = 53.2$.
- *Thử 2*: tâm khởi tạo 1 và 9.
  - Gán: 1,2,3 → tâm 1 (3: 2 < 6); 8, 9, 20 → tâm 9. Tâm mới: 2 và $37/3 \approx 12.33$.
  - Gán lại: 8: $|8-2|=6 > |8-12.33|=4.33$ → vẫn cụm 2. Ổn định: {1,2,3} | {8,9,20}.
  - SSE $= (1+0+1) + (4.33^2+3.33^2+7.67^2) = 2 + (18.78+11.11+58.78) = 2+88.67 = 90.67$.
- Chọn lần thử có SSE thấp nhất → **Thử 1** (53.2). Danh sách = { {1,2,3,8,9} (SSE 53.2), {20} (SSE 0) }. Mới có 2 cụm < 3 → lặp tiếp.

**Bước 2** – Chọn cụm có SSE lớn nhất: {1,2,3,8,9}. Chia đôi (vd. tâm khởi tạo 1 và 9): {1,2,3} (tâm 2) | {8,9} (tâm 8.5) → SSE $= 2 + 0.5 = 2.5$ (giả sử đây là lần thử tốt nhất).

Danh sách = { {1,2,3}, {8,9}, {20} } → đủ K=3 → **dừng**. SSE tổng = $2 + 0.5 + 0 = 2.5$.

**So sánh với K-means cơ bản khởi tạo xui** (tâm 1, 2, 3 trên cùng dữ liệu):
- Vòng 1: {1}, {2}, {3,8,9,20} → tâm 1, 2, 10.
- Vòng 2: 3: $|3-2|=1 < 7$ → cụm 2; 8: $|8-2|=6 > 2$ → cụm 3 → {1}, {2,3}, {8,9,20} → tâm 1, 2.5, 12.33.
- Vòng 3: 8: $5.5 > 4.33$ → không đổi → dừng. SSE $= 0 + 0.5 + 88.67 = 89.17$.

⇒ Bisecting K-means: **2.5**; K-means khởi tạo xui: **89.17**. Minh họa "not as susceptible to initialization issues".

**Cây phân cấp tạo ra** (vì sao gọi là "hierarchical"):
```
          {1,2,3,8,9,20}
           /          \
   {1,2,3,8,9}        {20}
     /      \
 {1,2,3}   {8,9}
```
Ghi lại thứ tự chia đôi → ta có một **cây phân cụm (dendrogram) chia tách từ trên xuống (divisive)**; cắt cây ở mức nào sẽ được phân hoạch tương ứng.

### Phân tích sâu / đánh giá
- **Ưu điểm**: ít nhạy với khởi tạo (mỗi lần chỉ cần đặt 2 tâm; có nhiều lần thử); cho cả kết quả phân cấp; hiệu quả (mỗi lần chia chỉ chạy K-means trên **một** cụm, và các cụm càng ngày càng nhỏ).
- **Nhược điểm**: vẫn kế thừa các giới hạn của K-means (cụm khác kích thước, mật độ, hình dạng không cầu; outliers – slide 61+); một lần chia sai **không được sửa lại** ở các bước sau (quyết định tham lam – greedy, bổ sung); vẫn cần biết K (hoặc quyết định điểm dừng).
- **Liên hệ**: là một dạng **phân cụm phân cấp chia tách (divisive hierarchical clustering)**, ngược với phân cụm phân cấp gộp (agglomerative) sẽ học ở phần sau.

---

## 13. Slide 60 – Bisecting K-means Example

Hình "Iteration 10" trên cùng bộ dữ liệu **10 cụm** (5 cặp) ở slides 51–54: bisecting K-means tìm ra **đúng cả 10 nhóm tự nhiên**, mỗi nhóm một màu và một dấu "+" ở giữa. (Mình hiểu "Iteration 10" là trạng thái sau khi đã tách đủ để có 10 cụm; hình không ghi rõ thêm.)

**So sánh với slides 53–54**: K-means cơ bản với khởi tạo xui thì gộp nhầm một cặp và tách đôi một nhóm; bisecting K-means thì không gặp vấn đề này vì nó chia dần: đầu tiên tách các vùng lớn, xa nhau (ví dụ tách các cặp), rồi mới tách các nhóm nhỏ bên trong – tâm không cần "di chuyển xa" giữa các vùng.

---

## 14. Dễ nhầm lẫn

1. **"K-means hội tụ" ≠ "K-means tìm nghiệm tối ưu"**: luôn hội tụ, nhưng chỉ tới **cực tiểu cục bộ** (slide 44, 48, 53).
2. **SSE dùng khoảng cách BÌNH PHƯƠNG** tới tâm cụm của điểm (không phải khoảng cách thường, không phải tới tâm toàn cục). Hay quên bình phương khi tính tay.
3. **So sánh SSE chỉ có ý nghĩa với cùng K**. SSE luôn giảm khi K tăng (K=n → SSE=0), nên SSE thấp hơn với K lớn hơn không chứng minh kết quả tốt hơn.
4. **Tâm (centroid) ≠ điểm dữ liệu**: tâm là trung bình, có thể nằm ở khoảng trống không có điểm nào (slide 48: tâm đỏ nằm giữa hai nhóm). Medoid mới là điểm thật (bổ sung).
5. **Trong $O(n K I d)$, $I$ là số vòng lặp của một lần chạy**, không phải số lần chạy lại (multiple runs). Nếu chạy R lần thì nhân thêm R.
6. **Công thức $P = K!/K^K$ không phụ thuộc $n$** ($n$ triệt tiêu) và là xác suất **mỗi cụm thật có đúng 1 tâm**, không phải xác suất K-means ra kết quả đúng (vì khởi tạo không hoàn hảo vẫn có thể tự sửa – slides 51–52).
7. **Bisecting K-means – dòng 4 "number_of_iterations"** là số lần thử chia đôi (với khởi tạo khác nhau), giữ lần có SSE thấp nhất – không phải số vòng lặp của K-means 2 cụm.
8. **Bisecting K-means không chia tất cả các cụm mỗi bước**: mỗi bước chỉ chọn **một** cụm để chia → mỗi bước số cụm tăng đúng 1.
9. **Incremental update: "zero or two centroids"** – không phải "một tâm". Điểm đổi cụm → 2 tâm thay đổi.
10. **Cụm rỗng là vấn đề của K-means batch**; với cập nhật tăng dần thì **không bao giờ** có cụm rỗng.
11. **Hậu xử lý: tách cụm SSE CAO, gộp cụm GẦN và SSE THẤP** – dễ nhớ ngược.
12. "Most widely separated" (chọn tâm xa nhau nhất) có rủi ro chọn trúng **outlier**.

---

## 15. Câu hỏi có thể ra thi (kèm lời giải ngắn)

**Câu 1.** Cho các điểm 1D $\{2, 4, 10, 12, 3, 20, 30, 11, 25\}$, K=2, tâm khởi tạo $c_1=2$, $c_2=4$. Chạy K-means đến hội tụ, tính SSE.
*Giải*:
- V1: 2→$c_1$; 3: $|3-2|=1=|3-4|$ → hòa, quy ước gán tâm có chỉ số nhỏ → $c_1$; 4,10,11,12,20,25,30 → $c_2$. Tâm: $c_1=2.5$, $c_2=(4+10+11+12+20+25+30)/7=112/7=16$.
- V2: 2,3→$c_1$; 4: $1.5 < 12$ → $c_1$; 10: $7.5 > 6$ → $c_2$; còn lại $c_2$. Tâm: $c_1=3$, $c_2=(10+11+12+20+25+30)/6=108/6=18$.
- V3: 10: $|10-3|=7 < |10-18|=8$ → **$c_1$**; 11: $|11-3|=8 > |11-18|=7$ → $c_2$; 12 → $c_2$. Tâm: $c_1=(2+3+4+10)/4=4.75$, $c_2=(11+12+20+25+30)/5=98/5=19.6$.
- V4: 10: $5.25 < 9.6$ → $c_1$; 11: $6.25 < 8.6$ → **$c_1$**; 12: $7.25 < 7.6$ → **$c_1$**; 20: $c_2$. Tâm: $c_1=(2+3+4+10+11+12)/6=42/6=7$, $c_2=(20+25+30)/3=25$.
- V5: 12: $5 < 13$ → $c_1$; 20: $13 > 5$ → $c_2$. Không đổi → dừng.
- Cụm {2,3,4,10,11,12} (tâm 7), {20,25,30} (tâm 25). SSE $= (25+16+9+9+16+25) + (25+0+25) = 100 + 50 = 150$.
- (Lưu ý cách xử lý hòa – nên nêu rõ quy ước trong bài thi.)

**Câu 2.** Chứng minh rằng với cụm cố định, điểm đại diện làm cực tiểu SSE là trung bình.
*Giải*: xem mục 4.2: đạo hàm $\sum 2(c-x)=0 \Rightarrow c=\bar x$.

**Câu 3.** Có 4 cụm thật cùng kích thước. Xác suất khởi tạo ngẫu nhiên cho đúng 1 tâm/cụm là bao nhiêu? Với 10 cụm?
*Giải*: $4!/4^4 = 24/256 \approx 0.094$; $10!/10^{10}\approx 0.00036$.

**Câu 4.** Độ phức tạp của K-means? Vì sao K-means phù hợp dữ liệu lớn?
*Giải*: $O(nKId)$, tuyến tính theo $n$; bộ nhớ $O((n+K)d)$ (bổ sung). Hierarchical cơ bản $O(n^2)$ bộ nhớ, $O(n^3)$ thời gian.

**Câu 5.** Nêu các giải pháp cho vấn đề chọn tâm khởi tạo.
*Giải*: (1) chạy nhiều lần, giữ SSE nhỏ nhất; (2) lấy mẫu + phân cụm phân cấp để có tâm; (3) chọn > K tâm rồi lấy K tâm xa nhau nhất; (4) hậu xử lý; (5) bisecting K-means.

**Câu 6.** "Giảm SSE bằng cách tăng K" – đúng không? SSE có dùng để chọn K được không?
*Giải*: Đúng là SSE (tối ưu) giảm khi K tăng, đến 0 khi K=n → không thể chọn K bằng cách tối thiểu SSE. Nhưng một phân cụm tốt với K nhỏ có thể có SSE thấp hơn phân cụm tồi với K lớn. Ví dụ dữ liệu $\{1,2,3,8,9,20\}$: K=2 tốt ({1,2,3,8,9}|{20}) có SSE 53.2 < K=3 tồi ({1}|{2,3}|{8,9,20}) có SSE 89.17.

**Câu 7.** Cụm rỗng là gì, khi nào xảy ra, xử lý thế nào? (Áp dụng số ở mục 9.3.)
*Giải*: tâm không nhận điểm nào; xử lý: thay tâm bằng điểm đóng góp SSE lớn nhất, hoặc một điểm từ cụm có SSE cao nhất; lặp lại nếu nhiều cụm rỗng.

**Câu 8.** So sánh cập nhật batch và incremental.
*Giải*: incremental cập nhật sau mỗi phép gán (0 hoặc 2 tâm), tốn hơn, phụ thuộc thứ tự, không có cụm rỗng, có thể dùng trọng số. Batch cập nhật sau khi gán hết.

**Câu 9.** Cụm A = {1,2,3,5} (tâm 2.75). Điểm 5 chuyển sang cụm B = {7,9} (tâm 8). Tính tâm mới bằng công thức tăng dần.
*Giải*: $c_A = 2.75 - (5-2.75)/3 = 2.75 - 0.75 = 2$ ✓ (mean{1,2,3}); $c_B = 8 + (5-8)/3 = 7$ ✓ (mean{5,7,9}).

**Câu 10.** Viết thuật toán bisecting K-means và chạy tay trên dữ liệu nhỏ; giải thích vì sao ít nhạy với khởi tạo và vì sao có thể cho kết quả phân cấp.
*Giải*: xem mục 12. Ít nhạy vì mỗi lần chỉ chọn 2 tâm (xác suất trúng ~0.5) và thử nhiều lần giữ SSE nhỏ nhất; phân cấp vì chuỗi các lần chia đôi tạo thành cây.

**Câu 11.** Vì sao cần chuẩn hóa dữ liệu trước K-means? Vì sao nên loại outlier?
*Giải*: khoảng cách Euclid phụ thuộc thang đo → thuộc tính có thang lớn lấn át; SSE bình phương → outlier kéo lệch tâm/chiếm cụm.

**Câu 12.** Giải thích hình slide 53: tại sao K-means không tự sửa được khi một cặp có 3 tâm và cặp khác có 1 tâm?
*Giải*: tâm chỉ di chuyển nhờ điểm được gán; tâm dư không "thấy" được cặp xa vì các điểm ở đó luôn gần tâm khác hơn → kẹt ở cực tiểu cục bộ: một cặp bị gộp, một nhóm bị tách.

---

## 16. Tóm tắt cho tờ A4

**K-means (slide 42–43)**
- Chọn K tâm (ngẫu nhiên) → lặp {gán điểm vào tâm gần nhất; tâm = mean cụm} → đến khi tâm không đổi / ít điểm đổi cụm.
- Đo gần: Euclid, cosine, correlation. Luôn hội tụ, phần lớn ở vài vòng đầu, nhưng chỉ **cực tiểu cục bộ**; kết quả thay đổi theo lần chạy.
- Phức tạp $O(n\cdot K\cdot I\cdot d)$ (n điểm, K cụm, I vòng, d thuộc tính).

**SSE (slide 47)**: $SSE=\sum_{i=1}^K\sum_{x\in C_i} dist^2(m_i,x)$; $m_i$ tối ưu = mean ($\partial/\partial c: \sum 2(c-x)=0$). Chọn kết quả có SSE nhỏ (cùng K). Tăng K → SSE giảm (K=n → 0); K nhỏ tốt có thể SSE < K lớn tồi.

**Khởi tạo (slide 44–54)**: $P=\dfrac{K!\,n^K}{(Kn)^K}=\dfrac{K!}{K^K}$; K=2: 0.5, K=3: 0.22, K=4: 0.094, K=10: 0.00036. Khởi tạo xấu đôi khi tự sửa (tâm dịch chuyển cục bộ), đôi khi kẹt (gộp 2 nhóm + tách 1 nhóm; tâm không di chuyển giữa vùng xa).

**Giải pháp (slide 55)**: nhiều lần chạy (xác suất thấp); mẫu + hierarchical; chọn > K tâm rồi lấy K tâm xa nhau nhất; hậu xử lý; bisecting K-means.

**Cụm rỗng (slide 56)**: thay bằng điểm đóng góp SSE lớn nhất, hoặc điểm từ cụm SSE cao nhất; lặp nếu nhiều cụm rỗng.

**Incremental (slide 57)**: cập nhật sau mỗi gán → 0 hoặc 2 tâm đổi; tốn hơn; phụ thuộc thứ tự; không cụm rỗng; có trọng số. Thêm: $c+\frac{x-c}{m+1}$; bớt: $c-\frac{x-c}{m-1}$.

**Pre/Post (slide 58)**: Pre: chuẩn hóa, loại outliers. Post: xóa cụm nhỏ (outliers), tách cụm SSE cao (loose), gộp cụm gần + SSE thấp; làm trong lúc chạy → ISODATA.

**Bisecting K-means (slide 59–60)**:
1. List = {toàn bộ dữ liệu}
2. repeat: chọn 1 cụm (lớn nhất / SSE lớn nhất); thử chia đôi bằng 2-means `number_of_iterations` lần; thêm cặp có SSE thấp nhất vào list
3. until list có K cụm.
→ cho phân hoạch hoặc phân cấp (cây chia đôi); ít nhạy khởi tạo; có thể dùng tâm cuối làm init cho K-means (bổ sung).
