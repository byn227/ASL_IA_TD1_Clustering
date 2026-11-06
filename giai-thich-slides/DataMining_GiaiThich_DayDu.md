# Data Mining — Tổng quan & lộ trình ôn tập (slides-dm.pdf, 176 trang)

> Tài liệu giải thích bằng tiếng Việt cho cours Data Mining (R. Ciucanu, INSA CVL), dựa trên sách Tan–Steinbach–Kumar *Introduction to Data Mining* (2006).
> Thuật ngữ gốc tiếng Anh/Pháp được giữ trong ngoặc. Mọi kiến thức **ngoài slide** đều được đánh dấu **(bổ sung)**.

## 1. Cách dùng bộ tài liệu này

| File | Nội dung | Slide |
|---|---|---|
| [01_intro.md](01_intro.md) | Ch1 – Data mining là gì, KDD, các nhiệm vụ (tasks), thách thức | 1–24 |
| [02_cluster_a.md](02_cluster_a.md) | Ch8 – Định nghĩa clustering, các kiểu phân cụm, 6 loại cụm, K-means cơ bản | 25–42 |
| [03_cluster_b.md](03_cluster_b.md) | Ch8 – K-means chi tiết: SSE, khởi tạo, cụm rỗng, cập nhật tăng dần, bisecting K-means | 43–60 |
| [04_cluster_c.md](04_cluster_c.md) | Ch8 – Hạn chế K-means, hierarchical clustering, MIN/MAX, bài tập tay ma trận 5×5 | 61–78 |
| [05_cluster_d.md](05_cluster_d.md) | Ch8 – Group average, Ward, so sánh linkage, độ phức tạp, hạn chế | 79–95 |
| [06_association.md](06_association.md) | Ch6 – Support, confidence, Apriori (chạy tay đầy đủ), maximal/closed itemset, sinh luật | 96–121 |
| [07_classif_a.md](07_classif_a.md) | Ch4 – Phân lớp, cây quyết định, Hunt, điều kiện chia, bài tập GINI/Entropy/IG | 122–148 |
| [08_classif_b.md](08_classif_b.md) | Ch4 – Độ đo tạp chất, chia thuộc tính liên tục, overfitting, Occam, MDL, pruning | 149–176 |

Mỗi file đều có cấu trúc giống nhau: giải thích theo thứ tự slide, rồi đến **Phân tích sâu / đánh giá**, **Dễ nhầm lẫn**, **Câu hỏi có thể ra thi** (kèm lời giải) và **Tóm tắt cho tờ A4**.

**Gợi ý thứ tự đọc:** đọc file này trước → 01 → 02 → 03 → 04 → 05 (đủ cho TD1 Clustering) → 06 → 07 → 08. Trước kỳ thi, tự làm lại các bài "Câu hỏi có thể ra thi" mà **không nhìn lời giải**.

---

## 2. Bức tranh lớn: 4 chương nối với nhau thế nào?

```
                        DATA MINING (Ch1)
          "Tự động tìm mẫu (pattern) hữu ích, chưa biết, trong dữ liệu lớn"
                               │
          ┌────────────────────┴─────────────────────┐
   MÔ TẢ (descriptive)                          DỰ ĐOÁN (predictive)
   không có nhãn — unsupervised                 có nhãn (class) — supervised
          │                                          │
   ┌──────┴───────────┐                       Classification (Ch4)
 Clustering (Ch8)   Association (Ch6)          └─ Cây quyết định (decision tree)
 "nhóm các ĐỐI       "tìm các MỤC (item)          GINI / Entropy / Error
  TƯỢNG giống nhau"   hay đi cùng nhau"           Overfitting & pruning
 ├─ K-means           ├─ support, confidence
 ├─ Bisecting K-means ├─ Apriori
 └─ Hierarchical      └─ maximal / closed
    (MIN/MAX/AVG/Ward)
```

**Một câu cho mỗi chương:**
- **Clustering**: nhóm các *dòng* (đối tượng) giống nhau, *không cần nhãn*. Câu hỏi trung tâm: "giống nhau" đo bằng gì, và cụm "tốt" là gì?
- **Association**: tìm các *cột* (item) hay xuất hiện cùng nhau trong các giao dịch. Câu hỏi trung tâm: làm sao tránh phải xét $2^d$ tập con → **nguyên lý Apriori**.
- **Classification**: học từ dữ liệu *có nhãn* một hàm "thuộc tính → lớp", rồi áp dụng cho dữ liệu mới. Câu hỏi trung tâm: chọn phép chia nào, và khi nào dừng để không **overfitting**.

### Sợi chỉ chung xuyên suốt môn học (tư duy sâu)

1. **Không gian tìm kiếm khổng lồ → dùng chiến lược tham lam (greedy) hoặc cắt tỉa (pruning).**
   - K-means: tìm phân hoạch tối ưu SSE là NP-hard → lặp tham lam, chỉ đạt **cực tiểu cục bộ**.
   - Hierarchical: mỗi bước gộp cặp gần nhất, **không quay lui**.
   - Apriori: $2^d$ itemset → cắt tỉa nhờ tính **anti-monotone** của support.
   - Cây quyết định: số cây có thể là vô hạn → Hunt chọn phép chia tốt nhất **tại chỗ**, không quay lui.
   → Hiểu được ý này là hiểu vì sao mọi thuật toán trong môn đều "nhanh nhưng không đảm bảo tối ưu toàn cục" (trừ Apriori: Apriori **chính xác**, cắt tỉa không làm mất kết quả).

2. **Hàm mục tiêu quyết định kết quả.**
   - SSE thích các cụm tròn, kích thước đều → đó là lý do K-means thất bại với cụm khác cỡ, khác mật độ, không lồi.
   - MIN / MAX / AVG / Ward là 4 định nghĩa khác nhau của "khoảng cách giữa hai cụm" → 4 dendrogram khác nhau trên cùng dữ liệu.
   - GINI / Entropy / Error là 3 định nghĩa khác nhau của "độ lẫn lộn" → thường chọn cùng phép chia, nhưng Error kém nhạy hơn.

3. **Đánh giá trên dữ liệu "chưa thấy".**
   - Clustering: SSE luôn giảm khi tăng K → không thể dùng SSE một mình để chọn K.
   - Classification: lỗi trên tập huấn luyện luôn giảm khi cây lớn lên → không dùng để ước lượng lỗi thật (overfitting).
   - Association: confidence cao chưa chắc là luật thú vị (bổ sung: lift).
   → Cùng một bài học: **chỉ số tối ưu hóa trên chính dữ liệu đã dùng sẽ luôn "lạc quan" quá mức.**

4. **Similarity vs distance** — bẫy thường gặp nhất trong bài thi tay: với ma trận *similarity* thì gộp cặp có giá trị **lớn nhất**, và single link = **max** similarity, complete link = **min** similarity.

---

## 3. Bảng so sánh tổng hợp

### 3.1 Các phương pháp phân cụm trong slide

| | K-means | Bisecting K-means | Hierarchical (agglomerative) |
|---|---|---|---|
| Kiểu | Partitional | Partitional (hoặc cây chia đôi) | Hierarchical (dendrogram) |
| Cần biết K trước? | Có | Có | Không (cắt cây sau) |
| Hàm mục tiêu | SSE toàn cục | SSE (chọn cặp tách tốt nhất) | Cục bộ (từng bước gộp) |
| Nhạy với khởi tạo? | Rất nhạy | Ít nhạy hơn | Không (deterministic, trừ khi hoà) |
| Độ phức tạp | $O(nKId)$ — tuyến tính theo n | ~ như K-means | Bộ nhớ $O(N^2)$, thời gian $O(N^3)$ |
| Yếu điểm | Cụm khác cỡ / mật độ / không lồi; outlier | Như K-means | Không hoàn tác; nhạy nhiễu (MIN); vỡ cụm lớn (MAX) |

### 3.2 Bốn kiểu linkage

| Linkage | Định nghĩa | Ưu | Nhược |
|---|---|---|---|
| MIN (single) | cặp điểm **gần nhất** | Bắt được hình dạng bất kỳ | Nhiễu, hiệu ứng chuỗi (chaining) |
| MAX (complete) | cặp điểm **xa nhất** | Ít nhạy nhiễu | Bẻ gãy cụm lớn, thiên cụm tròn |
| Group average | trung bình mọi cặp | Dung hoà MIN và MAX | Thiên cụm tròn |
| Ward | độ tăng SSE khi gộp | "K-means phân cấp", dùng để khởi tạo K-means | Thiên cụm tròn |

Luôn có: $d_{MIN} \le d_{AVG} \le d_{MAX}$.

### 3.3 Ba độ đo tạp chất (2 lớp, tỉ lệ $p$)

| Độ đo | Công thức | Max (2 lớp) | Ghi chú |
|---|---|---|---|
| GINI | $1-\sum p_j^2 = 2p(1-p)$ | 0.5 | CART, SLIQ, SPRINT |
| Entropy | $-\sum p_j \log_2 p_j$ | 1 | ID3, C4.5 → Information Gain |
| Error | $1-\max p_j = \min(p,1-p)$ | 0.5 | Tuyến tính → kém nhạy, ít dùng để xây cây |

---

## 4. Những điều quan trọng phát hiện khi đọc kỹ slide

### 4.1 Phạm vi môn học (để ôn đúng trọng tâm)
- **Chương Clustering trong slide KHÔNG có DBSCAN** (chỉ được nhắc tên ở mục "density-based") **và KHÔNG có các chỉ số đánh giá cụm** như silhouette, entropy/purity. Chỉ có **SSE**. Slide 95 là slide cuối của chương 8.
- **Chương Classification dừng ở post-pruning.** Không có confusion matrix, precision/recall, cross-validation, ROC (slide 168 chỉ nêu tên "Missing values", "Costs of classification"). Phụ lục trong file 08 có phần này, đánh dấu (bổ sung), chỉ để tham khảo.
- **Gain ratio / SplitINFO không có trong slide** → được thêm dưới dạng (bổ sung) vì liên quan trực tiếp đến nhược điểm của Information Gain mà slide có nêu.

→ **Dạng bài tính tay có khả năng ra thi cao nhất** (theo nội dung slide):
1. Chạy tay **K-means** vài vòng, tính **SSE**.
2. Chạy tay **hierarchical** với MIN / MAX / Group average trên ma trận khoảng cách hoặc similarity, vẽ **dendrogram**.
3. Chạy tay **Apriori** (C1→L1→C2→L2→…), sinh luật, tính **support / confidence**; xác định **closed / maximal itemset**.
4. Tính **GINI / Entropy / Information Gain / Error** để chọn thuộc tính chia, kể cả thuộc tính liên tục (quét ngưỡng).
5. Câu hỏi lý thuyết: hạn chế của K-means, overfitting, so sánh linkage, nguyên lý Apriori, số luật có thể có.

### 4.2 Lỗi trên slide (đã kiểm tra lại bằng tính toán)

Biết các lỗi này giúp bạn không bị rối khi tự tính ra kết quả khác slide:

| Slide | Slide ghi | Đúng ra là |
|---|---|---|
| **89** (Group average, ma trận similarity I1–I5) | Dendrogram giống hệt của single link | {1,2} gộp với {4,5} trước (0.4875), điểm 3 vào **cuối cùng** (0.375) |
| **90** (Group average, 6 điểm) | Hình vẽ | Thực ra là hình của Ward; hình "Group Average" ở slide 93 mới đúng |
| **109** (Apriori) | $\sigma$({Bread, Milk, Diaper}) = 3 | = **2** (chỉ T4, T5) |
| **114** (Closed itemset) | Tô vàng {B,C}, {C,D}; không tô {B,C,D} | Closed đúng là: **B, AB, BD, ABD, BCD, ABCD** ({B,C} có cùng support 3 với {B,C,D} nên không closed) |
| **155** (GINI nhị phân) | Gini(Children) = 0.369 | $\frac{7}{12}\cdot\frac{20}{49} + \frac{5}{12}\cdot 0.32 \approx$ **0.371** |
| **160** (Entropy) | $-\frac16\log_2\frac16 - \frac56\log_2\frac{1}{6}$ | Số hạng thứ hai phải là $\log_2\frac{5}{6}$ (kết quả 0.65 vẫn đúng) |

Ngoài ra: trên bộ dữ liệu "Cheat", slide 139 chọn **Refund** làm gốc để minh hoạ thuật toán Hunt; **Refund không phải phép chia tốt nhất** theo GINI (Marital Status và Income ≤ 97 đều cho 0.300 < 0.343).

---

## 5. Lời khuyên cho tờ A4 viết tay (recto-verso)

Mỗi file có mục **"Tóm tắt cho tờ A4"**. Khi chép lên giấy, ưu tiên theo thứ tự:
1. **Công thức** (SSE, support/confidence, $3^d-2^{d+1}+1$, GINI, Entropy, Error, Gain, Ward $\Delta$, cập nhật ma trận MIN/MAX/AVG).
2. **Bảng log₂ và các giá trị GINI/Entropy đã tính sẵn** (file 07) → tiết kiệm rất nhiều thời gian khi thi.
3. **Các bước thuật toán** (K-means, agglomerative, Apriori join–prune–count, Hunt).
4. **Bẫy similarity / distance** và danh sách lỗi slide ở mục 4.2.
5. Bảng so sánh ưu/nhược (mục 3).

Phần lý thuyết dạng chữ (định nghĩa DM, các thách thức…) chỉ cần vài từ khoá vì dễ nhớ.


---

# Phần 1 — Thông tin môn học & Chương 1: Giới thiệu Data Mining (slides 1–24)

> Nguồn: `slides-dm.pdf`, slides 1–24. Slides 3–24 lấy từ bộ slide gốc của Tan, Steinbach, Kumar, *Introduction to Data Mining* (2006), chương 1.
> Quy ước: phần nào **không có trên slide** mà mình thêm vào để giải thích thì được đánh dấu **(bổ sung)**.

---

## 0. Thông tin môn học (slides 1–2)

### Slide 1 — Cách đánh giá (Modalités de contrôle de connaissances)

- Giảng viên: **radu.ciucanu@insa-cvl.fr**; trang môn học trên Celene: `https://celene.insa-cvl.fr/course/view.php?id=479`.
- Hình thức: **Contrôle continu intégral** (đánh giá liên tục hoàn toàn, không có thi cuối kỳ riêng):
  - **50 % : Interro sur papier** (bài kiểm tra trên giấy) — ngày **2 tháng 12** (2 décembre).
    - Tài liệu được phép mang: **một tờ A4 viết tay, hai mặt** (*une feuille A4 recto-verso manuscrite*). → Không được in, không được photo: phải **chép tay**.
  - **50 % : Rendu TD machine × 3** (nộp 3 bài thực hành trên máy) qua Celene, **làm cá nhân hoặc theo cặp** (*individuel ou en binôme*).

**Gợi ý chiến lược (bổ sung):** vì tờ A4 phải viết tay, hãy ưu tiên ghi những thứ khó nhớ: công thức (khoảng cách, SSE, support/confidence, Gini/entropy…), các bước thuật toán (K-means, Apriori, Hunt…), và các bảng "ưu/nhược điểm". Phần định nghĩa ở chương 1 nên **hiểu** chứ không cần chép nhiều.

### Slide 2 — Tài liệu & cấu trúc môn học (Supports de cours)

- Sách: **P.-N. Tan, M. Steinbach, V. Kumar. *Introduction to Data Mining*, 2006.** (link: `https://www-users.cs.umn.edu/~kumar001/dmbook/firsted.php`).
- 4 phần, **theo thứ tự này** (chú ý: không theo thứ tự chương của sách):
  1. Introduction (Ch 1)
  2. Cluster Analysis — Phân tích cụm (Ch 8)
  3. Association Analysis — Phân tích luật kết hợp (Ch 6)
  4. Classification — Phân lớp (Ch 4)

**Phân tích:** thứ tự này đi từ phương pháp **mô tả / không giám sát** (clustering, association) sang phương pháp **dự đoán / có giám sát** (classification). TD đầu tiên là về clustering, nên phần 2 là quan trọng nhất cho TD1.

---

## 1. Vì sao phải khai phá dữ liệu? (slides 3–4)

### Slide 3 — Góc nhìn thương mại (Commercial Viewpoint)

Ba lý do:
1. **Rất nhiều dữ liệu đang được thu thập và lưu trữ (collected and warehoused)**:
   - dữ liệu web, thương mại điện tử (e-commerce);
   - lịch sử mua hàng ở cửa hàng bách hóa / siêu thị (department/grocery stores);
   - giao dịch ngân hàng / thẻ tín dụng (Bank/Credit Card transactions).
2. **Máy tính ngày càng rẻ và mạnh hơn** → có thể xử lý khối dữ liệu lớn.
3. **Áp lực cạnh tranh mạnh (Competitive Pressure)** → doanh nghiệp muốn cung cấp dịch vụ tốt hơn, **cá nhân hóa (customized)** để có **lợi thế (edge)**, ví dụ trong **CRM — Customer Relationship Management** (quản lý quan hệ khách hàng).

**Ví dụ trực quan:** Một siêu thị có hàng triệu hóa đơn mỗi tháng. Nếu chỉ lưu mà không phân tích thì dữ liệu là "chi phí". Data mining biến nó thành "tài sản": biết nhóm khách nào hay mua gì để gửi khuyến mãi đúng người.

### Slide 4 — Góc nhìn khoa học (Scientific Viewpoint)

- Dữ liệu được thu thập với tốc độ khổng lồ (**GB/giờ**):
  - cảm biến trên vệ tinh (remote sensors on a satellite);
  - kính thiên văn quét bầu trời (telescopes scanning the skies);
  - **microarrays** sinh dữ liệu biểu hiện gen (gene expression data) — hình các chấm xanh/đỏ trên slide là ảnh microarray;
  - mô phỏng khoa học sinh ra hàng **terabyte** dữ liệu (hình bản đồ nhiệt độ / dòng chảy là ví dụ mô phỏng khí hậu).
- **Kỹ thuật truyền thống không khả thi với dữ liệu thô (Traditional techniques infeasible for raw data)**.
- Data mining giúp nhà khoa học:
  - **phân lớp và phân đoạn dữ liệu (classifying and segmenting data)**;
  - **hình thành giả thuyết (Hypothesis Formation)**.

**Phân tích sâu / đánh giá:** Điểm then chốt: data mining **không thay thế** phương pháp khoa học mà **gợi ý giả thuyết** để kiểm chứng sau. Ví dụ: clustering gen theo mức biểu hiện cho thấy một nhóm gen "đi cùng nhau" → nhà sinh học đặt giả thuyết chúng cùng tham gia một cơ chế sinh học → làm thí nghiệm kiểm chứng.

---

## 2. Data Mining là gì? (slides 5–7)

### Slide 5 — Định nghĩa (What is Data Mining?)

Slide đưa **hai định nghĩa** (cần thuộc ý chính):

1. *"Non-trivial extraction of **implicit**, **previously unknown** and **potentially useful** information from data"*
   → Trích xuất **không tầm thường** những thông tin **ẩn**, **chưa từng biết trước** và **có khả năng hữu ích** từ dữ liệu.
2. *"Exploration & analysis, by **automatic or semi-automatic** means, of **large quantities of data** in order to discover **meaningful patterns**"*
   → Khám phá và phân tích, bằng phương tiện **tự động hoặc bán tự động**, **lượng lớn dữ liệu** nhằm phát hiện **các mẫu (patterns) có ý nghĩa**.

Giải nghĩa từng từ khóa:
| Từ khóa | Ý nghĩa | Ví dụ |
|---|---|---|
| non-trivial | không phải phép tính hiển nhiên | "tổng doanh thu tháng 3" là trivial; "khách mua tã thường mua bia" là non-trivial |
| implicit | ẩn trong dữ liệu, không ghi trực tiếp | không cột nào ghi "nhóm khách hàng", nhưng có thể suy ra |
| previously unknown | mới, chưa ai biết | nếu ai cũng biết rồi thì không phải "khám phá" |
| potentially useful | dùng được để ra quyết định | luật kết hợp → sắp xếp kệ hàng |
| automatic / semi-automatic | máy làm phần lớn, người có thể can thiệp (chọn tham số, diễn giải) | chọn K trong K-means là phần "semi" |

**Hình trên slide 5 — quy trình KDD (Knowledge Discovery in Databases)** (tên "KDD" và tác giả Fayyad et al. 1996 là **bổ sung**; slide chỉ vẽ sơ đồ). Các bước đọc từ trái-dưới lên phải-trên:

```
Data --Selection--> Target Data --Preprocessing--> Preprocessed Data
     --Transformation--> Transformed Data --Data Mining--> Patterns
     --Interpretation/Evaluation--> Knowledge
```

| Bước | Làm gì | Ví dụ (siêu thị) |
|---|---|---|
| **Selection** (chọn lọc) | chọn phần dữ liệu liên quan → *Target Data* | chỉ lấy hóa đơn năm 2025 của khách có thẻ thành viên |
| **Preprocessing** (tiền xử lý) | làm sạch: giá trị thiếu, nhiễu, trùng lặp → *Preprocessed Data* | xóa hóa đơn trùng, điền tuổi bị thiếu |
| **Transformation** (biến đổi) | đổi dạng/chuẩn hóa/rút gọn chiều → *Transformed Data* | chuẩn hóa thu nhập & tuổi về cùng thang đo; gộp thành "giỏ hàng" |
| **Data Mining** | áp dụng thuật toán → *Patterns* | chạy K-means / Apriori / cây quyết định |
| **Interpretation/Evaluation** (diễn giải/đánh giá) | lọc mẫu thực sự có ý nghĩa → *Knowledge* | chuyên gia marketing xem cụm nào có ý nghĩa kinh doanh |

**Phân tích sâu:**
- Data mining (theo nghĩa hẹp) chỉ là **một bước** trong quy trình KDD; nhưng trong thực tế người ta hay gọi cả quy trình là "data mining".
- Quy trình **lặp (iterative)** (bổ sung): kết quả đánh giá xấu → quay lại chọn dữ liệu/tiền xử lý khác.
- "Garbage in, garbage out" (bổ sung): tiền xử lý thường chiếm phần lớn thời gian. Liên hệ TD clustering: **quên chuẩn hóa dữ liệu** trước K-means là lỗi kinh điển (xem mục Euclid ở slide 18).

### Slide 6 — Cái gì là / không là Data Mining?

| **Không phải** Data Mining | **Là** Data Mining |
|---|---|
| Tra số điện thoại trong danh bạ | Phát hiện một số họ phổ biến hơn ở một số vùng của Mỹ (O'Brien, O'Rurke, O'Reilly… ở khu vực Boston) |
| Gõ "Amazon" vào công cụ tìm kiếm để lấy thông tin | **Gom nhóm** các tài liệu tương tự do công cụ tìm kiếm trả về theo ngữ cảnh (vd. *Amazon rainforest* vs *Amazon.com*) |

**Nguyên tắc phân biệt:**
- Bên trái = **truy vấn (query / information retrieval)**: ta *biết trước* mình tìm gì, câu trả lời đã có sẵn và được lấy ra trực tiếp.
- Bên phải = **khám phá mẫu**: kết quả là tri thức *mới*, *tổng quát* (một quy luật về phân bố họ theo vùng; một cách nhóm tài liệu) mà không ai ghi sẵn trong dữ liệu.
- Ví dụ "Amazon" bên phải chính là **clustering** tài liệu → liên hệ trực tiếp với chương 8.

**Mẹo kiểm tra (bổ sung):** Hỏi "kết quả có phải là một **mẫu/quy luật tổng quát** rút ra từ nhiều bản ghi không?" Có → data mining. Chỉ là lấy lại một bản ghi/tập bản ghi đã biết điều kiện → query.

### Slide 7 — Nguồn gốc của Data Mining (Origins)

- Kế thừa ý tưởng từ: **machine learning / AI**, **pattern recognition** (nhận dạng mẫu), **statistics** (thống kê), và **database systems** (hệ quản trị CSDL). Sơ đồ Venn: ba vòng tròn *Statistics/AI*, *Machine Learning/Pattern Recognition*, *Database systems*, **Data Mining nằm ở giao** của cả ba.
- **Kỹ thuật truyền thống có thể không phù hợp** vì:
  - **Enormity of data** — dữ liệu khổng lồ;
  - **High dimensionality** — số chiều (số thuộc tính) rất cao;
  - **Heterogeneous, distributed nature** — dữ liệu không đồng nhất (nhiều kiểu), phân tán (nhiều nơi).

**Phân tích:** Mỗi lĩnh vực đóng góp một thứ: thống kê → mô hình hóa, kiểm định, ước lượng; ML/PR → thuật toán học; CSDL → lưu trữ, truy cập, xử lý hiệu quả dữ liệu lớn. Ba lý do "truyền thống không phù hợp" chính là tiền thân của danh sách **thách thức** ở slide 24.

---

## 3. Các nhiệm vụ của Data Mining (slides 8–9)

### Slide 8 — Hai loại phương pháp

- **Prediction Methods (phương pháp dự đoán):** dùng một số biến để **dự đoán giá trị chưa biết hoặc tương lai** của các biến khác.
- **Description Methods (phương pháp mô tả):** tìm các **mẫu mà con người diễn giải được (human-interpretable patterns)** để **mô tả** dữ liệu.

**Ví dụ:**
- Dự đoán: "khách hàng X có gian lận không?" (biến cần đoán: `Cheat`).
- Mô tả: "khách hàng của ta chia thành 3 nhóm: sinh viên, gia đình trẻ, người về hưu" — không có biến đích, chỉ mô tả cấu trúc.

**Liên hệ (bổ sung):** Prediction ≈ **học có giám sát (supervised learning)** — có biến đích/nhãn; Description ≈ thường là **học không giám sát (unsupervised)** — không có nhãn.

### Slide 9 — Danh sách các nhiệm vụ (Data Mining Tasks…)

| Nhiệm vụ | Loại (theo slide) | Chương liên quan |
|---|---|---|
| **Classification** (phân lớp) | [Predictive] | Ch 4 (phần 4 của môn) |
| **Clustering** (phân cụm) | [Descriptive] | Ch 8 (phần 2, TD1) |
| **Association Rule Discovery** (khám phá luật kết hợp) | [Descriptive] | Ch 6 (phần 3) |
| **Sequential Pattern Discovery** (khám phá mẫu tuần tự) | [Descriptive] | không được chi tiết trong các slide 1–24 |
| **Regression** (hồi quy) | [Predictive] | slide 17 |
| **Deviation Detection** (phát hiện độ lệch / bất thường) | [Predictive] | slide 14 |

⚠️ **Thuộc lòng nhãn [Predictive]/[Descriptive]** — câu hỏi kiểu "Clustering là predictive hay descriptive?" rất dễ ra.

- *Sequential Pattern Discovery (bổ sung, slide chỉ liệt kê tên):* giống luật kết hợp nhưng **có thứ tự thời gian**, vd. "khách mua máy ảnh → vài tuần sau mua thẻ nhớ → sau đó mua chân máy".
- Lưu ý: slide xếp *Deviation Detection* vào **[Predictive]** (theo bộ slide gốc của Tan et al.). Trong thực tế (bổ sung) phát hiện bất thường có thể làm theo kiểu có giám sát (có nhãn "gian lận/bình thường") hoặc không giám sát. Ở bài thi, **trả lời theo slide: Predictive**.

---

## 4. Classification — Phân lớp (slides 10–13, 15–16)

### Slide 10 — Định nghĩa

- Cho một tập bản ghi (**training set** — tập huấn luyện):
  - mỗi bản ghi gồm một tập **thuộc tính (attributes)**, **một** trong số đó là **lớp (class)**.
- Tìm một **mô hình (model)** cho thuộc tính lớp **như một hàm của giá trị các thuộc tính khác**.
- **Mục tiêu:** các bản ghi **chưa từng thấy (previously unseen)** phải được gán lớp **chính xác nhất có thể**.
  - Dùng một **test set** (tập kiểm thử) để đo **độ chính xác (accuracy)** của mô hình. Thường tập dữ liệu ban đầu được **chia thành training set và test set**: training để **xây** mô hình, test để **kiểm chứng (validate)** nó.

Viết dưới dạng hàm (bổ sung, cách hình thức hóa):
$$ y = f(x_1, x_2, \dots, x_d) $$
- $x_1,\dots,x_d$: các thuộc tính mô tả (vd. Refund, Marital Status, Taxable Income);
- $y$: thuộc tính lớp, **rời rạc / phân loại** (vd. Cheat ∈ {Yes, No});
- $f$: mô hình cần học (cây quyết định, luật, k-NN, …).

Độ chính xác (bổ sung, chi tiết ở Ch 4):
$$ \text{Accuracy} = \frac{\text{số bản ghi test dự đoán đúng}}{\text{tổng số bản ghi test}}, \qquad \text{Error rate} = 1 - \text{Accuracy} $$
Ví dụ: test set có 6 bản ghi, mô hình đoán đúng 5 → Accuracy = 5/6 ≈ 0,83; error rate ≈ 0,17.

**Vì sao phải tách train/test? (phân tích sâu)** Nếu đánh giá ngay trên dữ liệu đã dùng để học, mô hình có thể chỉ "học thuộc lòng" (overfitting — bổ sung) và cho độ chính xác 100 % giả tạo. Giống như cho học sinh làm lại đúng đề đã chữa: điểm cao không chứng minh hiểu bài. Test set = "đề thi mới".

### Slide 11 — Ví dụ phân lớp (Classification Example)

Bảng **Training Set** (chép lại từ slide):

| Tid | Refund *(categorical)* | Marital Status *(categorical)* | Taxable Income *(continuous)* | Cheat *(class)* |
|---|---|---|---|---|
| 1 | Yes | Single | 125K | No |
| 2 | No | Married | 100K | No |
| 3 | No | Single | 70K | No |
| 4 | Yes | Married | 120K | No |
| 5 | No | Divorced | 95K | **Yes** |
| 6 | No | Married | 60K | No |
| 7 | Yes | Divorced | 220K | No |
| 8 | No | Single | 85K | **Yes** |
| 9 | No | Married | 75K | No |
| 10 | No | Single | 90K | **Yes** |

Bảng **Test Set** (lớp chưa biết, ký hiệu "?"):

| Refund | Marital Status | Taxable Income | Cheat |
|---|---|---|---|
| No | Single | 75K | ? |
| Yes | Married | 50K | ? |
| No | Married | 150K | ? |
| Yes | Divorced | 90K | ? |
| No | Single | 40K | ? |
| No | Married | 80K | ? |

Sơ đồ: **Training Set → Learn Classifier → Model**; sau đó **Test Set → Model** để dự đoán "?".

Ý nghĩa: bài toán phát hiện **gian lận thuế** (Cheat). *Refund* = có được hoàn thuế hay không; *Marital Status* = tình trạng hôn nhân; *Taxable Income* = thu nhập chịu thuế.

**Các kiểu thuộc tính trên slide:**
- **categorical** (định danh/phân loại): Refund, Marital Status — giá trị là nhãn, không có phép cộng trừ.
- **continuous** (liên tục): Taxable Income — số thực.
- **class**: Cheat — thuộc tính cần dự đoán.

**Thử "học" bằng tay (bổ sung — chính là cây quyết định kinh điển của Ch 4):** quan sát 3 bản ghi Cheat = Yes (Tid 5, 8, 10): tất cả đều *Refund = No*, *không Married*, thu nhập 85K–95K. Ta có thể đề xuất luật:

> Nếu Refund = Yes → No.
> Nếu Refund = No và Married → No.
> Nếu Refund = No, Single/Divorced, Income > 80K → Yes; ngược lại → No.

Kiểm tra trên training: Tid 3 (No, Single, 70K) → No ✔; Tid 5, 8, 10 → Yes ✔; mọi bản ghi Married hoặc Refund = Yes → No ✔ → đúng 10/10.
Áp dụng cho test set: (No, Single, 75K) → No; (Yes, Married, 50K) → No; (No, Married, 150K) → No; (Yes, Divorced, 90K) → No; (No, Single, 40K) → No; (No, Married, 80K) → No.

**Nhận xét:** đúng 10/10 trên training **không** đảm bảo tốt trên dữ liệu mới — chỉ có 10 bản ghi, ngưỡng 80K là "đoán" từ rất ít dữ liệu. Đó là lý do cần test set có nhãn thật để đo accuracy.

### Slide 12 — Ứng dụng 1: Marketing trực tiếp (Direct Marketing)

- **Mục tiêu:** giảm chi phí gửi thư quảng cáo bằng cách **nhắm (targeting)** vào nhóm người tiêu dùng có khả năng mua một sản phẩm điện thoại di động mới.
- **Cách làm:**
  - dùng dữ liệu của một **sản phẩm tương tự đã ra mắt trước đây**;
  - ta biết khách nào đã mua, khách nào không → quyết định **{buy, don't buy}** chính là **class attribute**;
  - thu thập thông tin nhân khẩu học, lối sống, tương tác với công ty của các khách đó (loại hình công việc, nơi ở, thu nhập…);
  - dùng làm **thuộc tính đầu vào** để học **classifier**.

**Điểm mấu chốt:** *nhãn lấy từ quá khứ* (sản phẩm cũ) để dự đoán cho tương lai (sản phẩm mới). Đây là mẫu chung của mọi ứng dụng phân lớp.

### Slide 13 — Ứng dụng 2: Phát hiện gian lận (Fraud Detection)

- **Mục tiêu:** dự đoán các giao dịch thẻ tín dụng gian lận.
- **Cách làm:**
  - dùng giao dịch thẻ + thông tin chủ tài khoản làm thuộc tính (khi nào mua, mua gì, có trả đúng hạn thường xuyên không…);
  - **gán nhãn** giao dịch quá khứ là *fraud* hoặc *fair* → **class attribute**;
  - học mô hình cho lớp của giao dịch;
  - dùng mô hình để phát hiện gian lận bằng cách quan sát các giao dịch trên một tài khoản.

**Phân tích sâu (bổ sung):** dữ liệu gian lận thường **mất cân bằng (imbalanced)** — 99,9 % giao dịch hợp lệ. Một mô hình "luôn đoán fair" có accuracy 99,9 % nhưng vô dụng → accuracy không phải lúc nào cũng là thước đo tốt (sẽ gặp lại ở Ch 4).

### Slide 14 — Phát hiện độ lệch / bất thường (Deviation/Anomaly Detection)

- **Phát hiện các độ lệch đáng kể so với hành vi bình thường (significant deviations from normal behavior).**
- Ứng dụng:
  - phát hiện gian lận thẻ tín dụng (Credit Card Fraud Detection);
  - phát hiện xâm nhập mạng (Network Intrusion Detection) — hình minh họa: kính lúp soi Internet với các loại tấn công **DOS, probe, U2R** (tên các loại tấn công trong bộ dữ liệu KDD Cup 99 — bổ sung).
- Chú thích: lưu lượng mạng ở mức một trường đại học có thể vượt **100 triệu kết nối mỗi ngày**.

**Ví dụ:** thẻ của bạn thường chỉ chi 20–50 € ở Bourges; đột nhiên có giao dịch 3 000 € ở nước khác lúc 3h sáng → "lệch khỏi hành vi bình thường" → cảnh báo.

**So sánh với slide 13:** cùng bài toán gian lận nhưng góc nhìn khác — slide 13 học từ nhãn *fraud/fair* (classification); slide 14 mô hình hóa "bình thường" rồi tìm cái lệch. Con số 100 triệu kết nối/ngày nhấn mạnh thách thức **scalability**.

**Liên hệ (bổ sung):** trong clustering, các điểm không thuộc cụm nào / xa mọi tâm cụm có thể coi là **outlier** — DBSCAN gọi chúng là *noise points*.

### Slide 15 — Ứng dụng 3: Khách hàng rời bỏ (Customer Attrition/Churn)

- **Mục tiêu:** dự đoán khách hàng có khả năng **bị mất về tay đối thủ** hay không.
- **Cách làm:**
  - dùng lịch sử giao dịch chi tiết với từng khách hàng cũ và hiện tại để tạo thuộc tính (tần suất gọi, gọi đi đâu, gọi giờ nào nhiều nhất, tình trạng tài chính, hôn nhân…);
  - gán nhãn khách hàng là **loyal** (trung thành) hoặc **disloyal**;
  - tìm mô hình cho lòng trung thành.

**Ví dụ:** nhà mạng di động thấy khách giảm số cuộc gọi dần và hay gọi tổng đài khiếu nại → mô hình dự đoán "disloyal" → gửi ưu đãi giữ chân.

### Slide 16 — Ứng dụng 4: Lập danh mục khảo sát bầu trời (Sky Survey Cataloging)

- **Mục tiêu:** dự đoán lớp (**star** hay **galaxy** — sao hay thiên hà) của các vật thể trên trời, đặc biệt các vật thể **mờ (visually faint)**, từ ảnh khảo sát kính viễn vọng (đài thiên văn **Palomar**).
  - **3000 ảnh**, mỗi ảnh **23 040 × 23 040 pixel**.
- **Cách làm:**
  - **phân đoạn ảnh (segment the image)** để tách từng vật thể;
  - đo các thuộc tính ảnh (**features**) — **40 thuộc tính** mỗi vật thể;
  - mô hình hóa lớp dựa trên các features đó.
  - **Thành công:** tìm được **16 quasar dịch chuyển đỏ cao (high red-shift quasars)** mới — thuộc những vật thể xa nhất, rất khó tìm.

**Phân tích:** ví dụ cho thấy quy trình KDD đầy đủ: dữ liệu thô (pixel) → **transformation** thành 40 features → classification → tri thức khoa học. Cũng minh họa quy mô dữ liệu: $3000 \times 23040^2 \approx 1{,}6\times10^{12}$ pixel (tính thêm — bổ sung).

---

## 5. Regression — Hồi quy (slide 17)

- **Dự đoán giá trị của một biến liên tục (continuous valued variable)** dựa trên giá trị các biến khác, **giả định một mô hình phụ thuộc tuyến tính hoặc phi tuyến** (linear or nonlinear model of dependency).
- Được nghiên cứu nhiều trong **thống kê** và **mạng nơ-ron (neural network)**.
- Ví dụ:
  - dự đoán **doanh số** sản phẩm mới dựa trên **chi phí quảng cáo**;
  - dự đoán **tốc độ gió** theo nhiệt độ, độ ẩm, áp suất không khí…;
  - dự đoán **chuỗi thời gian (time series)** chỉ số thị trường chứng khoán.

Mô hình tuyến tính đơn giản (bổ sung):
$$ \hat{y} = w_0 + w_1 x $$
- $x$: biến đầu vào (vd. chi phí quảng cáo, nghìn €); $\hat{y}$: giá trị dự đoán (doanh số); $w_0$: hệ số chặn; $w_1$: độ dốc (tăng 1 đơn vị $x$ thì $\hat y$ tăng $w_1$).
- Ví dụ số: $w_0 = 10$, $w_1 = 3$; chi 5 nghìn € quảng cáo → $\hat{y} = 10 + 3\cdot 5 = 25$ (nghìn sản phẩm).

**Classification vs Regression:** cả hai đều *predictive* và có biến đích; khác nhau ở **kiểu biến đích**: rời rạc/phân loại (classification) vs **liên tục** (regression).

---

## 6. Clustering — Phân cụm (slides 18–20) ★ quan trọng cho TD1

### Slide 18 — Định nghĩa (Clustering Definition)

- Cho một tập **điểm dữ liệu**, mỗi điểm có một tập **thuộc tính**, và một **độ đo tương tự (similarity measure)** giữa chúng, tìm các **cụm (clusters)** sao cho:
  - các điểm **trong cùng một cụm** thì **giống nhau hơn**;
  - các điểm **ở các cụm khác nhau** thì **ít giống nhau hơn**.
- **Độ đo tương tự (Similarity Measures):**
  - **Khoảng cách Euclid (Euclidean Distance)** nếu các thuộc tính là **liên tục**;
  - các độ đo khác tùy bài toán (**problem-specific**).

**Công thức khoảng cách Euclid** (slide chỉ nêu tên; công thức là bổ sung, sẽ gặp lại ở Ch 8):
$$ d(\mathbf{x}, \mathbf{y}) = \sqrt{\sum_{k=1}^{n} (x_k - y_k)^2} $$
- $\mathbf{x} = (x_1,\dots,x_n)$, $\mathbf{y} = (y_1,\dots,y_n)$: hai điểm dữ liệu với $n$ thuộc tính;
- $x_k - y_k$: chênh lệch ở thuộc tính thứ $k$;
- bình phương → cộng → căn bậc hai: chính là "độ dài đoạn thẳng" nối hai điểm (Pythagore tổng quát).

**Ví dụ số:** $\mathbf{x} = (1, 2, 3)$, $\mathbf{y} = (4, 6, 3)$:
$d = \sqrt{(1-4)^2 + (2-6)^2 + (3-3)^2} = \sqrt{9 + 16 + 0} = \sqrt{25} = 5.$

**Lưu ý quan trọng:** khoảng cách **nhỏ** = **tương tự cao** (khoảng cách là *dissimilarity*, ngược chiều với similarity).

**Phân tích sâu / cạm bẫy (bổ sung, rất hay gặp trong TD):**
- **Thang đo (scale):** khách A = (tuổi 25, thu nhập 30 000), B = (tuổi 60, thu nhập 31 000). $d = \sqrt{35^2 + 1000^2} \approx 1000{,}6$ → gần như chỉ do thu nhập quyết định; tuổi chênh 35 năm bị "nuốt". → **Phải chuẩn hóa** (vd. z-score $\frac{x-\mu}{\sigma}$ hoặc min-max) trước khi clustering.
- Euclid chỉ hợp lý với **thuộc tính số liên tục**. Với thuộc tính categorical (Marital Status…) cần độ đo khác (vd. simple matching, Jaccard) — đó là "problem-specific measures" của slide.
- Chọn độ đo khác → **kết quả cụm khác**. Clustering không có "đáp án đúng duy nhất".

### Slide 19 — Minh họa phân cụm (Illustrating Clustering)

- *Euclidean Distance Based Clustering in 3-D space* — phân cụm dựa trên khoảng cách Euclid trong không gian 3 chiều.
- Hình: 3 nhóm điểm (đỏ, hồng/tím, xanh ngọc) tách biệt rõ trong hệ trục 3D.
- Hai nguyên tắc (hai ô xanh trên slide):
  - **Intracluster distances are minimized** — khoảng cách **trong** cụm được **cực tiểu hóa** (cụm "chặt", *cohesion*);
  - **Intercluster distances are maximized** — khoảng cách **giữa** các cụm được **cực đại hóa** (cụm "tách biệt", *separation*).

**Liên hệ với Ch 8 (bổ sung):** hai ý này được định lượng bằng **SSE** (Sum of Squared Errors — tổng bình phương khoảng cách điểm tới tâm cụm, đo cohesion; càng nhỏ càng tốt) mà K-means tối thiểu hóa, và bằng các chỉ số như **silhouette** kết hợp cohesion + separation. Ví dụ trực quan: xếp học sinh vào bàn sao cho bạn cùng bàn thích cùng môn (gần nhau) và các bàn khác nhau thì sở thích khác hẳn nhau (xa nhau).

### Slide 20 — Ứng dụng 1: Phân khúc thị trường (Market Segmentation)

- **Mục tiêu:** chia thị trường thành các **tập con khách hàng phân biệt**, mỗi tập có thể được chọn làm **thị trường mục tiêu** và tiếp cận bằng một **marketing mix** riêng.
- **Cách làm:**
  - thu thập các thuộc tính khách hàng dựa trên thông tin **địa lý** và **lối sống**;
  - tìm các **cụm khách hàng tương tự**;
  - **đo chất lượng phân cụm** bằng cách quan sát **mẫu mua hàng** của khách **trong cùng cụm** so với khách ở **các cụm khác**.

**Phân tích sâu:** điểm thú vị là **đánh giá** — vì clustering không có nhãn, ta kiểm tra "gián tiếp": nếu khách cùng cụm có hành vi mua giống nhau và khác cụm thì khác, phân cụm là có ích. Đây là ý tưởng *external/business validation*.
**So sánh với slide 12 (Direct Marketing):** slide 12 có nhãn {buy, don't buy} → classification; slide 20 **không có nhãn**, chỉ tìm nhóm → clustering.

---

## 7. Association Rule Discovery — Khám phá luật kết hợp (slides 21–23)

### Slide 21 — Định nghĩa

- Cho một tập bản ghi, mỗi bản ghi chứa một số **mục (items)** từ một tập cho trước;
  - sinh ra các **luật phụ thuộc (dependency rules)** để **dự đoán sự xuất hiện của một item dựa trên sự xuất hiện của các item khác**.

Dữ liệu giao dịch trên slide:

| TID | Items |
|---|---|
| 1 | Bread, Coke, Milk |
| 2 | Beer, Bread |
| 3 | Beer, Coke, Diaper, Milk |
| 4 | Beer, Bread, Diaper, Milk |
| 5 | Coke, Diaper, Milk |

Luật tìm được (Rules Discovered):
- **{Milk} → {Coke}**
- **{Diaper, Milk} → {Beer}**

Đọc luật $X \to Y$: "nếu giỏ hàng chứa $X$ thì **thường** cũng chứa $Y$". $X$ gọi là **antecedent** (vế trái, tiền đề), $Y$ là **consequent** (vế phải, hệ quả).

**Đo độ mạnh của luật (bổ sung — định nghĩa chính thức ở Ch 6):**
$$ \text{support}(X \to Y) = \frac{\sigma(X \cup Y)}{N}, \qquad \text{confidence}(X \to Y) = \frac{\sigma(X \cup Y)}{\sigma(X)} $$
- $\sigma(Z)$: số giao dịch chứa **tất cả** item trong $Z$ (support count);
- $N$: tổng số giao dịch;
- support: luật xuất hiện **thường xuyên** đến đâu; confidence: khi có $X$ thì **bao nhiêu phần** cũng có $Y$ (ước lượng $P(Y \mid X)$).

**Tính trên bảng slide** ($N = 5$):
- {Milk} → {Coke}: $\sigma(\text{Milk}) = 4$ (T1, T3, T4, T5); $\sigma(\text{Milk, Coke}) = 3$ (T1, T3, T5).
  → support $= 3/5 = 0{,}6$; confidence $= 3/4 = 0{,}75$.
- {Diaper, Milk} → {Beer}: $\sigma(\text{Diaper, Milk}) = 3$ (T3, T4, T5); $\sigma(\text{Diaper, Milk, Beer}) = 2$ (T3, T4).
  → support $= 2/5 = 0{,}4$; confidence $= 2/3 \approx 0{,}67$.

### Slide 22 — Ứng dụng 1: Marketing và khuyến mãi (Marketing and Sales Promotion)

Giả sử tìm được luật **{Bagels, …} → {Potato Chips}** (bánh mì vòng → khoai tây chiên):
- **Potato Chips là consequent** → dùng để xác định **cần làm gì để tăng doanh số khoai tây chiên** (bán thứ gì ở vế trái sẽ kéo theo chips).
- **Bagels ở antecedent** → dùng để xem **sản phẩm nào sẽ bị ảnh hưởng nếu cửa hàng ngừng bán bagels**.
- **Bagels ở antecedent *và* Potato Chips ở consequent** → dùng để xem **nên bán kèm gì với Bagels để thúc đẩy doanh số Potato Chips**.

**Ý chính:** cố định item ở vế trái hoặc vế phải ta trả lời được các câu hỏi kinh doanh khác nhau.

### Slide 23 — Ứng dụng 2: Quản lý kệ hàng siêu thị (Supermarket shelf management)

- **Mục tiêu:** xác định các món được **mua cùng nhau bởi đủ nhiều khách hàng** (→ ý "đủ nhiều" chính là ngưỡng **support** tối thiểu — bổ sung).
- **Cách làm:** xử lý dữ liệu **point-of-sale** (tại quầy thu ngân) thu bằng máy quét mã vạch để tìm phụ thuộc giữa các món.
- **Luật kinh điển:** nếu khách mua **tã (diaper) và sữa (milk)** thì rất có khả năng mua **bia (beer)**. → "Đừng ngạc nhiên nếu thấy lốc 6 lon bia xếp cạnh tã!"

**Phân tích sâu / đánh giá:**
- Luật kết hợp chỉ nói **đồng xuất hiện (co-occurrence)**, **không phải quan hệ nhân quả (causality)**. Mua tã không *gây ra* mua bia.
- Confidence cao chưa chắc thú vị nếu $Y$ vốn đã rất phổ biến (bổ sung: cần thêm chỉ số **lift** — Ch 6).
- Thách thức tính toán: với $d$ item có $2^d$ tập con → cần thuật toán như **Apriori** (Ch 6).

---

## 8. Thách thức của Data Mining (slide 24)

| Thách thức | Giải thích | Ví dụ |
|---|---|---|
| **Scalability** (khả năng mở rộng) | thuật toán phải chạy được khi dữ liệu cực lớn (GB, TB) | 100 triệu kết nối mạng/ngày (slide 14); 3000 ảnh 23040² (slide 16) |
| **Dimensionality** (số chiều cao) | hàng trăm/nghìn thuộc tính; độ phức tạp tăng nhanh theo số chiều | microarray: hàng nghìn gen; văn bản: mỗi từ là một chiều |
| **Complex and Heterogeneous Data** (dữ liệu phức tạp, không đồng nhất) | nhiều kiểu: số, phân loại, văn bản, ảnh, đồ thị, chuỗi thời gian | hồ sơ khách: tuổi (số) + nghề (categorical) + email (văn bản) |
| **Data Quality** (chất lượng dữ liệu) | nhiễu, thiếu giá trị, ngoại lai, trùng lặp | thu nhập ghi sai, tuổi bị thiếu |
| **Data Ownership and Distribution** (sở hữu & phân tán) | dữ liệu nằm ở nhiều nơi/nhiều tổ chức, không gom tập trung được | dữ liệu bệnh viện ở nhiều cơ sở |
| **Privacy Preservation** (bảo vệ quyền riêng tư) | khai phá mà không làm lộ thông tin cá nhân | dữ liệu y tế, ngân hàng (liên hệ RGPD/GDPR — bổ sung) |
| **Streaming Data** (dữ liệu dòng) | dữ liệu đến liên tục, không lưu hết được, phải xử lý một lượt | log mạng, giao dịch thẻ thời gian thực |

**Phân tích sâu (bổ sung):** "**Curse of dimensionality**" (lời nguyền số chiều): khi số chiều lớn, dữ liệu trở nên thưa, và khoảng cách giữa các điểm trở nên "gần như bằng nhau" → độ đo Euclid kém phân biệt → clustering khó. Liên hệ trực tiếp với độ đo tương tự ở slide 18 và với Ch 8.
Ba thách thức đầu (scalability, dimensionality, heterogeneous) khớp với ba lý do "kỹ thuật truyền thống không phù hợp" ở slide 7.

(Slide 25 là slide chuyển sang phần 2 — Cluster Analysis, Ch 8; không thuộc phần này.)

---

## 9. Dễ nhầm lẫn

1. **Classification vs Clustering:**
   - Classification: **có nhãn lớp** biết trước trong training set, lớp định nghĩa trước → **Predictive** (có giám sát).
   - Clustering: **không có nhãn**, các nhóm được **khám phá** từ dữ liệu → **Descriptive** (không giám sát).
   - Mẹo: "class" có trước khi học → classification; "cluster" chỉ có sau khi chạy thuật toán → clustering.
2. **Classification vs Regression:** cả hai đều predictive; biến đích **rời rạc** (Yes/No, star/galaxy) → classification; **liên tục** (doanh số, tốc độ gió) → regression.
3. **Data Mining vs Query/Information Retrieval (slide 6):** tra danh bạ, tìm "Amazon" trên Google là query, **không** phải data mining.
4. **Data Mining vs KDD:** theo sơ đồ slide 5, data mining là **một bước** trong quy trình (Selection → Preprocessing → Transformation → **Data Mining** → Interpretation/Evaluation).
5. **Test set trên slide 11 có "?":** ý là bản ghi chưa biết lớp cần dự đoán. Nhưng để **đo accuracy** (slide 10) thì test set phải có nhãn thật, chỉ là **không được dùng khi học**.
6. **Deviation Detection** được slide xếp **[Predictive]**, còn **Sequential Pattern Discovery** là **[Descriptive]** — dễ nhớ ngược.
7. **Similarity vs Distance:** khoảng cách Euclid nhỏ ⇔ tương tự lớn. "Intracluster distances minimized" = các điểm trong cụm **giống** nhau nhiều.
8. **Luật kết hợp ≠ nhân quả;** và $X \to Y$ khác $Y \to X$ (confidence khác nhau: {Milk}→{Coke} = 3/4 nhưng {Coke}→{Milk} = 3/3 = 1).
9. **Antecedent vs Consequent:** antecedent = vế **trái** (điều kiện, "nếu"), consequent = vế **phải** (kết quả, "thì").
10. **Fraud detection** xuất hiện ở **cả** classification (slide 13, học từ nhãn fraud/fair) **và** anomaly detection (slide 14, tìm độ lệch so với bình thường).

---

## 10. Câu hỏi có thể ra thi (kèm đáp án ngắn)

1. **Nêu định nghĩa data mining.**
   → Trích xuất không tầm thường thông tin ẩn, chưa biết trước và có thể hữu ích từ dữ liệu; hoặc khám phá & phân tích tự động/bán tự động lượng lớn dữ liệu để tìm mẫu có ý nghĩa.
2. **Liệt kê các bước của quy trình khám phá tri thức (sơ đồ slide 5).**
   → Selection → Preprocessing → Transformation → Data Mining → Interpretation/Evaluation → Knowledge.
3. **Cho các ví dụ sau, cái nào là data mining?** (a) tra số điện thoại; (b) nhóm kết quả tìm kiếm "Amazon" theo ngữ cảnh; (c) tìm họ phổ biến theo vùng.
   → (b) và (c). (a) là truy vấn đơn giản.
4. **Phân biệt phương pháp predictive và descriptive; xếp các nhiệm vụ vào hai nhóm.**
   → Predictive: dùng biến này đoán biến khác (Classification, Regression, Deviation Detection). Descriptive: tìm mẫu con người hiểu được (Clustering, Association Rules, Sequential Patterns).
5. **Khác nhau giữa classification và clustering? Cho một ví dụ ứng dụng mỗi loại.**
   → Classification có nhãn, dự đoán lớp cho bản ghi mới (direct marketing, fraud, churn, sky survey). Clustering không nhãn, gom điểm tương tự (market segmentation, gom tài liệu).
6. **Vì sao chia dữ liệu thành training set và test set?**
   → Training để xây mô hình; test (chưa thấy khi học) để đánh giá khách quan độ chính xác trên dữ liệu mới, tránh đánh giá lạc quan do "học thuộc".
7. **Trong bảng slide 11, xác định kiểu từng thuộc tính.**
   → Refund: categorical; Marital Status: categorical; Taxable Income: continuous; Cheat: class.
8. **Mục tiêu của clustering theo hai tiêu chí khoảng cách?**
   → Cực tiểu hóa khoảng cách trong cụm (intracluster), cực đại hóa khoảng cách giữa cụm (intercluster).
9. **Tính khoảng cách Euclid giữa (1, 2, 3) và (4, 6, 3).** → 5.
10. **Với bảng 5 giao dịch slide 21, tính support và confidence của {Diaper, Milk} → {Beer}.**
    → support = 2/5 = 0,4; confidence = 2/3 ≈ 0,67. (Của {Milk} → {Coke}: 0,6 và 0,75.)
11. **Trong luật {Bagels} → {Potato Chips}, có thể dùng luật để làm gì?**
    → Chips ở consequent: biết làm gì để tăng doanh số chips; Bagels ở antecedent: biết sản phẩm nào bị ảnh hưởng nếu ngừng bán bagels; cả hai: nên bán gì kèm bagels để đẩy chips.
12. **Dự đoán doanh số theo chi phí quảng cáo là nhiệm vụ gì?** → Regression (biến đích liên tục).
13. **Kể 4–7 thách thức của data mining.** → Scalability, Dimensionality, Complex & Heterogeneous Data, Data Quality, Data Ownership & Distribution, Privacy Preservation, Streaming Data.
14. **Data mining bắt nguồn từ những lĩnh vực nào? Vì sao kỹ thuật truyền thống không đủ?**
    → ML/AI, pattern recognition, statistics, database systems. Vì dữ liệu khổng lồ, nhiều chiều, không đồng nhất & phân tán.
15. **Vì sao cần chuẩn hóa dữ liệu trước khi clustering bằng khoảng cách Euclid? (bổ sung, hay gặp trong TD)**
    → Thuộc tính có thang đo lớn (thu nhập) sẽ áp đảo thuộc tính thang đo nhỏ (tuổi) trong khoảng cách.

---

## 11. Tóm tắt cho tờ A4 (phần Intro — rất gọn)

- **DM** = trích xuất *non-trivial*, *implicit*, *previously unknown*, *potentially useful* info; tự động/bán tự động trên dữ liệu lớn → *patterns*.
- **KDD:** Selection → Preprocessing → Transformation → **DM** → Interpretation/Evaluation → Knowledge.
- **Không phải DM:** query (tra danh bạ, search "Amazon"). **Là DM:** gom nhóm tài liệu, tìm quy luật họ–vùng.
- Gốc: Stats/AI ∩ ML/Pattern Recognition ∩ Databases. Lý do mới: dữ liệu lớn, nhiều chiều, không đồng nhất/phân tán.
- **Predictive:** Classification, Regression, Deviation Detection. **Descriptive:** Clustering, Association Rules, Sequential Patterns.
- **Classification:** training set (attributes + 1 class) → model $y = f(x_1..x_d)$; test set đo accuracy $= \frac{\#\text{đúng}}{\#\text{test}}$. VD: direct marketing, fraud, churn, sky survey (star/galaxy).
- **Regression:** đích **liên tục**, mô hình tuyến tính/phi tuyến.
- **Anomaly detection:** độ lệch đáng kể so với bình thường (fraud, intrusion).
- **Clustering:** intra-cluster distance ↓, inter-cluster distance ↑. Euclid: $d(x,y) = \sqrt{\sum_k (x_k - y_k)^2}$ → **chuẩn hóa trước!**
- **Association rule** $X \to Y$ (antecedent → consequent): $s = \sigma(X\cup Y)/N$, $c = \sigma(X\cup Y)/\sigma(X)$. Co-occurrence ≠ causality.
- **Thách thức:** Scalability, Dimensionality, Heterogeneous data, Data quality, Ownership/Distribution, Privacy, Streaming.
- **Thi:** 50 % interro giấy 2/12 (1 A4 viết tay 2 mặt) + 50 % 3 TD máy (cá nhân/binôme).


---

# Chương 8 – Phân tích cụm (Cluster Analysis) — Phần A (slide 25 → 42)

> Phạm vi: định nghĩa phân cụm, ứng dụng, những gì *không phải* phân cụm, tính mơ hồ của khái niệm cụm, các loại phép phân cụm (types of clusterings), các loại cụm (types of clusters), danh sách thuật toán, và **thuật toán K-means cơ bản** (slide 42).
> Chi tiết K-means (slide 43 trở đi: khởi tạo, SSE, độ phức tạp, hạn chế…) do phần khác phụ trách; ở đây chỉ nhắc ngắn khi cần để hiểu slide 42.
> Ký hiệu **(bổ sung)** = kiến thức thêm ngoài slide (thường lấy từ sách Tan–Steinbach–Kumar), không có nguyên văn trên slide.

---

## 0. Slide 25 – Mục lục

Slide 25 chỉ là trang chuyển chương: khóa học gồm 4 phần (1) Introduction (Ch 1), **(2) Cluster Analysis (Ch 8)** ← đang học, (3) Association Analysis (Ch 6), (4) Classification (Ch 4).

Lưu ý: số chương theo sách Tan–Steinbach–Kumar (2006). Trong sách, Ch 8 = "Cluster Analysis: Basic Concepts and Algorithms".

---

## 1. Phân tích cụm là gì? (slide 26)

### Nội dung slide
> "Finding groups of objects such that the objects in a group will be similar (or related) to one another and different from (or unrelated to) the objects in other groups."

Hình vẽ: 3 nhóm điểm trong không gian 3D, kèm hai chú thích:
- **Intra-cluster distances are minimized**: khoảng cách *trong cùng một cụm* được làm **nhỏ nhất**.
- **Inter-cluster distances are maximized**: khoảng cách *giữa các cụm khác nhau* được làm **lớn nhất**.

### Giải thích
**Phân cụm (clustering / partitionnement / classification non supervisée)** là việc chia một tập đối tượng thành các nhóm (**cụm – cluster**) sao cho:
1. **Độ gắn kết nội cụm (cohesion / compactness)** cao: các đối tượng trong cùng một cụm giống nhau (gần nhau).
2. **Độ tách biệt giữa các cụm (separation)** cao: các đối tượng ở những cụm khác nhau thì khác nhau (xa nhau).

Đây là bài toán **học không giám sát (unsupervised learning)**: dữ liệu **không có nhãn lớp (class label)**. Thuật toán chỉ nhìn vào bản thân dữ liệu (thường qua một **độ đo khoảng cách / độ tương đồng – distance / similarity measure**) để tìm cấu trúc nhóm.

- "Intra" = bên trong (*intra-cluster* = trong một cụm).
- "Inter" = giữa (*inter-cluster* = giữa các cụm).
→ Mẹo nhớ: **intra nhỏ, inter lớn**.

### Ví dụ trực quan
Bạn đổ một túi kẹo nhiều màu ra bàn, không ai bảo bạn có bao nhiêu loại. Bạn tự gom các viên giống nhau (cùng màu, cùng kích thước) thành đống. Mỗi đống là một cụm: trong đống thì giống nhau (intra nhỏ), giữa các đống thì khác nhau (inter lớn).

### Ví dụ số nhỏ
Điểm 1D: {1, 2, 3, 10, 11, 12}. Phân cụm tự nhiên: {1,2,3} và {10,11,12}.
- Khoảng cách lớn nhất trong cụm: |3−1| = 2 (nhỏ).
- Khoảng cách nhỏ nhất giữa hai cụm: |10−3| = 7 (lớn).
Nếu thay bằng {1,2,10} và {3,11,12} thì trong cụm 1 có khoảng cách |10−1| = 9 → kém hơn hẳn.

### Phân tích sâu / đánh giá
- Hai tiêu chí "intra nhỏ" và "inter lớn" **có thể mâu thuẫn**: nếu cho mỗi điểm thành một cụm riêng thì intra = 0 (hoàn hảo) nhưng vô nghĩa. Vì vậy hầu hết thuật toán **cố định số cụm K** hoặc dùng tiêu chí cân bằng. **(bổ sung)**
- Kết quả phụ thuộc mạnh vào **định nghĩa "giống nhau"** (Euclid, cosine, Jaccard…) và việc **chuẩn hóa thuộc tính (normalisation)**: nếu một thuộc tính có thang đo lớn (vd. thu nhập tính bằng €) nó sẽ "lấn át" thuộc tính thang nhỏ (vd. tuổi). **(bổ sung)**

---

## 2. Ứng dụng của phân tích cụm (slide 27)

Slide chia thành hai mục đích chính:

### 2.1 Understanding – Hiểu dữ liệu
> "Group related documents for browsing, group genes and proteins that have similar functionality, or group stocks with similar price fluctuations."

- Gom **tài liệu (documents)** liên quan để duyệt (vd. kết quả tìm kiếm được gom theo chủ đề).
- Gom **gen / protein** có chức năng tương tự (sinh học).
- Gom **cổ phiếu (stocks)** có biến động giá tương tự.

Bảng trên slide ("Discovered Clusters" / "Industry Group") là kết quả phân cụm cổ phiếu theo biến động UP/DOWN trong ngày:

| # | Ví dụ cổ phiếu trong cụm (đọc được trên slide) | Industry Group |
|---|---|---|
| 1 | Applied-Matl-DOWN, Bay-Network-Down, 3-COM-DOWN, Cabletron-Sys-DOWN, CISCO-DOWN, HP-DOWN, DSC-Comm-DOWN, INTEL-DOWN, LSI-Logic-DOWN, Micron-Tech-DOWN, Texas-Inst-Down, Tellabs-Inc-Down, Natl-Semiconduct-DOWN, Oracl-DOWN, SGI-DOWN, Sun-DOWN | **Technology1-DOWN** |
| 2 | Apple-Comp-DOWN, Autodesk-DOWN, DEC-DOWN, ADV-Micro-Device-DOWN, Andrew-Corp-DOWN, Computer-Assoc-DOWN, Circuit-City-DOWN, Compaq-DOWN, EMC-Corp-DOWN, Gen-Inst-DOWN, Motorola-DOWN, Microsoft-DOWN, Scientific-Atl-DOWN | **Technology2-DOWN** |
| 3 | Fannie-Mae-DOWN, Fed-Home-Loan-DOWN, MBNA-Corp-DOWN, Morgan-Stanley-DOWN | **Financial-DOWN** |
| 4 | Baker-Hughes-UP, Dresser-Inds-UP, Halliburton-HLD-UP, Louisiana-Land-UP, Phillips-Petro-UP, Unocal-UP, Schlumberger-UP | **Oil-UP** |

(Chữ trên slide rất nhỏ; tên cổ phiếu ở trên là đọc gần đúng, ý chính là cột "Industry Group".)

**Điều thú vị**: thuật toán **không hề biết ngành nghề** của các công ty. Nó chỉ thấy chuỗi giá tăng/giảm. Vậy mà các cụm tìm ra lại trùng với ngành (công nghệ, tài chính, dầu khí). → Phân cụm giúp **phát hiện cấu trúc ẩn** có ý nghĩa.

### 2.2 Summarization – Tóm tắt dữ liệu
> "Reduce the size of large data sets."

Hình: **Clustering precipitation in Australia** – bản đồ Úc tô màu theo cụm lượng mưa. Thay vì lưu chuỗi lượng mưa của hàng nghìn điểm đo, ta chỉ cần lưu vài cụm (mỗi cụm đại diện bởi một "tâm"). → **Nén / giảm kích thước dữ liệu**.

Ví dụ trực quan: thay vì mô tả 10 000 khách hàng, công ty chỉ mô tả 5 "chân dung khách hàng" (5 tâm cụm).

### Phân tích sâu
- Ứng dụng khác **(bổ sung)**: phân khúc khách hàng (customer segmentation), nén ảnh / lượng tử hóa màu (vector quantization – mỗi pixel thay bằng màu tâm cụm), tiền xử lý cho thuật toán khác, phát hiện ngoại lai (outlier = điểm xa mọi cụm).
- "Summarization" liên quan trực tiếp đến K-means: mỗi cụm được **tóm tắt bằng centroid** → đó là lý do SSE (sai số khi thay điểm bằng centroid) là thước đo tự nhiên.

---

## 3. Những gì KHÔNG phải là phân tích cụm (slide 28)

| Không phải clustering | Vì sao |
|---|---|
| **Supervised classification** (phân lớp có giám sát) | Đã **có nhãn lớp (class label)**. Clustering thì không có nhãn. |
| **Simple segmentation** (phân đoạn đơn giản) | Ví dụ: chia sinh viên vào các nhóm đăng ký **theo thứ tự chữ cái của họ**. Quy tắc định sẵn, không dựa trên độ tương đồng của dữ liệu. |
| **Results of a query** (kết quả truy vấn) | Nhóm được tạo ra bởi **đặc tả bên ngoài (external specification)**, vd. `SELECT … WHERE ville='Bourges'`. Không "khám phá" được gì. |
| **Graph partitioning** (phân hoạch đồ thị) | "Some mutual relevance and synergy, but areas are not identical": có liên quan và bổ trợ lẫn nhau với clustering nhưng **không đồng nhất**. |

### Giải thích
Điểm chung: phân tích cụm là **khám phá nhóm từ chính dữ liệu dựa trên độ tương đồng**, không dùng nhãn có sẵn và không dùng quy tắc chia nhóm áp đặt từ ngoài.
- Classification: "Đây là ảnh mèo, đây là ảnh chó, hãy học phân biệt" → có giám sát.
- Clustering: "Đây là 1000 ảnh, hãy tự chia thành các nhóm giống nhau" → không giám sát.
- Graph partitioning (vd. cắt đồ thị thành các phần có ít cạnh nối nhau – min-cut) dùng kỹ thuật gần giống clustering (một số thuật toán clustering như spectral clustering dùng nó), nhưng mục tiêu và đầu vào khác (đồ thị cho sẵn, thường ràng buộc kích thước phần). Slide chỉ nói "không đồng nhất", không nói rõ hơn. **(phần giải thích về min-cut/spectral là bổ sung)**

---

## 4. Khái niệm "cụm" có thể mơ hồ (slide 29)

### Nội dung slide
Cùng một tập ~20 điểm đen ("How many clusters?") được tô màu theo 3 cách:
- **Two Clusters** (hình vuông đỏ / tam giác xanh): chia trái – phải.
- **Four Clusters**: mỗi nửa lại chia thành trên – dưới.
- **Six Clusters**: chia mịn hơn nữa.

### Giải thích
**Không có "đáp án đúng" duy nhất** cho số cụm. Cả 2, 4 hay 6 cụm đều hợp lý tùy **mức độ chi tiết (granularity)** và **mục đích sử dụng**.

Ví dụ: phân cụm động vật → 2 cụm (động vật có xương sống / không xương sống), 4 cụm, hay 6 cụm (thú, chim, cá, …) đều đúng ở những mức khác nhau.

### Phân tích sâu
- Đây là lý do K-means **bắt người dùng chọn K** (slide 42), và cũng là lý do **phân cụm phân cấp (hierarchical)** hữu ích: nó cho tất cả các mức (2, 4, 6…) cùng lúc trong một cây.
- Đánh giá cụm (cluster validity) là khó vì không có ground truth. Các phần sau của chương có các chỉ số đánh giá. **(bổ sung)**
- Bẫy: trong đề thi, nếu hỏi "tập điểm này có bao nhiêu cụm?" → nên trả lời "tùy định nghĩa cụm / mức chi tiết", rồi biện luận.

---

## 5. Các loại phép phân cụm – Types of Clusterings (slide 30–33)

### 5.1 Định nghĩa (slide 30)
- **A clustering is a set of clusters**: một *phép phân cụm (clustering)* là **một tập hợp các cụm**. (Phân biệt: *cluster* = một cụm; *clustering* = toàn bộ kết quả chia cụm.)
- Phân biệt quan trọng: **hierarchical** (phân cấp) vs **partitional** (phân hoạch).

**Partitional Clustering (phân cụm phân hoạch)**:
> "A division of data objects into non-overlapping subsets (clusters) such that each data object is in exactly one subset."

→ Chia dữ liệu thành các tập con **không giao nhau**, **mỗi đối tượng thuộc đúng một tập con**.
Về mặt toán học **(bổ sung, cách viết hình thức)**: với tập dữ liệu $D$, một phân hoạch là $\{C_1,\dots,C_K\}$ thỏa
$$C_i \neq \emptyset,\quad C_i \cap C_j = \emptyset\ (i\neq j),\quad \bigcup_{i=1}^{K} C_i = D.$$

**Hierarchical Clustering (phân cụm phân cấp)**:
> "A set of nested clusters organized as a hierarchical tree."

→ Một tập các cụm **lồng nhau (nested)**, tổ chức thành **cây phân cấp**.

### 5.2 Partitional Clustering – hình minh họa (slide 31)
- Trên: các điểm gốc (Original Points) → chia thành **2 cụm** (2 elip).
- Dưới: 5 điểm thưa → được đặt chung trong **1 cụm** (một elip lớn).
Ý: mỗi điểm nằm trong **đúng một** elip; các elip không chồng nhau.

Ví dụ: {1,2,3,10,11,12} → {{1,2,3},{10,11,12}} là một phân hoạch. Kết quả {{1,2,3},{3,10,11,12}} **không** phải phân hoạch (điểm 3 thuộc 2 cụm).

### 5.3 Hierarchical Clustering – hình minh họa (slide 32)
Bốn hình:
1. **Traditional Hierarchical Clustering** (sơ đồ lồng nhau – nested cluster diagram): elip ngoài cùng chứa p1 và một elip chứa {p2, p3, p4}; trong đó lại có elip chứa {p3, p4}.
2. **Traditional Dendrogram** (cây dendrogram tương ứng): p3 và p4 nối với nhau trước (thấp nhất), sau đó p2 nhập vào {p3,p4}, cuối cùng p1 nhập vào → gốc là toàn bộ {p1,p2,p3,p4}.
3. **Non-traditional Hierarchical Clustering**: elip ngoài chứa hai elip con {p1, p2} và {p3, p4}.
4. **Non-traditional Dendrogram**: gốc tách thành 2 nhánh {p1,p2} và {p3,p4}.

**Dendrogram** = sơ đồ cây biểu diễn thứ tự gộp (hoặc tách) các cụm; lá là các điểm, mỗi nút trong là một cụm = hợp các lá bên dưới; chiều cao nút thường là khoảng cách tại lúc gộp **(bổ sung về ý nghĩa chiều cao)**.

**Cắt dendrogram** ở một độ cao → thu được một phép phân cụm phân hoạch. Ví dụ với dendrogram truyền thống:
- Cắt ngay dưới gốc → 2 cụm: {p1}, {p2,p3,p4}.
- Cắt thấp hơn → 3 cụm: {p1}, {p2}, {p3,p4}.
- Cắt ở đáy → 4 cụm đơn lẻ.
→ Một dendrogram chứa **nhiều phép phân hoạch lồng nhau** cùng lúc (liên hệ slide 29: 2/4/6 cụm).

**Ghi chú về "traditional" vs "non-traditional"**: slide **không định nghĩa** rõ hai từ này, chỉ đưa hình. Cách hiểu hợp lý: trường hợp "traditional" là cây nhị phân thu được bằng cách gộp lần lượt từng cặp cụm (kiểu agglomerative), mọi điểm cuối cùng là lá đơn; "non-traditional" là một cấu trúc lồng nhau khác (ở đây hai cụm con đặt ngang hàng, hai điểm trong mỗi cụm con có vẻ được treo cùng mức). Hình khá nhỏ nên không chắc chắn chi tiết độ cao; điểm cần nhớ cho thi: **phân cấp = cụm lồng nhau, biểu diễn bằng dendrogram hoặc sơ đồ cụm lồng nhau**.

### 5.4 Các phân biệt khác (slide 33)

| Cặp | Ý nghĩa | Ví dụ |
|---|---|---|
| **Exclusive vs non-exclusive** (độc quyền / không độc quyền) | Non-exclusive: một điểm **có thể thuộc nhiều cụm**. Dùng để biểu diễn đối tượng thuộc nhiều lớp hoặc **điểm biên ('border' points)**. | Một người vừa là "sinh viên" vừa là "nhân viên part-time" → thuộc 2 cụm. |
| **Fuzzy vs non-fuzzy** (mờ / không mờ) | Fuzzy: mỗi điểm thuộc **mọi cụm** với một **trọng số (weight) trong [0,1]**; **tổng trọng số = 1**. **Probabilistic clustering** (phân cụm xác suất) có đặc điểm tương tự. | Điểm x: $w_{x,1}=0.7,\ w_{x,2}=0.2,\ w_{x,3}=0.1$ (tổng = 1). |
| **Partial vs complete** (bộ phận / toàn bộ) | Partial: **chỉ phân cụm một phần dữ liệu** (bỏ qua nhiễu/ngoại lai). Complete: mọi điểm đều được gán. | DBSCAN để nhiễu ra ngoài (partial); K-means gán mọi điểm (complete). **(ví dụ thuật toán là bổ sung)** |
| **Heterogeneous vs homogeneous** (không đồng nhất / đồng nhất) | Heterogeneous: các cụm có **kích thước, hình dạng, mật độ rất khác nhau**. | Một cụm lớn thưa và một cụm nhỏ đặc. |

#### Ví dụ fuzzy (tính tay)
Ba điểm 1D: a = 0, b = 5, c = 10; hai cụm có tâm 0 và 10.
Phân cụm cứng (hard / non-fuzzy): b cách đều hai tâm → phải gán tùy ý vào 1 cụm.
Phân cụm mờ: b có trọng số (0.5, 0.5); a ≈ (1, 0); c ≈ (0, 1). Mỗi hàng có tổng = 1. → Mô hình hóa tốt các điểm "lưỡng lự" ở biên.
(Thuật toán cụ thể như Fuzzy C-means **(bổ sung)** không có trong slide này.)

### Phân tích sâu / đánh giá (5.x)
- **Partitional** ⇔ exclusive + complete + non-fuzzy (mỗi điểm đúng 1 cụm). K-means là đại diện tiêu biểu.
- **Hierarchical** cho nhiều mức chi tiết, không cần chọn K trước (nhưng phải chọn chỗ cắt); thường tốn hơn về tính toán (ví dụ agglomerative cổ điển là $O(n^2)$ bộ nhớ, $O(n^3)$ thời gian **(bổ sung)**).
- Fuzzy ≠ non-exclusive: non-exclusive là "thuộc **hẳn** nhiều cụm" (thuộc/không thuộc), fuzzy là "thuộc **một phần** vào **tất cả** các cụm" với trọng số tổng = 1.
- "Partial" hữu ích khi có nhiễu: ép mọi điểm vào cụm (complete) sẽ làm méo cụm (vd. ngoại lai kéo lệch centroid của K-means).

---

## 6. Các loại cụm – Types of Clusters (slide 34–40)

Slide 34 liệt kê 6 loại (6 *định nghĩa khác nhau* về thế nào là một cụm):
1. Well-separated clusters
2. Center-based clusters
3. Contiguous clusters
4. Density-based clusters
5. Property or Conceptual
6. Described by an Objective Function

> Quan trọng: "Types of **clusterings**" (mục 5) nói về **cấu trúc của kết quả** (phân cấp hay phân hoạch, mờ hay không…). "Types of **clusters**" (mục 6) nói về **định nghĩa/hình dạng của một cụm**. Đừng nhầm!

### 6.1 Well-separated (tách biệt rõ) – slide 35
> "A cluster is a set of points such that any point in a cluster is closer (or more similar) to every other point in the cluster than to any point not in the cluster."

Hình: **3 well-separated clusters** (3 hình tròn đỏ, xanh dương, xanh lá cách xa nhau).

**Hình thức hóa (bổ sung)**: với mọi $x, y \in C$ và mọi $z \notin C$: $d(x,y) < d(x,z)$.
Tương đương: **đường kính lớn nhất trong cụm < khoảng cách nhỏ nhất ra ngoài cụm**.

Ví dụ: {1,2,3} và {10,11,12}: khoảng cách trong cụm ≤ 2, khoảng cách ra ngoài ≥ 7 → well-separated. ✓
Phản ví dụ: {1,2,3,4,5,6} chia thành {1,2,3} và {4,5,6}: điểm 3 cách 1 là 2 nhưng cách 4 chỉ là 1 → **không** well-separated.

Đánh giá: định nghĩa **rất chặt** – chỉ thỏa khi dữ liệu thật sự tách biệt rõ; dữ liệu thực tế hiếm khi như vậy. Cụm có thể có hình dạng bất kỳ (không nhất thiết tròn) **(bổ sung)**.

### 6.2 Center-based (dựa trên tâm) – slide 36
> "A cluster is a set of objects such that an object in a cluster is closer (more similar) to the 'center' of a cluster, than to the center of any other cluster."
> "The center of a cluster is often a **centroid**, the average of all the points in the cluster, or a **medoid**, the most 'representative' point of a cluster."

Hình: **4 center-based clusters** – hình tròn đỏ và xanh dương **chạm nhau** nhưng vẫn là 2 cụm (vì mỗi điểm gần tâm cụm mình hơn); xanh lá và vàng cũng gần nhau.

**Centroid vs medoid:**
- **Centroid** = **trung bình** các điểm: $c = \frac{1}{|C|}\sum_{x\in C} x$. Có thể **không phải** là một điểm dữ liệu thật.
- **Medoid** = một **điểm thật trong cụm**, "đại diện nhất" (thường: tổng khoảng cách tới các điểm khác nhỏ nhất **(bổ sung)**). Dùng khi trung bình không có nghĩa (vd. dữ liệu phân loại – categorical) hoặc để bền vững hơn với ngoại lai.

**Ví dụ số**: cụm 1D {1, 2, 3, 10}.
- Centroid = (1+2+3+10)/4 = 4 → không phải điểm dữ liệu, và bị ngoại lai 10 kéo lệch.
- Medoid: tổng khoảng cách từ 1: 1+2+9=12; từ 2: 1+1+8=10; từ 3: 2+1+7=10; từ 10: 9+8+7=24 → medoid = 2 (hoặc 3, đồng hạng). Ít bị ngoại lai ảnh hưởng hơn.

Đánh giá: cụm dựa trên tâm có xu hướng **hình cầu/lồi (globular)** **(bổ sung)**. Đây chính là kiểu cụm mà **K-means** tìm (slide 42). K-medoids/PAM dùng medoid **(bổ sung)**.

### 6.3 Contiguity-based (liền kề / láng giềng gần nhất, bắc cầu) – slide 37
> "Contiguous Cluster (Nearest neighbor or Transitive): A cluster is a set of points such that a point in a cluster is closer (or more similar) to **one or more** other points in the cluster than to any point not in the cluster."

Khác với well-separated ("gần **mọi** điểm trong cụm"), ở đây chỉ cần gần **ít nhất một** điểm trong cụm → **tính bắc cầu (transitive)**: A gần B, B gần C ⇒ A, B, C cùng cụm dù A xa C.

Hình: **8 contiguous clusters**. Đếm (theo cách đọc hình):
- 3 đường cong hình chữ S đan nhau (đường nét đứt vàng-xanh, chấm xanh dương, nét đứt đỏ) → 3 cụm (mỗi đường là một chuỗi điểm liền kề).
- Hình chữ C màu hồng tím → 1 cụm (hình dạng không lồi vẫn OK).
- **Hai chấm xanh cyan nối bằng một đường thẳng** (một "cầu" điểm) → **1 cụm** (vì chuỗi điểm nối liền).
- **Hai hình tròn xanh dương chồng lên nhau** → **1 cụm** (liền nhau).
- Tròn xanh lá → 1 cụm; tròn vàng → 1 cụm.
Tổng: 3 + 1 + 1 + 1 + 1 + 1 = 8. ✓

**Ví dụ số**: điểm 1D {1, 2, 3, 4, 5, 20}, ngưỡng "gần" = 1.5. Chuỗi 1–2–3–4–5 nối liền (mỗi bước = 1) → một cụm dù 1 và 5 cách nhau 4; điểm 20 là cụm riêng.

Đánh giá:
- **Ưu**: bắt được cụm **hình dạng bất kỳ** (chữ S, chữ C, xoắn).
- **Nhược**: **nhạy với nhiễu** – một "cây cầu" vài điểm nhiễu đủ để **nối hai cụm khác nhau thành một** (đúng như 2 chấm cyan ở hình). Đây là **hiệu ứng chuỗi (chaining effect)**, đặc trưng của **single link (MIN)** trong phân cụm phân cấp **(liên hệ – bổ sung, chi tiết ở phần sau của chương)**.
- Định nghĩa này giống "thành phần liên thông (connected component)" của đồ thị láng giềng **(bổ sung)**.

### 6.4 Density-based (dựa trên mật độ) – slide 38
> "A cluster is a dense region of points, which is separated by low-density regions, from other regions of high density."
> "Used when the clusters are irregular or intertwined, and when noise and outliers are present."

Hình: nền rải đầy các chấm nhỏ thưa (**nhiễu – noise**), trên đó có **6 density-based clusters**:
- Chữ C hồng tím (1), chấm xanh đậm bên trong chữ C (1), chấm cyan (1) – lần này **không có cầu nối** (cầu bị coi là nhiễu, mật độ thấp) nên hai chấm tách riêng;
- Hai hình tròn xanh dương chồng nhau → **1 cụm** (vùng đặc liền nhau);
- Tròn xanh lá (1), tròn vàng (1).
Tổng: 6. Các chấm nền thưa **không thuộc cụm nào** → đây là phân cụm **partial** (liên hệ slide 33).

**So sánh slide 37 vs 38**: cùng bố cục, nhưng
- contiguity: cầu nối mảnh nối 2 chấm cyan thành **1 cụm** → 8 cụm;
- density: vùng thưa (cầu, nền) bị coi là nhiễu → chấm cyan và chấm xanh đậm là **2 cụm riêng**; tổng 6 cụm (do không còn 3 đường chữ S trong hình này – hình 38 không vẽ các đường chữ S).

**Ví dụ số (bổ sung, trực giác kiểu DBSCAN)**: 1D {1, 1.2, 1.4, 1.6, 5, 9, 9.1, 9.3}. Với bán kính 0.5, vùng quanh 1–1.6 đặc (nhiều hàng xóm), quanh 9–9.3 đặc, còn 5 đứng một mình (mật độ thấp) → 2 cụm + 1 nhiễu (5).

Đánh giá:
- **Ưu**: hình dạng bất kỳ, **chịu nhiễu/ngoại lai** tốt, không cần K.
- **Nhược**: khó khi các cụm có **mật độ khác nhau** (heterogeneous density), nhạy tham số (bán kính, số điểm tối thiểu); khó trong không gian nhiều chiều **(bổ sung)**. Thuật toán đại diện: **DBSCAN** (slide 41 nhắc "Density-based clustering").

### 6.5 Shared Property / Conceptual Clusters (cụm khái niệm) – slide 39
> "Finds clusters that share some common property or represent a particular concept."

Hình: **2 Overlapping Circles** – hai **vòng tròn (vành khuyên)** màu đỏ cam đan chéo nhau.

Giải thích: con người thấy ngay "hai chiếc nhẫn". Nhưng:
- Center-based thất bại: tâm hai vòng gần nhau, và điểm ở vùng giao nhau gần tâm nào cũng mơ hồ.
- Contiguity/density thất bại: hai vòng **chạm nhau** → bị nối thành 1 cụm.
- Chỉ khi biết **khái niệm "hình tròn"** (các điểm cùng nằm trên một đường tròn – thuộc tính chung) mới tách đúng được 2 cụm.

→ Cụm được định nghĩa bởi một **thuộc tính chung / khái niệm**, không chỉ bởi khoảng cách. Đây là loại khó nhất, cần thuật toán chuyên biệt (vd. mô hình hóa "điểm trên đường tròn", Hough transform **(bổ sung)**). Các điểm ở chỗ giao có thể thuộc cả 2 cụm → liên hệ **non-exclusive**.

### 6.6 Clusters defined by an Objective Function (theo hàm mục tiêu) – slide 40
Nội dung slide:
- "Finds clusters that **minimize or maximize an objective function**."
- "Enumerate all possible ways of dividing the points into clusters and evaluate the 'goodness' of each potential set of clusters by using the given objective function. (**NP Hard**)"
- "Can have **global or local** objectives."
  - "Hierarchical clustering algorithms typically have **local** objectives."
  - "Partitional algorithms typically have **global** objectives."
- "A variation of the global objective function approach is to **fit the data to a parameterized model**."
  - "Parameters for the model are determined from the data."
  - "**Mixture models** assume that the data is a 'mixture' of a number of statistical distributions."

#### Giải thích
Thay vì mô tả hình dạng cụm, ta định nghĩa một **con số đo độ tốt** của cả phép phân cụm, rồi tìm phép phân cụm **tối ưu** con số đó.

Ví dụ hàm mục tiêu kinh điển (K-means) **(công thức là bổ sung ở slide này; SSE được trình bày ở slide sau)**:
$$\text{SSE} = \sum_{i=1}^{K} \sum_{x \in C_i} \text{dist}(c_i, x)^2$$
- $K$: số cụm; $C_i$: cụm thứ $i$; $c_i$: centroid của $C_i$; $\text{dist}$: khoảng cách Euclid.
- SSE nhỏ ⇒ các điểm sát tâm ⇒ cụm chặt.

**Ví dụ số**: {1,2,4,7,8,10}, K=2:
- Phân hoạch {1,2,4},{7,8,10}: tâm 7/3 và 25/3; SSE = 14/3 + 14/3 = **28/3 ≈ 9.33**.
- Phân hoạch {1,2},{4,7,8,10}: tâm 1.5 và 7.25; SSE = 0.5 + 18.75 = **19.25**.
→ Hàm mục tiêu nói phân hoạch thứ nhất tốt hơn.

#### Tại sao NP-hard?
"Liệt kê mọi cách chia": số cách chia $n$ điểm thành $K$ cụm khác rỗng là **số Stirling loại 2** $S(n,K) \approx \frac{K^n}{K!}$ **(bổ sung)**.
- $S(4,2) = 7$; $S(10,2) = 511$; $S(100, 5) \approx 6.6\times10^{67}$ → không thể vét cạn.
→ Thực tế dùng **heuristic / tối ưu cục bộ** (như K-means) – nhanh nhưng **không đảm bảo tối ưu toàn cục**.

#### Global vs local objective
- **Global** (toàn cục): một con số cho **cả phép phân cụm**, tối ưu tất cả cùng lúc → điển hình **partitional** (K-means tối thiểu hóa SSE tổng).
- **Local** (cục bộ): ở mỗi bước chỉ tối ưu một quyết định nhỏ (vd. "gộp hai cụm gần nhau nhất") → điển hình **hierarchical agglomerative**. Không có cam kết nào về tối ưu toàn cục; quyết định đã gộp thì không quay lại **(bổ sung)**.

#### Fit to a parameterized model / Mixture models
Giả định dữ liệu sinh ra từ một **mô hình có tham số**; tìm tham số khớp dữ liệu nhất. **Mixture model**: dữ liệu là "hỗn hợp" của nhiều phân phối thống kê, mỗi phân phối ↔ một cụm.
Ví dụ **(bổ sung)**: Gaussian Mixture Model (GMM) – dữ liệu chiều cao học sinh lớp 6 + học sinh lớp 12 = hỗn hợp 2 phân phối chuẩn $\mathcal{N}(\mu_1,\sigma_1^2)$, $\mathcal{N}(\mu_2,\sigma_2^2)$; ước lượng tham số bằng thuật toán **EM**. Kết quả tự nhiên là **xác suất thuộc cụm** → liên hệ "probabilistic clustering" (slide 33). K-means có thể xem như trường hợp đặc biệt "cứng" của GMM với phương sai bằng nhau **(bổ sung)**.

### Bảng tổng hợp 6 loại cụm

| Loại | Định nghĩa 1 dòng | Hình slide | Thuật toán liên quan **(bổ sung)** | Điểm yếu |
|---|---|---|---|---|
| Well-separated | Gần **mọi** điểm trong cụm hơn **mọi** điểm ngoài | 3 cụm | gần như mọi thuật toán làm tốt | Hiếm gặp trong thực tế |
| Center-based | Gần **tâm** cụm mình hơn tâm cụm khác (centroid/medoid) | 4 cụm | K-means, K-medoids | Chỉ cụm lồi/cầu |
| Contiguity | Gần **ít nhất một** điểm trong cụm (bắc cầu) | 8 cụm | Single link (MIN) | Cầu nhiễu nối cụm |
| Density-based | Vùng **đặc** tách bởi vùng **thưa** | 6 cụm | DBSCAN | Mật độ khác nhau |
| Conceptual | Chung **thuộc tính / khái niệm** | 2 vòng tròn | chuyên biệt | Khó tổng quát |
| Objective function | Tối ưu một **hàm mục tiêu** | – | K-means (SSE), GMM/EM | NP-hard → heuristic |

---

## 7. Các thuật toán phân cụm (slide 41)

Slide liệt kê 3 họ thuật toán sẽ học:
1. **K-means and its variants** (K-means và biến thể) – partitional, center-based, objective = SSE.
2. **Hierarchical clustering** (phân cụm phân cấp) – agglomerative/divisive, dendrogram.
3. **Density-based clustering** (phân cụm theo mật độ) – DBSCAN.

Liên kết với lý thuyết ở trên: mỗi họ thuật toán ứng với một định nghĩa cụm (center-based ↔ K-means; contiguity ↔ single-link hierarchical; density ↔ DBSCAN).

---

## 8. K-means (slide 42)

### 8.1 Nội dung slide
- **Partitional clustering approach** (phân hoạch).
- Each cluster is associated with a **centroid** (center point).
- Each point is assigned to the cluster with the **closest centroid**.
- **Number of clusters, K, must be specified** (phải chọn K trước).
- The basic algorithm is very simple:

```
1: Select K points as the initial centroids.
2: repeat
3:    Form K clusters by assigning all points to the closest centroid.
4:    Recompute the centroid of each cluster.
5: until The centroids don't change
```

### 8.2 Giải thích từng bước
1. **Khởi tạo (initialization)**: chọn K điểm làm centroid ban đầu (thường chọn ngẫu nhiên K điểm dữ liệu – slide 43).
2–5. **Lặp hai bước xen kẽ**:
   - **Bước gán (assignment step)** – dòng 3: mỗi điểm được gán cho centroid **gần nhất** → tạo ra K cụm.
   - **Bước cập nhật (update step)** – dòng 4: tính lại centroid mỗi cụm = **trung bình** các điểm trong cụm.
   - **Điều kiện dừng** – dòng 5: centroid **không đổi** (tương đương: không điểm nào đổi cụm).

### 8.3 Pseudocode chi tiết hơn (bổ sung, viết lại cho dễ code trong TD)
```
Input : D = {x_1..x_n} ⊂ R^d, số cụm K
Output: nhãn cụm label[1..n], centroid c_1..c_K

c_1..c_K ← K điểm chọn ngẫu nhiên trong D
repeat
    # Bước gán
    for each x_j in D:
        label[j] ← argmin_{i=1..K} ||x_j − c_i||²
    # Bước cập nhật
    for i = 1..K:
        C_i ← { x_j : label[j] = i }
        if C_i ≠ ∅: c_i ← (1/|C_i|) · Σ_{x ∈ C_i} x
        # (nếu C_i rỗng: cần xử lý riêng – xem slide sau / phần khác)
until không centroid nào thay đổi
```
Python (bổ sung, hữu ích cho TD):
```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=2, init="random", n_init=10, random_state=0).fit(X)
km.labels_, km.cluster_centers_, km.inertia_   # inertia_ = SSE
```

### 8.4 Hand-trace 1: dữ liệu 1D (minh họa nhiều vòng lặp)
Dữ liệu: **{1, 2, 4, 7, 8, 10}**, **K = 2**, khởi tạo (cố ý chọn tệ) **c1 = 1, c2 = 2**.

**Vòng 1 – gán**: so |x − 1| và |x − 2|

| x | d(x,c1=1) | d(x,c2=2) | Cụm |
|---|---|---|---|
| 1 | 0 | 1 | C1 |
| 2 | 1 | 0 | C2 |
| 4 | 3 | 2 | C2 |
| 7 | 6 | 5 | C2 |
| 8 | 7 | 6 | C2 |
| 10 | 9 | 8 | C2 |

C1 = {1}, C2 = {2,4,7,8,10}. **Cập nhật**: c1 = 1, c2 = 31/5 = **6.2**. (SSE = 40.8)

**Vòng 2 – gán** với c1 = 1, c2 = 6.2:
- 2: |2−1| = 1 < |2−6.2| = 4.2 → C1
- 4: |4−1| = 3 > |4−6.2| = 2.2 → C2
- 7, 8, 10 → C2
C1 = {1,2}, C2 = {4,7,8,10}. **Cập nhật**: c1 = 1.5, c2 = 29/4 = **7.25**. (SSE = 19.25)

**Vòng 3 – gán** với c1 = 1.5, c2 = 7.25:
- 4: |4−1.5| = 2.5 < |4−7.25| = 3.25 → **C1** (đổi cụm)
- 7: 5.5 vs 0.25 → C2
C1 = {1,2,4}, C2 = {7,8,10}. **Cập nhật**: c1 = 7/3 ≈ **2.33**, c2 = 25/3 ≈ **8.33**. (SSE = 28/3 ≈ 9.33)

**Vòng 4 – gán** với c1 ≈ 2.33, c2 ≈ 8.33:
- 4: 1.67 vs 4.33 → C1; 7: 4.67 vs 1.33 → C2. Không điểm nào đổi cụm → centroid không đổi → **DỪNG**.

Kết quả: {1,2,4}, {7,8,10}; SSE: 40.8 → 19.25 → 9.33 (**giảm đơn điệu** qua mỗi vòng).

Kiểm tra SSE cuối: cụm 1: $(1-\tfrac73)^2+(2-\tfrac73)^2+(4-\tfrac73)^2 = \tfrac{16}{9}+\tfrac19+\tfrac{25}{9} = \tfrac{42}{9}=\tfrac{14}{3}$; cụm 2 đối xứng $=\tfrac{14}{3}$; tổng $\tfrac{28}{3}\approx 9.33$.

### 8.5 Hand-trace 2: dữ liệu 2D
Điểm: A(1,1), B(1,2), C(2,1), D(5,4), E(6,5). **K = 2**, khởi tạo **c1 = A = (1,1), c2 = C = (2,1)**. Dùng **bình phương khoảng cách Euclid** (đủ để so sánh, khỏi khai căn).

**Vòng 1 – gán**

| Điểm | d²(·, c1=(1,1)) | d²(·, c2=(2,1)) | Cụm |
|---|---|---|---|
| A(1,1) | 0 | 1 | C1 |
| B(1,2) | 0+1 = 1 | 1+1 = 2 | C1 |
| C(2,1) | 1 | 0 | C2 |
| D(5,4) | 16+9 = 25 | 9+9 = 18 | C2 |
| E(6,5) | 25+16 = 41 | 16+16 = 32 | C2 |

**Cập nhật**: c1 = mean(A,B) = (1, 1.5); c2 = mean(C,D,E) = ((2+5+6)/3, (1+4+5)/3) = (4.33, 3.33).

**Vòng 2 – gán**

| Điểm | d²(·, c1=(1,1.5)) | d²(·, c2=(4.33,3.33)) | Cụm |
|---|---|---|---|
| A(1,1) | 0+0.25 = 0.25 | 11.11+5.44 = 16.56 | C1 |
| B(1,2) | 0.25 | 11.11+1.78 = 12.89 | C1 |
| C(2,1) | 1+0.25 = 1.25 | 5.44+5.44 = 10.89 | **C1** (đổi) |
| D(5,4) | 16+6.25 = 22.25 | 0.44+0.44 = 0.89 | C2 |
| E(6,5) | 25+12.25 = 37.25 | 2.78+2.78 = 5.56 | C2 |

**Cập nhật**: c1 = mean(A,B,C) = (4/3, 4/3) ≈ (1.33, 1.33); c2 = mean(D,E) = (5.5, 4.5).

**Vòng 3 – gán**: A: 0.22; B: 0.56; C: 0.56 (đều rất nhỏ so với c2 ≥ 24) → C1. D: 0.5; E: 0.5 tới c2 → C2. Không đổi → **DỪNG**.

Kết quả: {A,B,C}, {D,E}. SSE = (0.22 + 0.56 + 0.56) + (0.5 + 0.5) = 4/3 + 1 = **7/3 ≈ 2.33**.

### 8.6 Hand-trace 3: khởi tạo khác → kết quả khác (cực tiểu địa phương)
Dữ liệu {0, 4, 6, 10}, K = 2.
- Khởi tạo c1 = 0, c2 = 6 → gán: 0→C1; 4: |4−0|=4 > |4−6|=2 → C2; 6, 10 → C2. Cập nhật c1 = 0, c2 = 20/3 ≈ 6.67. Gán lại: 4: 4 vs 2.67 → vẫn C2 → **dừng** ở {0}, {4,6,10}, **SSE = 56/3 ≈ 18.67**.
- Khởi tạo c1 = 0, c2 = 10 → gán: 4 → C1 (4 < 6), 6 → C2 (6 > 4) → {0,4},{6,10}, tâm 2 và 8, ổn định, **SSE = 16**.
→ Cùng dữ liệu, cùng K, **hai kết quả khác nhau**; cái đầu là **cực tiểu địa phương (local minimum)**, không phải tối ưu toàn cục. Đây chính là ý của slide 43: "Clusters produced vary from one run to another". Cách khắc phục: chạy nhiều lần lấy SSE nhỏ nhất, K-means++ … **(bổ sung; chi tiết ở phần sau)**.

### 8.7 Phân tích sâu / đánh giá K-means (phần liên quan slide 42)
- **Vì sao hội tụ? (bổ sung)** Mỗi bước không làm tăng SSE: bước gán chọn tâm gần nhất cho từng điểm (SSE giảm hoặc giữ nguyên); bước cập nhật lấy trung bình – trung bình là điểm làm **tổng bình phương khoảng cách nhỏ nhất** ($\frac{\partial}{\partial c}\sum (x-c)^2 = 0 \Rightarrow c = \bar{x}$). Số phân hoạch hữu hạn + SSE giảm đơn điệu ⇒ phải dừng. Nhưng chỉ dừng ở **cực tiểu địa phương**.
- **Độ phức tạp** (slide 43, nhắc lại): $O(n \cdot K \cdot I \cdot d)$ với $n$ số điểm, $K$ số cụm, $I$ số vòng lặp, $d$ số thuộc tính → **tuyến tính theo n**, rất nhanh, phù hợp dữ liệu lớn. Phần lớn sự hội tụ xảy ra ở vài vòng đầu; thực tế hay đổi điều kiện dừng thành "cho tới khi tương đối ít điểm đổi cụm".
- **Ưu điểm**: đơn giản, nhanh, dễ cài đặt, kết quả dễ diễn giải (mỗi cụm = 1 centroid → summarization).
- **Nhược điểm / trường hợp thất bại (bổ sung, phần sau sẽ trình bày)**:
  - Phải **chọn K trước** (mà slide 29 cho thấy K có thể mơ hồ).
  - **Phụ thuộc khởi tạo** → cực tiểu địa phương (ví dụ 8.6).
  - Chỉ tìm cụm **center-based / hình cầu**, khó với cụm **kích thước khác nhau, mật độ khác nhau, hình không lồi** (chữ C, chữ S, 2 vòng tròn ở slide 37–39).
  - **Nhạy ngoại lai** (centroid = trung bình bị kéo lệch; xem ví dụ {1,2,3,10} ở 6.2).
  - Có thể xuất hiện **cụm rỗng (empty cluster)**.
  - Cần trung bình có nghĩa → dữ liệu số; với dữ liệu phân loại cần biến thể (K-modes / K-medoids).
  - Cần **chuẩn hóa** thuộc tính vì dùng khoảng cách Euclid.
- **Kết nối**: K-means = partitional + exclusive + complete + center-based + objective function (SSE, global). Biến thể: K-medoids (medoid), Bisecting K-means, Fuzzy C-means, GMM/EM (bản "mềm").

---

## 9. Dễ nhầm lẫn

1. **Clustering vs Classification**: clustering = không giám sát, không nhãn; classification = có giám sát, có nhãn (slide 28). Trong tiếng Pháp, "classification non supervisée" = clustering, còn "classification supervisée" = classification. Đừng nhầm chữ "classification".
2. **Cluster vs Clustering**: *cluster* = một cụm; *clustering* = tập hợp các cụm (slide 30).
3. **Types of clusterings vs types of clusters**: cái trước là cấu trúc kết quả (hierarchical/partitional, fuzzy, partial…), cái sau là định nghĩa một cụm (well-separated, center-based…).
4. **Intra vs inter**: intra = trong cụm (muốn **nhỏ**), inter = giữa cụm (muốn **lớn**).
5. **Well-separated vs contiguity**: well-separated: gần **mọi** điểm trong cụm; contiguity: gần **ít nhất một** điểm trong cụm (bắc cầu).
6. **Contiguity vs density**: contiguity nối mọi chuỗi điểm (kể cả cầu nhiễu mảnh) → 8 cụm ở slide 37; density bỏ vùng thưa → 6 cụm ở slide 38 (2 chấm tách riêng, nhiễu không thuộc cụm nào).
7. **Centroid vs medoid**: centroid = trung bình, có thể không phải điểm thật; medoid = điểm thật đại diện nhất.
8. **Fuzzy vs non-exclusive**: fuzzy = trọng số trong [0,1], tổng = 1, thuộc tất cả các cụm; non-exclusive = thuộc trọn vẹn nhiều cụm.
9. **Partial vs complete**: partial cho phép điểm không thuộc cụm nào (nhiễu).
10. **Global vs local objective**: partitional ↔ global; hierarchical ↔ local (slide 40) – dễ đảo ngược khi thi!
11. **Điều kiện dừng K-means**: "centroids don't change" (không phải "SSE = 0"). SSE = 0 chỉ khi mỗi điểm trùng centroid.
12. **K-means hội tụ ≠ tối ưu toàn cục**: hội tụ được đảm bảo (với các độ đo thông dụng), nhưng thường chỉ tới cực tiểu địa phương; bài toán tối ưu toàn cục là NP-hard.
13. Trong bước gán, dùng **d²** hay **d** đều cho cùng kết quả (hàm đơn điệu); nhưng **SSE dùng d²**.

---

## 10. Câu hỏi có thể ra thi (kèm lời giải ngắn)

**Q1.** Định nghĩa phân tích cụm. Nêu hai tiêu chí của một phép phân cụm tốt.
→ Tìm nhóm đối tượng sao cho đối tượng trong cùng nhóm giống nhau và khác với đối tượng nhóm khác. Tiêu chí: khoảng cách intra-cluster nhỏ nhất, inter-cluster lớn nhất (slide 26).

**Q2.** Những ví dụ sau có phải là clustering không? (a) Chia sinh viên theo chữ cái đầu của họ; (b) Phân nhóm email spam/không spam từ tập đã gán nhãn; (c) Nhóm khách hàng theo hành vi mua hàng mà không có nhãn; (d) Lấy các khách hàng ở Bourges bằng truy vấn SQL.
→ (a) Không – simple segmentation; (b) Không – supervised classification; (c) Có; (d) Không – result of a query (external specification).

**Q3.** Phân biệt partitional và hierarchical clustering. Cho dendrogram truyền thống của slide 32, liệt kê các phân hoạch thu được khi cắt.
→ Partitional: tập con không giao, mỗi điểm đúng 1 cụm. Hierarchical: cụm lồng nhau dạng cây. Cắt: {p1,p2,p3,p4}; {p1},{p2,p3,p4}; {p1},{p2},{p3,p4}; {p1},{p2},{p3},{p4}.

**Q4.** Phân biệt fuzzy và non-exclusive clustering. Ma trận thành viên sau có hợp lệ cho fuzzy clustering không: x1: (0.6, 0.5), x2: (0.3, 0.7)?
→ x1 có tổng 1.1 ≠ 1 → **không hợp lệ**; x2 hợp lệ.

**Q5.** Kể tên 6 loại cụm và cho biết loại nào K-means tìm được tốt.
→ Well-separated, center-based, contiguous, density-based, conceptual, objective function. K-means: center-based (và well-separated hình cầu); tối ưu hàm mục tiêu SSE.

**Q6.** Giải thích tại sao ở slide 37 có 8 cụm nhưng ở slide 38 có 6 cụm.
→ Contiguity: hai chấm cyan nối bằng một chuỗi điểm → 1 cụm; 3 đường chữ S → 3 cụm. Density: chuỗi nối và nền là vùng mật độ thấp → nhiễu; hai chấm nhỏ thành 2 cụm riêng; hình 38 không có các đường chữ S. Hai tròn xanh dương chồng nhau là 1 cụm trong cả hai định nghĩa.

**Q7.** Vì sao tìm phân cụm tối ưu theo hàm mục tiêu là NP-hard? Thực tế làm thế nào?
→ Phải liệt kê mọi cách chia (số lượng ~ $K^n/K!$, bùng nổ tổ hợp). Thực tế dùng heuristic lặp như K-means → chỉ đạt cực tiểu địa phương; chạy nhiều lần với khởi tạo khác nhau.

**Q8.** Hierarchical dùng hàm mục tiêu global hay local? Partitional thì sao?
→ Hierarchical: thường local; partitional: thường global (slide 40).

**Q9.** (Bài tính) Chạy K-means trên {2, 3, 6, 9, 10, 14}, K = 2, centroid khởi tạo 2 và 3. Cho kết quả từng vòng và SSE cuối.
→ V1: c1=2, c2=3: 2→C1; 3,6,9,10,14→C2 (vì gần 3 hơn). c1 = 2, c2 = 42/5 = 8.4.
V2: 3: |3−2|=1 < 5.4 → C1; 6: 4 vs 2.4 → C2; 9,10,14 → C2. C1={2,3}, C2={6,9,10,14}; c1 = 2.5, c2 = 39/4 = 9.75.
V3: 6: |6−2.5|=3.5 < |6−9.75|=3.75 → **C1**. C1={2,3,6}, C2={9,10,14}; c1 = 11/3 ≈ 3.67, c2 = 11.
V4: 6: 2.33 vs 5 → C1; 9: 5.33 vs 2 → C2. Không đổi → dừng.
SSE = [(2−3.67)² + (3−3.67)² + (6−3.67)²] + [(9−11)² + (10−11)² + (14−11)²] = (2.78 + 0.44 + 5.44) + (4 + 1 + 9) = 8.67 + 14 = **22.67** (chính xác: 26/3 + 14 = 68/3).

**Q10.** (Bài tính 2D) A(0,0), B(0,1), C(4,4), D(5,4), K = 2, khởi tạo c1 = A, c2 = B. Kết quả?
→ V1: A→c1 (0 vs 1); B→c2; C: d²(c1)=32, d²(c2)=16+9=25 → c2; D: 41 vs 34 → c2. c1=(0,0), c2=((0+4+5)/3,(1+4+4)/3)=(3,3).
V2: B(0,1): d²(c1)=1, d²(c2)=9+4=13 → c1; C: 32 vs 2 → c2; D: 41 vs 5 → c2. c1=(0,0.5), c2=(4.5,4).
V3: không đổi → dừng. Cụm {A,B},{C,D}; SSE = (0.25+0.25)+(0.25+0.25) = **1**.

**Q11.** Cho cụm {1, 2, 3, 10}: tính centroid và medoid. Cái nào bền với ngoại lai hơn?
→ Centroid = 4; medoid = 2 (hoặc 3, tổng khoảng cách = 10). Medoid bền hơn.

**Q12.** Nêu 3 nhược điểm của K-means cơ bản.
→ Phải chọn K; phụ thuộc khởi tạo (cực tiểu địa phương); chỉ hợp cụm hình cầu, kích thước/mật độ tương tự; nhạy ngoại lai; có thể có cụm rỗng.

**Q13.** Điều kiện dừng của K-means? Có chắc chắn dừng không? Có chắc tìm được SSE nhỏ nhất không?
→ Dừng khi centroid không đổi (hoặc ít điểm đổi cụm). Có, chắc chắn hội tụ (SSE không tăng, số phân hoạch hữu hạn). Không chắc tối ưu toàn cục (ví dụ {0,4,6,10}).

---

## 11. Tóm tắt cho tờ A4

- **Clustering** = nhóm đối tượng: giống trong nhóm, khác giữa nhóm. **Intra ↓, inter ↑**. Không giám sát (no labels).
- **Ứng dụng**: Understanding (documents, gènes, stocks) / Summarization (réduire la taille).
- **KHÔNG phải**: supervised classification (có nhãn), simple segmentation (theo chữ cái), query result (spec. externe), graph partitioning (liên quan nhưng khác).
- Số cụm **mơ hồ** (2/4/6 cụm cùng dữ liệu).
- **Clustering = set of clusters**. **Partitional**: tập con không giao, mỗi điểm đúng 1 cụm. **Hierarchical**: cụm lồng nhau, cây (**dendrogram**); cắt cây → phân hoạch.
- **Exclusive / non-exclusive** (1 điểm ∈ nhiều cụm, điểm biên). **Fuzzy**: $w_{ij}\in[0,1]$, $\sum_j w_{ij}=1$ (≈ probabilistic). **Partial / complete** (bỏ nhiễu hay không). **Heterogeneous / homogeneous** (size, shape, density).
- **6 loại cụm**:
  - Well-separated: gần **mọi** điểm cùng cụm hơn mọi điểm ngoài.
  - Center-based: gần **tâm** mình hơn tâm khác; **centroid** = mean, **medoid** = điểm thật đại diện nhất.
  - Contiguity (NN / transitive): gần **≥1** điểm cùng cụm; bắt hình bất kỳ; **cầu nhiễu nối cụm**.
  - Density: vùng **đặc** tách bởi vùng **thưa**; chịu nhiễu, hình bất kỳ (DBSCAN).
  - Conceptual: chung thuộc tính (2 vòng tròn giao nhau).
  - Objective function: min/max hàm mục tiêu; vét cạn **NP-hard**; **partitional ↔ global**, **hierarchical ↔ local**; biến thể: **mixture models** (fit model có tham số).
- **3 họ thuật toán**: K-means (+variants), Hierarchical, Density-based.
- **K-means**: partitional, centroid, chọn **K** trước.
  1. Chọn K centroid ban đầu. 2. repeat 3. gán mỗi điểm → centroid gần nhất. 4. tính lại centroid = mean. 5. until centroid không đổi.
- $\text{SSE}=\sum_{i=1}^K\sum_{x\in C_i} d(c_i,x)^2$, $c_i=\frac{1}{|C_i|}\sum_{x\in C_i}x$. SSE giảm đơn điệu → hội tụ, nhưng **cực tiểu địa phương** (phụ thuộc init: vd {0,4,6,10}: SSE 18.67 vs 16).
- Độ phức tạp $O(n\cdot K\cdot I\cdot d)$. Yếu: K, init, outliers, cụm không cầu / size-density khác, cụm rỗng, cần chuẩn hóa.


---

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


---

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


---

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


---

# Chương 6 — Phân tích luật kết hợp (Association Analysis) — slides 96–121

> Nguồn: Tan, Steinbach, Kumar, *Introduction to Data Mining* (2006), chương 6.
> Các số liệu trên slide và ví dụ tự soạn đều đã được **kiểm tra lại bằng máy** (script Python liệt kê toàn bộ tập mục).
> Phần ghi "(bổ sung)" là kiến thức ngoài slide.

---

## 0. Bức tranh tổng thể (đọc trước)

- **Bài toán:** có một cơ sở dữ liệu giao dịch (transaction database), mỗi giao dịch là một "giỏ hàng" gồm vài mặt hàng. Ta muốn tìm các **quy luật dạng "nếu mua X thì thường mua Y"**, ví dụ {Tã} → {Bia}.
- **Hai thước đo:** độ hỗ trợ (support) đo *mức độ phổ biến* của luật, độ tin cậy (confidence) đo *mức độ tin được* của luật.
- **Cách làm (slide 102):**
  1. Tìm tất cả **tập mục phổ biến (frequent itemsets)**, tức các tập có support ≥ minsup. Đây là bước tốn kém nhất, và **thuật toán Apriori** sinh ra để giải quyết nó.
  2. Từ mỗi tập mục phổ biến, **sinh luật (rule generation)** có confidence ≥ minconf.
- **Ý tưởng then chốt:** tính chất **đơn điệu ngược (anti-monotone)** của support: nếu một tập không phổ biến thì mọi tập cha của nó cũng không phổ biến. Nhờ vậy ta cắt tỉa (prune) được rất nhiều ứng viên.
- **Cách biểu diễn gọn:** tập mục phổ biến **cực đại (maximal)** và **đóng (closed)**.

---

## 1. Slide 96 — Mục lục

Slide chuyển chương: phần 3 của môn học là **Association Analysis (Ch 6)**, nằm sau Clustering (Ch 8) và trước Classification (Ch 4).

**Liên hệ (bổ sung):** Clustering và Association đều là **học không giám sát (unsupervised)**: không có nhãn lớp, ta tìm cấu trúc ẩn trong dữ liệu. Classification thì có giám sát (supervised).

---

## 2. Slide 97 — Khai phá luật kết hợp (Association Rule Mining)

**Định nghĩa trên slide:** cho một tập giao dịch, tìm các luật **dự đoán sự xuất hiện của một mục (item)** dựa trên sự xuất hiện của các mục khác trong cùng giao dịch.

**Bảng giao dịch giỏ hàng (Market-Basket transactions)**, được dùng xuyên suốt chương:

| TID | Items |
|---|---|
| 1 | Bread, Milk |
| 2 | Bread, Diaper, Beer, Eggs |
| 3 | Milk, Diaper, Beer, Coke |
| 4 | Bread, Milk, Diaper, Beer |
| 5 | Bread, Milk, Diaper, Coke |

(TID = Transaction ID; Bread = bánh mì, Milk = sữa, Diaper = tã, Beer = bia, Eggs = trứng, Coke = nước ngọt.)

**Ví dụ luật trên slide:**
- {Diaper} → {Beer}
- {Milk, Bread} → {Eggs, Coke}
- {Beer, Bread} → {Milk}

**Câu quan trọng trên slide: "Implication means co-occurrence, not causality!"**
Mũi tên "→" chỉ có nghĩa là **"hay xuất hiện cùng nhau"** (đồng xuất hiện, co-occurrence). Nó **không** có nghĩa là "gây ra" (quan hệ nhân quả, causality).
- Ví dụ: {Diaper} → {Beer} không có nghĩa là mua tã *khiến* người ta mua bia. Có thể có một nguyên nhân chung ẩn đằng sau (theo giai thoại: các ông bố trẻ đi mua tã tối thứ Sáu và tiện tay mua bia).
- Tương tự (bổ sung): "người mang ô" → "đường ướt" có tương quan mạnh, nhưng ô không làm ướt đường; mưa mới là nguyên nhân chung.

---

## 3. Slide 98 — Định nghĩa: Tập mục phổ biến (Frequent Itemset)

| Khái niệm | Định nghĩa | Ví dụ (bảng slide 97) |
|---|---|---|
| **Itemset** (tập mục) | Tập hợp gồm một hoặc nhiều mục | {Milk, Bread, Diaper} |
| **k-itemset** | Itemset có đúng k mục | {Milk, Bread, Diaper} là 3-itemset |
| **Support count** $\sigma$ (số đếm hỗ trợ) | **Số giao dịch** chứa itemset | $\sigma(\{Milk, Bread, Diaper\}) = 2$ |
| **Support** $s$ (độ hỗ trợ) | **Tỉ lệ** giao dịch chứa itemset | $s(\{Milk, Bread, Diaper\}) = 2/5$ |
| **Frequent itemset** | Itemset có support **≥ minsup** | Với minsup = 0.4, {Milk, Bread, Diaper} là phổ biến |

**Công thức:**
$$\sigma(X) = \big|\{\, t_i \in T \;:\; X \subseteq t_i \,\}\big|, \qquad s(X) = \frac{\sigma(X)}{|T|} = \frac{\sigma(X)}{N}$$

- $T$ là tập các giao dịch, $N = |T|$ là số giao dịch (ở đây $N=5$).
- $t_i$ là giao dịch thứ i (một tập các mục).
- $X \subseteq t_i$: giao dịch **chứa toàn bộ** các mục của X. Chứa một phần thì không tính.

**Kiểm tra lại:** {Milk, Bread, Diaper} xuất hiện ở T4 (Bread, Milk, Diaper, Beer) và T5 (Bread, Milk, Diaper, Coke). T2 có Bread và Diaper nhưng thiếu Milk; T3 có Milk và Diaper nhưng thiếu Bread. Vậy $\sigma = 2$ và $s = 2/5 = 0.4$. ✔

**Trực giác:** support trả lời câu hỏi "trong 100 hoá đơn, có bao nhiêu hoá đơn chứa đủ cả bộ này?".

**Lưu ý:** minsup có thể cho dưới dạng **tỉ lệ** (0.4 = 40%) hoặc **số đếm** (minsup count = 2). Quy đổi: $\text{minsup\_count} = \lceil \text{minsup} \times N \rceil$.

---

## 4. Slide 99 — Định nghĩa: Luật kết hợp (Association Rule)

**Luật kết hợp** là biểu thức kéo theo dạng $X \rightarrow Y$, trong đó X và Y là các itemset, và **$X \cap Y = \emptyset$** (bổ sung: điều kiện rời nhau có trong sách, slide không ghi rõ).
- X là **vế trái / tiền đề (antecedent, LHS)**, Y là **vế phải / hệ quả (consequent, RHS)**.
- Ví dụ: {Milk, Diaper} → {Beer}.

**Hai độ đo đánh giá luật (Rule Evaluation Metrics):**

$$\boxed{s(X\rightarrow Y) = \frac{\sigma(X \cup Y)}{N}} \qquad \boxed{c(X\rightarrow Y) = \frac{\sigma(X \cup Y)}{\sigma(X)}}$$

- **Support (s):** tỉ lệ giao dịch chứa **cả X và Y**. Nó cho biết luật có "đủ phổ biến" để đáng quan tâm hay không.
- **Confidence (c):** trong các giao dịch chứa X, có bao nhiêu phần cũng chứa Y. Đây chính là **xác suất có điều kiện** (bổ sung) $c = P(Y \mid X)$. Nó cho biết luật "đáng tin" đến đâu.

**Ví dụ trên slide:** {Milk, Diaper} ⇒ Beer
- $\sigma(\{Milk, Diaper, Beer\}) = 2$ (T3, T4), nên $s = 2/5 = 0.4$.
- $\sigma(\{Milk, Diaper\}) = 3$ (T3, T4, T5), nên $c = 2/3 \approx 0.67$.

**Lời đọc:** "40% số hoá đơn có cả sữa, tã và bia; trong các hoá đơn có sữa và tã thì 67% có bia."

⚠️ **Hay nhầm:** chữ $X \cup Y$ trong công thức có nghĩa là **giao dịch chứa tất cả mục của X và tất cả mục của Y** (hợp các *tập mục*), chứ **không phải** "giao dịch chứa X *hoặc* Y".

---

## 5. Slide 100 — Nhiệm vụ khai phá luật (Association Rule Mining Task)

**Mục tiêu:** cho tập giao dịch T, tìm **tất cả** các luật thoả đồng thời:
- support ≥ **minsup**
- confidence ≥ **minconf**

**Cách vét cạn (brute-force):**
1. Liệt kê mọi luật có thể có.
2. Tính support và confidence cho từng luật.
3. Loại các luật không đạt minsup hoặc minconf.

Kết luận trên slide: cách này **"Computationally prohibitive!"**, tức chi phí tính toán không chấp nhận được, vì số luật tăng theo hàm mũ (xem slide 105: với d = 6 mục đã có 602 luật).

---

## 6. Slide 101 — Quan sát quan trọng: tách support khỏi confidence

**Các luật ví dụ** (đã kiểm tra lại từng số):

| Luật | $\sigma(X\cup Y)$ | $\sigma(X)$ | s | c |
|---|---|---|---|---|
| {Milk, Diaper} → {Beer} | 2 | 3 | 0.4 | 2/3 = 0.67 |
| {Milk, Beer} → {Diaper} | 2 | 2 | 0.4 | 2/2 = 1.0 |
| {Diaper, Beer} → {Milk} | 2 | 3 | 0.4 | 0.67 |
| {Beer} → {Milk, Diaper} | 2 | 3 | 0.4 | 0.67 |
| {Diaper} → {Milk, Beer} | 2 | 4 | 0.4 | 0.5 |
| {Milk} → {Diaper, Beer} | 2 | 4 | 0.4 | 0.5 |

**Quan sát:**
1. Cả 6 luật đều là các **cách chia đôi (binary partitions)** của **cùng một itemset** {Milk, Diaper, Beer}.
2. Các luật sinh ra từ cùng một itemset có **support giống hệt nhau** (vì $X\cup Y$ luôn là cùng một tập), nhưng **confidence có thể khác nhau** (vì mẫu số $\sigma(X)$ thay đổi).
3. Vì vậy ta có thể **tách rời (decouple)** hai yêu cầu: trước hết lọc theo support ở mức **itemset**, sau đó mới xét confidence ở mức **luật**.

**Trực giác:** nếu {Milk, Diaper, Beer} không phổ biến thì *cả 6 luật* đều bị loại mà không cần tính confidence nào. Một phép kiểm tra trên itemset thay cho 6 phép kiểm tra trên luật.

---

## 7. Slide 102 — Cách tiếp cận hai bước (Two-step approach)

1. **Sinh tập mục phổ biến (Frequent Itemset Generation):** tìm mọi itemset có support ≥ minsup.
2. **Sinh luật (Rule Generation):** từ mỗi tập mục phổ biến, sinh các luật có confidence cao. Mỗi luật là **một cách chia đôi** của tập mục phổ biến đó.

Slide nhấn mạnh rằng **bước 1 vẫn rất tốn kém**. Phần lớn chương này bàn về cách làm bước 1 hiệu quả.

---

## 8. Slide 103 — Dàn tập mục (itemset lattice)

Hình vẽ là **dàn (lattice)** của mọi itemset trên 5 mục {A, B, C, D, E}:
- Tầng 0: `null` (tập rỗng)
- Tầng 1: A, B, C, D, E (5 tập)
- Tầng 2: AB, AC, …, DE (10 tập)
- Tầng 3: ABC, …, CDE (10 tập)
- Tầng 4: ABCD, …, BCDE (5 tập)
- Tầng 5: ABCDE (1 tập)

Mỗi cạnh nối một tập với tập cha "ngay trên" nó (thêm đúng 1 mục).

**Công thức:** với d mục, có **$2^d$ itemset ứng viên** (kể cả tập rỗng; bỏ tập rỗng thì còn $2^d - 1$).
- Ví dụ: d = 5 cho $2^5 = 32$ tập (= 1 + 5 + 10 + 10 + 5 + 1).
- Một siêu thị có d = 1000 mặt hàng cho $2^{1000}$ tập, không thể duyệt hết.

---

## 9. Slide 104 — Vét cạn để sinh tập phổ biến

- **Mỗi itemset trong dàn là một ứng viên (candidate)** có thể phổ biến.
- Để đếm support, ta quét CSDL và so khớp **mỗi giao dịch với mọi ứng viên**.
- Ký hiệu trên hình:
  - **N** = số giao dịch
  - **w** = độ rộng giao dịch (transaction width, tức số mục tối đa trong một giao dịch)
  - **M** = số ứng viên
- **Độ phức tạp $\approx O(NMw)$.** Con số này **đắt vì $M = 2^d$**.

**Trực giác:** giống như cầm danh sách 1 triệu "combo" và dò từng hoá đơn xem có chứa combo đó không.

---

## 10. Slide 105 — Độ phức tạp tính toán (Computational Complexity)

Với d mục phân biệt:
- Tổng số itemset: $2^d$.
- **Tổng số luật kết hợp có thể có:**
$$R = \sum_{k=1}^{d-1}\left[\binom{d}{k}\times\sum_{j=1}^{d-k}\binom{d-k}{j}\right] = 3^d - 2^{d+1} + 1$$

**Ý nghĩa các ký hiệu:**
- $k$ là số mục ở **vế trái** X. Có $\binom{d}{k}$ cách chọn X.
- $j$ là số mục ở **vế phải** Y, chọn trong $d-k$ mục còn lại. Có $\binom{d-k}{j}$ cách.
- Cả X và Y đều phải khác rỗng, nên $k \ge 1$ và $j \ge 1$.

**Vì sao bằng $3^d - 2^{d+1} + 1$ (bổ sung, chứng minh ngắn):** mỗi mục có 3 lựa chọn: vào X, vào Y, hoặc không dùng. Vậy có $3^d$ cách. Trừ các trường hợp X rỗng ($2^d$ cách) và Y rỗng ($2^d$ cách). Trường hợp cả hai rỗng (1 cách) bị trừ hai lần nên cộng lại 1. Kết quả: $3^d - 2\cdot 2^d + 1$.

**Ví dụ số:**
- d = 2: $9 - 8 + 1 = 2$ (A→B, B→A) ✔
- d = 3: $27 - 16 + 1 = 12$
- d = 6: $729 - 128 + 1 = \mathbf{602}$ luật (đúng như slide)

Đồ thị trên slide: số luật tăng theo hàm mũ, lên khoảng $5.7\times10^4$ khi d = 10 ($3^{10} - 2^{11} + 1 = 57\,002$).

---

## 11. Slide 106 — Các chiến lược sinh tập phổ biến

| Chiến lược | Ý tưởng | Kỹ thuật |
|---|---|---|
| **Giảm số ứng viên (M)** | Tìm kiếm đầy đủ thì $M = 2^d$ | Dùng kỹ thuật **cắt tỉa (pruning)**, chính là **Apriori** |
| **Giảm số giao dịch (N)** | Thu nhỏ N khi kích thước itemset tăng | Dùng trong **DHP** và các thuật toán **khai phá theo chiều dọc (vertical-based mining)** |
| **Giảm số phép so sánh (NM)** | Dùng **cấu trúc dữ liệu hiệu quả** để lưu ứng viên hoặc giao dịch | Không cần so mỗi ứng viên với mỗi giao dịch (ví dụ **cây băm, hash tree**, bổ sung) |

**Bổ sung:**
- **DHP** (Direct Hashing and Pruning): dùng bảng băm để loại sớm các cặp ứng viên.
- **Vertical mining** (ví dụ Eclat): lưu với mỗi mục **danh sách TID** chứa nó. Khi đó $\sigma(AB) = |TID(A)\cap TID(B)|$, không cần quét lại CSDL. Các số đỏ trên slide 115 chính là các danh sách TID này.
- **Hash tree:** chia các ứng viên vào các "ngăn" theo hàm băm. Mỗi giao dịch chỉ được so với ứng viên trong các ngăn liên quan.

---

## 12. Slide 107 — Nguyên lý Apriori (Apriori principle) ⭐

**Nguyên lý:** *Nếu một itemset là phổ biến thì mọi tập con của nó cũng phải phổ biến.*

**Dạng tương đương (contrapositive), là dạng thực sự dùng để cắt tỉa:** *nếu một itemset **không** phổ biến thì mọi **tập cha (superset)** của nó cũng **không** phổ biến.*

**Cơ sở toán học:** support có tính chất
$$\forall X, Y:\ (X \subseteq Y) \Rightarrow s(X) \ge s(Y)$$
- Support của một itemset **không bao giờ vượt quá** support của các tập con của nó.
- Đây là tính chất **đơn điệu ngược (anti-monotone)** của support.

**Chứng minh 1 dòng (bổ sung, nên thuộc):** nếu $X \subseteq Y$ thì mọi giao dịch chứa Y đều chứa X. Tập giao dịch chứa Y là tập con của tập giao dịch chứa X, nên $\sigma(Y) \le \sigma(X)$.

**Ví dụ:** $\sigma(\{Bread\}) = 4 \ge \sigma(\{Bread, Milk\}) = 3 \ge \sigma(\{Bread, Milk, Diaper\}) = 2$.

**Ẩn dụ:** muốn một *đội* 3 người cùng có mặt ở ≥ 3 buổi học, thì *mỗi cặp* trong đội phải cùng có mặt ở ≥ 3 buổi. Nếu cặp (An, Bình) chỉ cùng đi 2 buổi thì bất kỳ đội nào chứa cả An và Bình cũng không thể đạt 3 buổi.

---

## 13. Slide 108 — Minh hoạ nguyên lý Apriori trên dàn

- Trong hình, **AB được phát hiện là không phổ biến** ("Found to be Infrequent").
- Do đó **mọi tập cha của AB** bị **cắt tỉa (Pruned supersets)**: ABC, ABD, ABE, ABCD, ABCE, ABDE, ABCDE (vùng khoanh nét đứt đỏ, các nút tô xám).
- Ta loại ngay $2^{3} - 1 = 7$ tập mà không cần đếm (vì A, B đã cố định, 3 mục C, D, E còn lại mỗi mục có hoặc không, trừ trường hợp chính AB).

---

## 14. Slide 109 — Minh hoạ Apriori trên dữ liệu giỏ hàng (minsup count = 3)

**Bước 1: các 1-itemset (Items)**

| Item | Count | Phổ biến? |
|---|---|---|
| Bread | 4 | ✔ |
| Coke | 2 | ✘ |
| Milk | 4 | ✔ |
| Beer | 3 | ✔ |
| Diaper | 4 | ✔ |
| Eggs | 1 | ✘ |

**Bước 2: các 2-itemset (Pairs).** *"No need to generate candidates involving Coke or Eggs"*: ta không cần sinh ứng viên chứa Coke hay Eggs, vì chúng đã không phổ biến. Chỉ ghép 4 mục còn lại, được $\binom{4}{2} = 6$ cặp:

| Itemset | Count | TID (kiểm tra) | Phổ biến? |
|---|---|---|---|
| {Bread, Milk} | 3 | 1, 4, 5 | ✔ |
| {Bread, Beer} | 2 | 2, 4 | ✘ |
| {Bread, Diaper} | 3 | 2, 4, 5 | ✔ |
| {Milk, Beer} | 2 | 3, 4 | ✘ |
| {Milk, Diaper} | 3 | 3, 4, 5 | ✔ |
| {Beer, Diaper} | 3 | 2, 3, 4 | ✔ |

**Bước 3: các 3-itemset (Triplets).** Slide liệt kê một ứng viên duy nhất: **{Bread, Milk, Diaper}**. Đây là ứng viên duy nhất có cả 3 tập con 2 phần tử đều phổ biến. Các ứng viên khác chứa Beer đều có một cặp không phổ biến ({Bread, Beer} hoặc {Milk, Beer}), nên bị loại.

> ⚠️ **Lỗi trên slide:** slide ghi count của {Bread, Milk, Diaper} là **3**, nhưng đếm lại thì nó chỉ xuất hiện ở **T4 và T5**, tức **count = 2**. Con số này cũng khớp với slide 98, nơi ghi $\sigma(\{Milk, Bread, Diaper\}) = 2$. Vậy với minsup = 3, tập này **không phổ biến** và L3 = ∅. Đi thi, nếu đề dùng lại bảng này, **hãy tự đếm lại**.

**So sánh số ứng viên (có trên slide):**
- Xét mọi tập con có tối đa 3 phần tử: $\binom{6}{1} + \binom{6}{2} + \binom{6}{3} = 6 + 15 + 20 = 41$ ứng viên.
- Có cắt tỉa theo support: $6 + 6 + 1 = 13$ ứng viên (6 mục đơn, 6 cặp, 1 bộ ba).

Như vậy cắt tỉa giảm khoảng 3 lần số ứng viên ngay cả với dữ liệu nhỏ xíu này.

---

## 15. Slide 110 — Thuật toán Apriori ⭐⭐

**Nội dung trên slide (Method):**
- Đặt k = 1.
- Sinh các tập phổ biến độ dài 1.
- Lặp đến khi không còn tập phổ biến mới:
  - **Sinh** các ứng viên độ dài (k+1) từ các tập phổ biến độ dài k.
  - **Cắt tỉa** các ứng viên có chứa tập con độ dài k không phổ biến.
  - **Đếm** support của mỗi ứng viên bằng cách quét CSDL.
  - **Loại** các ứng viên không phổ biến, chỉ giữ lại các tập phổ biến.

### 15.1. Mã giả chi tiết

```
Apriori(T, minsup):
    // Ck = tập ứng viên (Candidates) kích thước k
    // Lk = tập phổ biến (Large/frequent) kích thước k
    k ← 1
    L1 ← { i ∈ I : σ(i) ≥ minsup }             // 1 lần quét CSDL
    while Lk ≠ ∅ :
        // (1) SINH ỨNG VIÊN — join Lk với Lk (bổ sung: phương pháp F(k-1)×F(k-1))
        Ck+1 ← ∅
        for mỗi cặp p, q ∈ Lk (đã sắp thứ tự từ điển) :
            if p và q giống nhau ở k-1 mục đầu và p[k] < q[k] :
                c ← p ∪ {q[k]}                    // ghép
                // (2) CẮT TỈA (Apriori pruning)
                if mọi tập con k phần tử của c đều thuộc Lk :
                    Ck+1 ← Ck+1 ∪ {c}
        // (3) ĐẾM SUPPORT — 1 lần quét CSDL
        for mỗi giao dịch t ∈ T :
            for mỗi ứng viên c ∈ Ck+1 với c ⊆ t :
                σ(c) ← σ(c) + 1
        // (4) LOẠI ứng viên không phổ biến
        Lk+1 ← { c ∈ Ck+1 : σ(c) ≥ minsup }
        k ← k + 1
    return ⋃ Lk
```

**Ghi chú:**
- Bước ghép (join) theo kiểu "giống nhau k−1 mục đầu" là phương pháp $F_{k-1}\times F_{k-1}$ trong sách (bổ sung). Slide chỉ nói "generate from length k frequent itemsets".
  - Ví dụ: {A,B} và {A,C} ghép thành {A,B,C}.
  - {A,B} và {B,C} **không** ghép với nhau vì mục đầu khác. {A,B,C} đã được sinh từ {A,B} và {A,C} rồi.
- Mỗi vòng lặp k tốn **1 lần quét CSDL**. Nếu tập phổ biến dài nhất có $k_{max}$ mục thì cần khoảng $k_{max}+1$ lần quét.
- Thuật toán duyệt dàn **theo chiều rộng, từng tầng một (level-wise, breadth-first)**, từ trên xuống.

### 15.2. ⭐ Ví dụ chạy tay đầy đủ (dạng bài thi)

**Đề bài:** CSDL gồm 6 giao dịch trên 5 mục {A, B, C, D, E}. Cho **minsup = 50%**, tức **minsup count = 0.5 × 6 = 3**, và **minconf = 75%**. Tìm mọi tập mục phổ biến và mọi luật mạnh.

| TID | Items |
|---|---|
| T1 | A, B, C |
| T2 | A, B, C, E |
| T3 | A, B, C, D |
| T4 | A, D, E |
| T5 | A, C, D |
| T6 | B, C, D |

#### Vòng k = 1: C1 → L1

| C1 | TID chứa nó | σ | ≥ 3? |
|---|---|---|---|
| {A} | 1, 2, 3, 4, 5 | 5 | ✔ |
| {B} | 1, 2, 3, 6 | 4 | ✔ |
| {C} | 1, 2, 3, 5, 6 | 5 | ✔ |
| {D} | 3, 4, 5, 6 | 4 | ✔ |
| {E} | 2, 4 | 2 | ✘ loại |

**L1 = { A:5, B:4, C:5, D:4 }**

#### Vòng k = 2: C2 → L2

- **Sinh:** ghép từng cặp trong L1 được $\binom{4}{2} = 6$ ứng viên. Không có ứng viên nào chứa E, vì E đã bị loại.
- **Cắt tỉa:** mọi tập con 1 phần tử đều thuộc L1, nên chưa loại được ứng viên nào ở bước này.
- **Đếm:**

| C2 | TID | σ | ≥ 3? |
|---|---|---|---|
| {A, B} | 1, 2, 3 | 3 | ✔ |
| {A, C} | 1, 2, 3, 5 | 4 | ✔ |
| {A, D} | 3, 4, 5 | 3 | ✔ |
| {B, C} | 1, 2, 3, 6 | 4 | ✔ |
| {B, D} | 3, 6 | 2 | ✘ loại |
| {C, D} | 3, 5, 6 | 3 | ✔ |

**L2 = { AB:3, AC:4, AD:3, BC:4, CD:3 }**

#### Vòng k = 3: C3 → L3

**Sinh (join):** ghép các cặp trong L2 có **cùng mục đầu tiên**:

| Cặp ghép | Ứng viên | Tập con 2 phần tử | Kết quả cắt tỉa |
|---|---|---|---|
| AB + AC | {A, B, C} | AB ✔, AC ✔, BC ✔ | **giữ** |
| AB + AD | {A, B, D} | AB ✔, AD ✔, **BD ✘** | **CẮT TỈA** (BD không phổ biến), không cần đếm |
| AC + AD | {A, C, D} | AC ✔, AD ✔, CD ✔ | **giữ** |
| BC + ? | (không có tập nào khác bắt đầu bằng B) | | |
| CD + ? | (không có) | | |

**C3 sau khi cắt tỉa = { ABC, ACD }**

**Đếm:**

| C3 | TID | σ | ≥ 3? |
|---|---|---|---|
| {A, B, C} | 1, 2, 3 | 3 | ✔ |
| {A, C, D} | 3, 5 | 2 | ✘ loại |

**L3 = { ABC:3 }**

(Kiểm tra cho chắc: nếu không cắt tỉa ABD thì đếm ra σ(ABD) = 1 (chỉ T3), đúng là không phổ biến. Cắt tỉa không làm mất kết quả nào.)

#### Vòng k = 4

L3 chỉ có 1 phần tử nên không có cặp nào để ghép. **C4 = ∅**, và thuật toán dừng.

#### Kết quả: các tập mục phổ biến (10 tập)

| Kích thước | Tập (σ) |
|---|---|
| 1 | A:5, B:4, C:5, D:4 |
| 2 | AB:3, AC:4, AD:3, BC:4, CD:3 |
| 3 | ABC:3 |

**Số ứng viên phải đếm:** 5 (C1) + 6 (C2) + 2 (C3) = 13. Nếu vét cạn thì là $2^5 - 1 = 31$.
**Số lần quét CSDL:** 3.

#### Sinh luật với minconf = 75%

Áp dụng $c(X\rightarrow Y) = \sigma(X\cup Y)/\sigma(X)$. Chỉ sinh luật từ các tập phổ biến có ≥ 2 mục. Một tập k mục cho $2^k - 2$ luật.

**Từ các 2-itemset** (mỗi tập cho $2^2 - 2 = 2$ luật):

| Luật | Tính | c | ≥ 0.75? |
|---|---|---|---|
| A → B | σ(AB)/σ(A) = 3/5 | 0.60 | ✘ |
| B → A | 3/4 | 0.75 | ✔ |
| A → C | 4/5 | 0.80 | ✔ |
| C → A | 4/5 | 0.80 | ✔ |
| A → D | 3/5 | 0.60 | ✘ |
| D → A | 3/4 | 0.75 | ✔ |
| B → C | 4/4 | 1.00 | ✔ |
| C → B | 4/5 | 0.80 | ✔ |
| C → D | 3/5 | 0.60 | ✘ |
| D → C | 3/4 | 0.75 | ✔ |

**Từ 3-itemset ABC** (σ = 3, có $2^3 - 2 = 6$ luật). Ta sinh **theo tầng**, giống slide 120–121:

*Tầng 1: hệ quả có 1 mục*

| Luật | Tính | c | ≥ 0.75? |
|---|---|---|---|
| AB → C | 3/σ(AB) = 3/3 | 1.00 | ✔ |
| AC → B | 3/σ(AC) = 3/4 | 0.75 | ✔ |
| BC → A | 3/σ(BC) = 3/4 | 0.75 | ✔ |

*Tầng 2: hệ quả có 2 mục, ghép từ các hệ quả 1 mục của các luật đạt ở tầng 1*

| Luật | Tính | c | ≥ 0.75? |
|---|---|---|---|
| C → AB | 3/σ(C) = 3/5 | 0.60 | ✘ |
| B → AC | 3/σ(B) = 3/4 | 0.75 | ✔ |
| A → BC | 3/σ(A) = 3/5 | 0.60 | ✘ |

**Kiểm chứng tính anti-monotone (slide 119):** $c(AB\rightarrow C)=1.0 \ \ge\ c(A\rightarrow BC)=0.6$ ✔. $c(BC\rightarrow A)=0.75 \ \ge\ c(C\rightarrow AB)=0.6$ ✔.

**Biến thể để thấy cắt tỉa luật:** nếu **minconf = 80%** thì ở tầng 1 chỉ có AB → C (1.0) đạt; AC → B (0.75) và BC → A (0.75) bị loại.
- Ở tầng 2, mọi hệ quả 2 mục đều chứa A hoặc B:
  - {A,B} cần A→ và B→ đều đạt,
  - {A,C} chứa A, tương ứng luật BC→A đã trượt,
  - {B,C} chứa B, tương ứng luật AC→B đã trượt.
- Vì vậy **cả 3 luật C→AB, B→AC, A→BC bị cắt tỉa mà không cần tính**. Đây đúng là ý của slide 120.

**Kết quả cuối (minconf = 75%): 11 luật mạnh**
- B→A, A→C, C→A, D→A, B→C, C→B, D→C
- AB→C, AC→B, BC→A, B→AC

**Bonus: tập đóng và tập cực đại của ví dụ này** (xem slide 113–117)
- **Cực đại (maximal):** {A,B,C}, {A,D}, {C,D}. Mọi tập cha trực tiếp của chúng đều có σ < 3.
- **Đóng (closed):** A(5), C(5), D(4), AC(4), AD(3), BC(4), CD(3), ABC(3), tổng **8 tập**.
- **Không đóng:** B(4), vì BC cũng có 4; và AB(3), vì ABC cũng có 3.

---

## 16. Slide 111 — Các yếu tố ảnh hưởng đến độ phức tạp

| Yếu tố | Ảnh hưởng |
|---|---|
| **Ngưỡng minsup** | **Hạ minsup** cho ra nhiều tập phổ biến hơn, **nhiều ứng viên hơn** và **tập phổ biến dài hơn** (nên cần nhiều vòng hơn). |
| **Số chiều (số mục d)** | Cần nhiều bộ nhớ hơn để lưu support count của mỗi mục. Nếu số mục phổ biến cũng tăng thì cả chi phí tính toán lẫn I/O đều tăng. |
| **Kích thước CSDL (N)** | Apriori **quét CSDL nhiều lần**, nên thời gian chạy tăng theo số giao dịch. |
| **Độ rộng giao dịch trung bình (w)** | Dữ liệu càng dày đặc (dense) thì giao dịch càng rộng, tập phổ biến tối đa càng dài, và số tập con của một giao dịch cần duyệt trong **hash tree** càng tăng. Một giao dịch có w mục có $2^w$ tập con, mỗi tập con là một ứng viên có thể có (bổ sung). |

**Ví dụ:** w = 5 cho $\binom{5}{3} = 10$ tập con 3 phần tử cần kiểm tra mỗi giao dịch; w = 20 cho $\binom{20}{3} = 1140$ tập con.

---

## 17. Slide 112 — Biểu diễn gọn các tập phổ biến (Compact Representation)

**Vấn đề:** *Có những itemset bị dư thừa vì chúng có cùng support với các tập cha của chúng.*

**Dữ liệu trên slide:** 15 giao dịch, 30 mục chia làm 3 khối:
- T1–T5 chứa đúng 10 mục A1…A10,
- T6–T10 chứa đúng B1…B10,
- T11–T15 chứa đúng C1…C10.

**Số tập phổ biến:**
$$3\times\sum_{k=1}^{10}\binom{10}{k} = 3\times(2^{10}-1) = 3\times 1023 = 3069$$
(bổ sung: con số này đúng khi minsup ≤ 5 giao dịch. Mỗi khối có $2^{10}-1$ tập con khác rỗng, tất cả đều có support 5.)

**Nhận xét (bổ sung):** thông tin thật sự chỉ có 3 "khối" {A1..A10}, {B1..B10}, {C1..C10}. 3069 tập kia là dư thừa. Slide kết luận: **cần một biểu diễn gọn (Need a compact representation)**. Hai lời giải là tập **cực đại** và tập **đóng**. Ở ví dụ này cả hai cách đều chỉ còn **3 tập**.

---

## 18. Slide 113 — Tập phổ biến cực đại (Maximal Frequent Itemset)

**Định nghĩa:** một itemset là **phổ biến cực đại** nếu nó phổ biến và **không có tập cha trực tiếp (immediate superset) nào phổ biến**. (Tập cha trực tiếp là tập có thêm đúng 1 mục.)

**Hình trên slide:**
- Đường nét đứt đỏ là **biên (Border)** chia dàn thành hai phần: phía trên là phổ biến, phía dưới (tô xám) là không phổ biến.
- Các tập **cực đại** (tô xanh) là **AD, ACE, BCDE**. Chúng nằm ngay sát biên, phía bên phổ biến.
- Các tập **không phổ biến (Infrequent Itemsets)** được chỉ bằng mũi tên, ví dụ ABC, ABD, ABE, ABCD, ABCDE…

**Ý nghĩa:**
- Từ tập cực đại ta **suy ra được mọi tập phổ biến**: một tập là phổ biến khi và chỉ khi nó là **tập con của một tập cực đại nào đó**. Ví dụ: BCD ⊂ BCDE nên BCD phổ biến; ABC không là tập con của AD, ACE hay BCDE nên ABC không phổ biến.
- Đây là biểu diễn **rất gọn**: chỉ 3 tập thay cho toàn bộ tập phổ biến.
- **Nhược điểm (bổ sung, quan trọng):** tập cực đại **không giữ lại support** của các tập con. Biết BCD phổ biến nhưng không biết σ(BCD) bằng bao nhiêu, nên chưa tính được confidence.

**Ẩn dụ:** tập cực đại giống "các đỉnh núi" của vùng phổ biến. Biết các đỉnh thì biết toàn bộ vùng núi, nhưng không biết độ cao từng điểm.

---

## 19. Slide 114 — Tập đóng (Closed Itemset)

**Định nghĩa:** một itemset là **đóng (closed)** nếu **không có tập cha trực tiếp nào có cùng support** với nó.

Nói cách khác: thêm bất kỳ mục nào vào X thì support đều **giảm thật sự**. Nếu thêm mục Y vào mà support không đổi thì "mọi lần X xuất hiện, Y cũng xuất hiện", và X là tập dư thừa, không đóng.

**Dữ liệu trên slide:**

| TID | Items |
|---|---|
| 1 | {A, B} |
| 2 | {B, C, D} |
| 3 | {A, B, C, D} |
| 4 | {A, B, D} |
| 5 | {A, B, C, D} |

**Support (đã kiểm tra, khớp slide):**
- A:4, B:5, C:3, D:4
- AB:4, AC:2, AD:3, BC:3, BD:4, CD:3
- ABC:2, ABD:3, ACD:2, BCD:3, ABCD:2

**Tự xét tính đóng từng tập** (so với các tập cha trực tiếp):

| Tập | σ | Tập cha trực tiếp (σ) | Đóng? |
|---|---|---|---|
| A | 4 | AB=**4**, AC=2, AD=3 | ✘ |
| B | 5 | AB=4, BC=3, BD=4 | **✔** |
| C | 3 | AC=2, **BC=3**, CD=3 | ✘ |
| D | 4 | AD=3, **BD=4**, CD=3 | ✘ |
| AB | 4 | ABC=2, ABD=3 | **✔** |
| AC | 2 | **ABC=2**, ACD=2 | ✘ |
| AD | 3 | **ABD=3**, ACD=2 | ✘ |
| BC | 3 | ABC=2, **BCD=3** | ✘ |
| BD | 4 | ABD=3, BCD=3 | **✔** |
| CD | 3 | ACD=2, **BCD=3** | ✘ |
| ABC | 2 | **ABCD=2** | ✘ |
| ABD | 3 | ABCD=2 | **✔** |
| ACD | 2 | **ABCD=2** | ✘ |
| BCD | 3 | ABCD=2 | **✔** |
| ABCD | 2 | (không có) | **✔** |

**Các tập đóng: {B}, {A,B}, {B,D}, {A,B,D}, {B,C,D}, {A,B,C,D}.**

> ⚠️ **Slide có vẻ tô màu không khớp định nghĩa:** khi phóng to, mình thấy slide tô vàng {B}, {A,B}, {B,C}, {B,D}, {C,D}, {A,B,D}, {A,B,C,D}.
> - **{B,C}** và **{C,D}** thực ra **không đóng**: cả hai có support 3, bằng {B,C,D}.
> - **{B,C,D}** (σ = 3, tập cha duy nhất ABCD có σ = 2) thực ra **là tập đóng** nhưng không được tô.
>
> Có thể do lỗi slide gốc hoặc do màu tô khó phân biệt. **Hãy tin vào định nghĩa và tự kiểm tra.**

**Trực giác:** tập đóng là tập "đã gom hết các mục luôn đi kèm". Ví dụ, mọi giao dịch có C đều có B (C:3, BC:3), nên {C} chưa "đóng". Phải mở rộng thành {B,C}, rồi {B,C,D}, thì mới "đóng".

**Ý nghĩa (bổ sung):** từ các tập **đóng phổ biến** kèm support của chúng, ta **khôi phục được support của mọi tập phổ biến**:
$$s(X) = \max\{\, s(Y) : Y \text{ đóng},\ X \subseteq Y \,\}$$
Ví dụ: s(C) = max(s(BCD) = 3, s(ABCD) = 2) = 3 ✔. Vì vậy tập đóng là biểu diễn **không mất thông tin (lossless)**, còn tập cực đại thì mất thông tin support.

---

## 20. Slide 115 — Cực đại và Đóng: dàn có danh sách TID

**Dữ liệu:** T1 = ABC, T2 = ABCD, T3 = BCE, T4 = ACDE, T5 = DE.

Các **số đỏ** trên mỗi nút là **danh sách TID (Transaction Ids)** chứa itemset đó. Support count bằng độ dài danh sách. Đã kiểm tra:

| Itemset | TIDs | Itemset | TIDs | Itemset | TIDs |
|---|---|---|---|---|---|
| A | 1 2 4 | AB | 1 2 | ABC | 1 2 |
| B | 1 2 3 | AC | 1 2 4 | ABD | 2 |
| C | 1 2 3 4 | AD | 2 4 | ACD | 2 4 |
| D | 2 4 5 | AE | 4 | ACE | 4 |
| E | 3 4 5 | BC | 1 2 3 | ADE | 4 |
| | | BD | 2 | BCD | 2 |
| | | BE | 3 | BCE | 3 |
| | | CD | 2 4 | CDE | 4 |
| | | CE | 3 4 | ABCD | 2 |
| | | DE | 4 5 | ACDE | 4 |

- Các nút không có số (ABE, BDE, ABCE, ABDE, BCDE, ABCDE…) là các tập **không được giao dịch nào hỗ trợ (Not supported by any transactions)**.
- **Mẹo:** TID(X ∪ Y) = TID(X) ∩ TID(Y). Ví dụ TID(AC) = {1,2,4} ∩ {1,2,3,4} = {1,2,4}. Đây là ý tưởng của **vertical mining** (slide 106).

---

## 21. Slide 116 — Cực đại và Đóng với minsup = 2 ⭐

Cùng dữ liệu, **minsup count = 2**:
- **Các tập phổ biến:** A, B, C, D, E, AB, AC, AD, BC, CD, CE, DE, ABC, ACD.
- **Tập đóng phổ biến (# Closed = 9):** C(4), D(3), E(3), AC(3), BC(3), CE(2), DE(2), ABC(2), ACD(2).
- **Tập cực đại (# Maximal = 4):** **CE, DE, ABC, ACD** (khoanh viền xanh đậm), "Closed and maximal".
- Chú thích **"Closed but not maximal"** chỉ vào **C, D, E**.
  - Ví dụ C: σ = 4, mọi tập cha đều có σ ≤ 3 nên C đóng; nhưng tập cha AC phổ biến nên C không cực đại.
  - AC và BC cũng thuộc loại "đóng mà không cực đại" (tô xám trên hình), vì chúng nằm trong ABC.

**Vì sao A không đóng:** σ(A) = 3 (TID 1,2,4) bằng σ(AC) = 3 (TID 1,2,4). Mỗi lần có A đều có C.
**Vì sao AB không đóng:** σ(AB) = 2 bằng σ(ABC) = 2.
**Vì sao ABC cực đại:** tập cha duy nhất được hỗ trợ là ABCD với σ = 1 < 2.

**Đã kiểm chứng bằng máy:** đúng 9 tập đóng và 4 tập cực đại, khớp slide.

---

## 22. Slide 117 — Quan hệ bao hàm

$$\text{Maximal Frequent} \ \subseteq\ \text{Closed Frequent} \ \subseteq\ \text{Frequent Itemsets}$$

**Vì sao mọi tập cực đại đều đóng (bổ sung, chứng minh):** giả sử X cực đại. Mọi tập cha trực tiếp Y của X đều không phổ biến, nên $s(Y) <$ minsup $\le s(X)$, tức $s(Y) \ne s(X)$. Vậy X đóng.
**Chiều ngược lại sai:** ví dụ C ở slide 116 đóng nhưng không cực đại.

**So sánh nhanh:**

| | Maximal | Closed |
|---|---|---|
| Điều kiện | Không có tập cha trực tiếp nào **phổ biến** | Không có tập cha trực tiếp nào **cùng support** |
| Kích thước | Nhỏ nhất (gọn nhất) | Lớn hơn maximal |
| Khôi phục được tập phổ biến? | ✔ (lấy mọi tập con) | ✔ |
| Khôi phục được support? | ✘ (mất thông tin) | ✔ (không mất thông tin) |

---

## 23. Slide 118 — Sinh luật (Rule Generation)

**Bài toán:** cho tập phổ biến L, tìm mọi tập con khác rỗng $f \subset L$ sao cho luật $f \rightarrow L - f$ thoả minconf.

**Ví dụ:** L = {A,B,C,D} cho các luật ứng viên sau.
- Vế trái 3 mục: ABC→D, ABD→C, ACD→B, BCD→A
- Vế trái 1 mục: A→BCD, B→ACD, C→ABD, D→ABC
- Vế trái 2 mục: AB→CD, AC→BD, AD→BC, BC→AD, BD→AC, CD→AB

Tổng cộng **14 luật**.

**Công thức:** nếu $|L| = k$ thì có **$2^k - 2$ luật ứng viên** (bỏ $L\rightarrow\emptyset$ và $\emptyset\rightarrow L$).
- k = 4 cho $16 - 2 = 14$ ✔.
- k = 3 cho 6 luật ✔ (như ví dụ {Milk, Diaper, Beer} ở slide 101).

**Ưu điểm (bổ sung):** sinh luật **không cần quét lại CSDL**. Mọi support cần thiết ($\sigma(L)$ và $\sigma(f)$) đã được tính trong bước 1, vì f ⊂ L nên f cũng phổ biến (nguyên lý Apriori).

---

## 24. Slide 119 — Tính anti-monotone của confidence ⭐

**Nói chung, confidence KHÔNG có tính anti-monotone:** $c(ABC\rightarrow D)$ có thể **lớn hơn hoặc nhỏ hơn** $c(AB\rightarrow D)$.
- Lý do: $c(ABC\rightarrow D) = \sigma(ABCD)/\sigma(ABC)$ và $c(AB\rightarrow D) = \sigma(ABD)/\sigma(AB)$. Cả tử lẫn mẫu đều thay đổi.
- **Ví dụ từ bài tập ở 15.2:**
  - $c(A\rightarrow C) = 4/5 = 0.8$, còn $c(AB\rightarrow C) = 3/3 = 1.0$: thêm B vào vế trái làm confidence **tăng**.
  - $c(A\rightarrow B) = 3/5 = 0.6$, còn $c(AD\rightarrow B) = \sigma(ABD)/\sigma(AD) = 1/3 \approx 0.33$: thêm D vào vế trái làm confidence **giảm**.

**Nhưng với các luật sinh từ CÙNG một itemset L, confidence có tính anti-monotone:**
$$L = \{A,B,C,D\}:\quad c(ABC\rightarrow D)\ \ge\ c(AB\rightarrow CD)\ \ge\ c(A\rightarrow BCD)$$
Confidence **anti-monotone theo số mục ở vế phải (RHS)**: chuyển mục từ trái sang phải thì confidence chỉ có thể **giảm hoặc giữ nguyên**.

**Chứng minh (bổ sung):** các luật này đều có cùng tử số $\sigma(L)$. Mẫu số lần lượt là $\sigma(ABC) \le \sigma(AB) \le \sigma(A)$, do support anti-monotone. Mẫu số tăng dần nên confidence giảm dần. ∎

**Hệ quả để cắt tỉa:** nếu $X \rightarrow L - X$ có confidence thấp thì mọi luật $X' \rightarrow L - X'$ với $X' \subset X$ (vế trái nhỏ hơn, vế phải lớn hơn) cũng có confidence thấp.

---

## 25. Slide 120 — Dàn luật và cắt tỉa luật (Lattice of rules)

- Dàn luật của L = ABCD:
  - Gốc: ABCD ⇒ {}
  - Tầng 1 (hệ quả 1 mục): BCD⇒A, ACD⇒B, ABD⇒C, ABC⇒D
  - Tầng 2 (hệ quả 2 mục): CD⇒AB, BD⇒AC, BC⇒AD, AD⇒BC, AC⇒BD, AB⇒CD
  - Tầng 3 (hệ quả 3 mục): D⇒ABC, C⇒ABD, B⇒ACD, A⇒BCD
- Trên hình, **BCD⇒A có confidence thấp (Low Confidence Rule)**. Theo slide 119, mọi luật có **hệ quả chứa A** (vế trái là tập con của BCD) đều bị cắt tỉa (**Pruned Rules**): CD⇒AB, BD⇒AC, BC⇒AD, D⇒ABC, C⇒ABD, B⇒ACD.
- **Trực giác:** BCD⇒A đã yếu, tức là có B, C, D mà vẫn ít khi có A. Bớt thông tin ở vế trái (chỉ biết CD) mà còn đòi đoán thêm cả A lẫn B thì chỉ càng khó hơn.

Đây là "nguyên lý Apriori" áp dụng cho **luật**, tương tự slide 108 áp dụng cho **itemset**.

---

## 26. Slide 121 — Sinh luật trong Apriori: ghép luật

- **Luật ứng viên được tạo bằng cách ghép hai luật có cùng tiền tố (prefix) trong hệ quả (consequent).**
- **Ví dụ:** join(CD⇒**AB**, BD⇒**AC**) cho **D⇒ABC**.
  - Hệ quả AB và AC có chung tiền tố "A".
  - Hệ quả mới là AB ∪ AC = ABC.
  - Vế trái mới là phần còn lại: L − ABC = D (cũng bằng CD ∩ BD = D).
- **Cắt tỉa:** loại D⇒ABC nếu luật con của nó là **AD⇒BC** không có confidence cao. (Hệ quả BC là một tập con 2 mục của ABC; AD⇒BC chưa được dùng để ghép nên phải kiểm tra riêng, giống bước cắt tỉa ứng viên itemset.)

### Mã giả sinh luật (bổ sung, theo sách, khớp slide 118–121)

```
GenRules(tập phổ biến F, minconf):
    for mỗi tập phổ biến L ∈ F với |L| ≥ 2 :
        H1 ← { {i} : i ∈ L }                  // hệ quả 1 mục
        H1 ← { h ∈ H1 : σ(L)/σ(L−h) ≥ minconf } // giữ hệ quả cho luật mạnh, xuất luật (L−h)→h
        m ← 1
        while |L| > m+1 và Hm ≠ ∅ :
            Hm+1 ← ghép các cặp h, h' ∈ Hm có chung m−1 mục đầu   // như Apriori-gen
            Hm+1 ← bỏ h nếu có tập con m mục của h ∉ Hm             // cắt tỉa
            for h ∈ Hm+1 :
                c ← σ(L)/σ(L−h)
                if c ≥ minconf : xuất luật (L−h) → h
                else            : xoá h khỏi Hm+1
            m ← m + 1
```

Ví dụ chạy tay xem ở **mục 15.2** (luật từ ABC).

---

## 27. Phân tích sâu / đánh giá

1. **Vì sao Apriori đúng (không bỏ sót):** một tập k+1 mục bị cắt tỉa chỉ khi có tập con k mục không phổ biến. Theo tính anti-monotone, tập đó chắc chắn không phổ biến. Vậy mọi tập phổ biến đều được sinh ra và được đếm. Apriori **đầy đủ (complete)** và **chính xác (exact)**, không phải heuristic.
2. **Độ phức tạp:**
   - Trường hợp xấu nhất vẫn là hàm mũ: nếu mọi tập đều phổ biến (minsup rất thấp, dữ liệu dày), có $2^d$ tập.
   - Số lần quét CSDL là $k_{max}+1$.
   - Chi phí đếm khoảng $O(N \cdot |C_k| \cdot w)$ mỗi vòng.
   - Apriori hiệu quả nhất khi dữ liệu **thưa (sparse)** và minsup **không quá thấp**.
3. **Hạn chế của Apriori (bổ sung):**
   - Quét CSDL nhiều lần.
   - Có thể sinh rất nhiều ứng viên. Ví dụ có $10^4$ mục đơn phổ biến thì C2 có khoảng $5\times10^7$ cặp.
   - Để tìm một tập phổ biến dài 100 mục, phải sinh khoảng $2^{100}$ tập con.
   - Các giải pháp khác: **FP-Growth** (cây FP-tree, không sinh ứng viên), **Eclat** (dọc, giao TID-list), **DHP**, sampling, partitioning.
4. **Chọn minsup là đánh đổi:**
   - Cao quá thì **mất các luật hiếm nhưng có giá trị** (ví dụ mua đồ trang sức đắt tiền).
   - Thấp quá thì **bùng nổ** số tập và luật, chạy chậm, và sinh nhiều luật giả (spurious).
5. **⚠️ Confidence cao ≠ luật thú vị (bổ sung, rất hay ra):** confidence bỏ qua support của vế phải.
   - **Ví dụ kinh điển (sách Tan, mục 6.7):** khảo sát 1000 người.
     - 200 người uống trà (Tea), trong đó 150 người uống cả cà phê.
     - Tổng cộng 900 người uống cà phê (Coffee).
     - Khi đó c(Tea→Coffee) = 150/200 = 0.75, nghe có vẻ cao.
     - Nhưng P(Coffee) = 900/1000 = 0.9 > 0.75. Biết một người uống trà lại làm **giảm** khả năng người đó uống cà phê.
   - Độ đo bổ sung: **Lift** $= \dfrac{c(X\rightarrow Y)}{s(Y)} = \dfrac{s(X\cup Y)}{s(X)\,s(Y)}$.
     - Lift > 1: tương quan dương.
     - Lift = 1: độc lập.
     - Lift < 1: tương quan âm.
     - Với trà/cà phê: lift = 0.75/0.9 ≈ 0.83 < 1.
   - **Trong ví dụ 15.2:** A→C có c = 0.8 (luật "mạnh") nhưng lift = 0.8/(5/6) = **0.96 < 1**, nghĩa là A và C thậm chí hơi tương quan âm. D→A có c = 0.75 nhưng lift = 0.9. Ngược lại, B→C có c = 1.0 và lift = 1.2, đây mới là quan hệ dương thật.
6. **Tương quan ≠ nhân quả** (slide 97). Luật chỉ mô tả đồng xuất hiện.
7. **Liên hệ với các phần khác:**
   - **Clustering (Ch 8):** cùng là học không giám sát. Tuy nhiên clustering nhóm các *đối tượng (giao dịch)*, còn association tìm quan hệ giữa các *thuộc tính (mục)*.
   - **Classification (Ch 4):** luật kết hợp có vế phải là nhãn lớp cho ra "classification rules" (bổ sung: phương pháp CBA, *associative classification*).
   - **Tiền xử lý (Ch 1–2):** dữ liệu số hoặc định danh phải được **nhị phân hoá (binarization)** hoặc rời rạc hoá thành các "item" thì mới áp dụng được. Ví dụ "Tuổi ∈ [20,30)" trở thành một item.
   - Ma trận giao dịch nhị phân trên slide 112 chính là dạng "asymmetric binary data" ở Ch 1/2: chỉ giá trị 1 (có mua) là quan trọng.

---

## 28. Dễ nhầm lẫn ⚠️

| Nhầm lẫn | Đúng là |
|---|---|
| Support count σ và support s là một | σ là **số đếm** (vd 2), s = σ/N là **tỉ lệ** (vd 0.4). Đọc kỹ đề cho minsup dạng nào. |
| $\sigma(X\cup Y)$ là số giao dịch chứa X **hoặc** Y | Là số giao dịch chứa **tất cả mục của X và của Y** (hợp các tập mục, tức giao các tập giao dịch). |
| Confidence chia cho N | $c = \sigma(X\cup Y)/\sigma(X)$, chia cho support count **của vế trái**, không phải N, cũng không phải σ(Y). |
| c(X→Y) = c(Y→X) | Sai. Tử số giống nhau nhưng mẫu số khác: $\sigma(X)$ và $\sigma(Y)$. Support thì đối xứng: s(X→Y) = s(Y→X). |
| Nguyên lý Apriori: "tập con phổ biến thì tập cha phổ biến" | **Ngược lại!** Tập cha phổ biến thì tập con phổ biến; tập con **không** phổ biến thì tập cha **không** phổ biến. |
| Support anti-monotone nghĩa là tập càng lớn support càng lớn | Tập **lớn hơn** thì support **nhỏ hơn hoặc bằng**. |
| Confidence luôn anti-monotone | Chỉ đúng **giữa các luật từ cùng một itemset**, theo số mục ở vế phải. Thêm mục vào vế trái của luật bất kỳ có thể làm c tăng hoặc giảm. |
| Cắt tỉa = loại ứng viên sau khi đếm | Trong Apriori có 2 bước loại khác nhau: **cắt tỉa (prune)** *trước khi đếm*, dựa trên tập con không phổ biến; và **loại (eliminate)** *sau khi đếm*, dựa trên σ < minsup. |
| Cắt tỉa thì kiểm tra các tập con k−1 mục | Ứng viên kích thước k+1 được kiểm tra bằng **mọi tập con kích thước k** của nó, so với L_k. |
| Tập đóng = tập cực đại | Cực đại ⊆ Đóng. Cực đại xét "tập cha có **phổ biến** không", đóng xét "tập cha có **cùng support** không". |
| Tập đóng thì phải phổ biến | Định nghĩa "closed" không cần minsup. "Closed **frequent**" = đóng **và** phổ biến. |
| Xét "immediate superset" là xét mọi tập cha | Chỉ cần xét tập cha **trực tiếp** (thêm 1 mục). Nhờ tính anti-monotone thế là đủ. |
| Số luật từ tập k mục là $2^k$ | Là $2^k - 2$ (bỏ ∅→L và L→∅). |
| Số itemset trên d mục là $2^d - 1$ hay $2^d$? | Slide ghi $2^d$ (kể cả tập rỗng `null`). Nếu đề hỏi itemset **khác rỗng** thì ghi $2^d - 1$ và nói rõ. |
| Luật mạnh thì thú vị và có quan hệ nhân quả | Không. Cần xét lift và tri thức miền. Luật chỉ là đồng xuất hiện. |
| Bước join ghép mọi cặp trong L_k | Chỉ ghép các cặp có **k−1 mục đầu giống nhau** (đã sắp thứ tự). Ví dụ {A,B} và {B,C} không ghép. |

---

## 29. Câu hỏi có thể ra thi (kèm lời giải ngắn)

**Q1. Với bảng slide 97, tính s và c của luật {Bread, Diaper} → {Beer}.**
- σ(Bread, Diaper, Beer) = 2 (T2, T4), nên s = 2/5 = 0.4.
- σ(Bread, Diaper) = 3 (T2, T4, T5), nên c = 2/3 ≈ 0.67.

**Q2. Có bao nhiêu luật kết hợp có thể có trên d = 4 mục? Và bao nhiêu itemset?**
- Số luật: $R = 3^4 - 2^5 + 1 = 81 - 32 + 1 = 50$.
- Số itemset: $2^4 = 16$ (kể cả rỗng), hay 15 itemset khác rỗng.

**Q3. Có bao nhiêu luật ứng viên sinh từ một tập phổ biến 5 mục?**
- $2^5 - 2 = 30$.

**Q4. Phát biểu và chứng minh nguyên lý Apriori.**
- Phát biểu: nếu $X\subseteq Y$ thì $s(X)\ge s(Y)$.
- Chứng minh: mỗi giao dịch chứa Y đều chứa X.
- Hệ quả: tập không phổ biến thì mọi tập cha của nó không phổ biến, nên cắt tỉa được tập cha.

**Q5. Chạy Apriori trên CSDL cho trước với minsup = …** (dạng bài chính)
- Trình bày giống mục 15.2: bảng C1/L1, C2/L2, C3 (ghi rõ cặp ghép và lý do cắt tỉa)/L3, …
- **Ghi TID cho từng ứng viên** để giám khảo dễ chấm và để bản thân tránh đếm sai.

**Q6. Cho L2 = {AB, AC, AD, BC, BD, CE}. Tìm C3 sau bước join và prune.**
- Join (cùng mục đầu):
  - AB+AC cho ABC
  - AB+AD cho ABD
  - AC+AD cho ACD
  - BC+BD cho BCD
- Prune:
  - ABC: cần BC ✔, giữ.
  - ABD: cần BD ✔, giữ.
  - ACD: cần CD ✘, loại.
  - BCD: cần CD ✘, loại.
- **C3 = {ABC, ABD}**.

**Q7. Confidence có tính anti-monotone không?**
- Nói chung là không: c(ABC→D) có thể lớn hơn hoặc nhỏ hơn c(AB→D).
- Nhưng với các luật từ **cùng một itemset**, confidence giảm khi vế phải tăng: c(ABC→D) ≥ c(AB→CD) ≥ c(A→BCD). Chứng minh: cùng tử số σ(L), mẫu số σ(vế trái) tăng khi vế trái co lại.

**Q8. Vì sao nên tách bài toán thành 2 bước?**
- Các luật từ cùng itemset có cùng support (slide 101), nên lọc theo minsup một lần ở mức itemset thay cho nhiều lần ở mức luật.
- Sinh luật sau đó không cần quét lại CSDL.

**Q9. Với dữ liệu slide 115 và minsup = 2, liệt kê tập đóng và tập cực đại.**
- Đóng: C, D, E, AC, BC, CE, DE, ABC, ACD (9 tập).
- Cực đại: CE, DE, ABC, ACD (4 tập).
- Giải thích ví dụ: A không đóng vì σ(A) = σ(AC) = 3.

**Q10. So sánh tập cực đại và tập đóng.**
- Xem bảng mục 22.
- Maximal ⊆ Closed ⊆ Frequent. Maximal gọn hơn nhưng mất support; closed giữ được support (lossless).

**Q11. Nêu các yếu tố ảnh hưởng đến độ phức tạp của Apriori.**
- minsup, số mục d, số giao dịch N, độ rộng giao dịch trung bình w (slide 111).

**Q12. Một luật có confidence 90% có chắc là thú vị không?**
- Không chắc. Nếu s(Y) ≥ 0.9 thì lift ≤ 1, tức X không làm tăng khả năng Y.
- Ngoài ra luật chỉ phản ánh đồng xuất hiện, không phải nhân quả.

**Q13. Nếu BCD→A có confidence thấp, những luật nào từ ABCD bị cắt tỉa?**
- Mọi luật có hệ quả chứa A (vế trái là tập con thực sự của BCD): CD→AB, BD→AC, BC→AD, D→ABC, C→ABD, B→ACD.

**Q14. Ghép CD⇒AB và BD⇒AC cho luật gì? Khi nào luật đó bị cắt tỉa?**
- Cho D⇒ABC.
- Bị cắt nếu AD⇒BC có confidence thấp.

**Q15. Kiểm tra lại số trên slide 109:** σ({Bread, Milk, Diaper}) = 2 (T4, T5), không phải 3, nên với minsup = 3, L3 = ∅.

---

## 30. Tóm tắt cho tờ A4 📝

**Định nghĩa**
- Itemset; k-itemset = tập có k mục.
- $\sigma(X)$ = số giao dịch chứa X; $s(X) = \sigma(X)/N$.
- Frequent: $s \ge$ minsup.
- Luật $X\rightarrow Y$ với $X\cap Y=\emptyset$.
- $s(X\rightarrow Y) = \sigma(X\cup Y)/N$; $c(X\rightarrow Y) = \sigma(X\cup Y)/\sigma(X) = P(Y|X)$.
- (bổ sung) lift $= c/s(Y)$: >1 dương, =1 độc lập, <1 âm.
- Luật = co-occurrence, **không phải causality**.

**Đếm**
- Số itemset: $2^d$ (kể cả ∅).
- Số luật: $R = 3^d - 2^{d+1} + 1$ (d = 6 cho 602).
- Số luật từ tập k mục: $2^k - 2$.
- Vét cạn tốn $O(NMw)$ với $M = 2^d$.

**Hai bước:**
1. Frequent itemset generation (support).
2. Rule generation (confidence), mỗi luật là một cách chia đôi tập phổ biến.

**Nguyên lý Apriori:** $X\subseteq Y \Rightarrow s(X)\ge s(Y)$ (anti-monotone). Tập không phổ biến thì mọi tập cha không phổ biến.

**Apriori:**
- k = 1; tính L1.
- Lặp lại:
  - (1) **Join** L_k × L_k (cùng k−1 mục đầu) cho C_{k+1}.
  - (2) **Prune**: bỏ ứng viên có tập con k mục ∉ L_k.
  - (3) **Count**: quét CSDL.
  - (4) **Eliminate**: bỏ σ < minsup, được L_{k+1}.
- Dừng khi L_k = ∅.

**Chiến lược:** giảm M (pruning), giảm N (DHP, vertical), giảm NM (hash tree).

**Độ phức tạp tăng khi:** minsup ↓, d ↑, N ↑, w ↑.

**Maximal:** phổ biến và không tập cha trực tiếp nào phổ biến. Gọn nhất nhưng mất support.

**Closed:** không tập cha trực tiếp nào có cùng support. Lossless: $s(X) = \max\{s(Y): Y \text{ đóng}, Y\supseteq X\}$.

**Bao hàm:** Maximal ⊆ Closed ⊆ Frequent.

**Confidence:**
- Nói chung không anti-monotone.
- Cùng itemset L thì anti-monotone theo |RHS|: $c(ABC\rightarrow D)\ge c(AB\rightarrow CD)\ge c(A\rightarrow BCD)$.
- Luật X→L−X yếu thì mọi luật có vế trái X' ⊂ X cũng yếu, nên cắt tỉa được.

**Sinh luật:**
- Tầng 1 lấy hệ quả 1 mục.
- Ghép 2 luật có chung tiền tố hệ quả: join(CD⇒AB, BD⇒AC) cho D⇒ABC.
- Cắt D⇒ABC nếu AD⇒BC yếu.
- Không cần quét lại CSDL.

**Mẹo làm bài:**
- Ghi TID-list cạnh mỗi ứng viên; σ(XY) = |TID(X) ∩ TID(Y)|.
- Đổi minsup % sang số đếm trước khi bắt đầu.
- Ghi rõ "pruned vì tập con … ∉ L_k".

**⚠️ Lỗi slide 109:** σ(Bread, Milk, Diaper) = 2, không phải 3.


---

# Chương 4 — Phân lớp (Classification), phần A: slide 122 → 148

> Phạm vi: định nghĩa phân lớp, tập huấn luyện / tập kiểm tra, cây quyết định (decision tree), cách áp dụng cây, thuật toán Hunt (Hunt's algorithm), chiến lược tham lam (greedy), cách chia theo từng loại thuộc tính, và câu hỏi "chia thế nào là tốt nhất".
> Các công thức độ vẩn đục (impurity) GINI / entropy / classification error nằm chính thức ở slide 149–164 (phần B). Vì đây là dạng bài thi kinh điển nên ở đây vẫn có **ví dụ tính tay đầy đủ** (mục 7), có trích dẫn đúng các slide đó.
> Ký hiệu: "(bổ sung)" = kiến thức ngoài slide.

---

## 0. Slide 122 — Mục lục
Slide chỉ đánh dấu ta đang bước vào phần 4 của môn: **Classification (Ch 4)**, sau Introduction, Cluster Analysis và Association Analysis.

**Đặt vào bối cảnh (bổ sung):**
| | Clustering (Ch 8) | Association (Ch 6) | Classification (Ch 4) |
|---|---|---|---|
| Kiểu học | không giám sát (unsupervised) | không giám sát | **có giám sát (supervised)** |
| Có nhãn lớp? | Không | Không | **Có**: một thuộc tính là *class* |
| Kết quả | các nhóm (clusters) | luật $X \Rightarrow Y$ | một **mô hình** dự đoán nhãn |

---

## 1. Định nghĩa phân lớp (slide 123)

Nội dung slide:
- Cho một tập bản ghi (records) gọi là **tập huấn luyện (training set)**.
  - Mỗi bản ghi có một tập **thuộc tính (attributes)**, trong đó **một thuộc tính là lớp (class)**.
- Tìm một **mô hình (model)** cho thuộc tính lớp, dưới dạng **hàm của các thuộc tính còn lại**: $\text{class} = f(\text{attr}_1, \dots, \text{attr}_m)$.
- **Mục tiêu**: những bản ghi **chưa từng thấy (previously unseen)** phải được gán lớp **chính xác nhất có thể**.
  - Dùng một **tập kiểm tra (test set)** để đo **độ chính xác (accuracy)** của mô hình. Thông thường, dữ liệu được **chia thành tập huấn luyện và tập kiểm tra**: tập huấn luyện để **xây dựng** mô hình, tập kiểm tra để **đánh giá (validate)** nó.

**Giải thích dễ hiểu:** giống học sinh ôn thi. Đề cương có đáp án = training set; đề thi thật (chưa thấy bao giờ) = test set. Học thuộc lòng đáp án đề cương (training) không chứng minh được gì; điểm thi thật mới đo được bạn có "hiểu" không. Vì vậy **không bao giờ đánh giá mô hình trên chính dữ liệu đã dùng để học**.

**Ví dụ:** ngân hàng có 10 000 khách hàng cũ, biết ai đã vỡ nợ (class = Yes/No). Ta học mô hình $f(\text{thu nhập}, \text{tuổi}, \text{nghề}, \dots)$ để dự đoán khách hàng **mới**. Chia ngẫu nhiên, ví dụ 70% học / 30% kiểm tra.

**Phân tích sâu (bổ sung):**
- Accuracy $= \dfrac{\text{số bản ghi dự đoán đúng}}{\text{tổng số bản ghi test}}$; error rate $= 1 - \text{accuracy}$.
- Thuộc tính lớp phải là **rời rạc / định danh (categorical)**. Nếu đầu ra là số liên tục thì đó là **hồi quy (regression)**, không phải phân lớp.
- Lý do cần test set riêng: mô hình có thể "học thuộc" cả nhiễu của training set (**overfitting**, slide 169+), nên lỗi trên training set luôn **lạc quan** hơn thực tế.

---

## 2. Minh họa nhiệm vụ phân lớp (slide 124)

Hình gồm:
- **Training Set** (Tid 1–10): Attrib1 (Yes/No), Attrib2 (Large/Medium/Small), Attrib3 (số: 125K, 100K, …), **Class** (Yes/No).
- **Learning algorithm** → **Learn Model** → **Model**: chiều đi này gọi là **quy nạp (Induction)**: từ các ví dụ cụ thể suy ra quy luật tổng quát.
- **Model** → **Apply Model** trên **Test Set** (Tid 11–15, cột Class = "?"): chiều này gọi là **suy diễn (Deduction)**: từ quy luật tổng quát suy ra kết luận cho từng trường hợp cụ thể.

**Ẩn dụ:** Induction = quan sát 10 con thiên nga trắng rồi rút ra "thiên nga thì trắng". Deduction = gặp con chim mới, biết nó là thiên nga, suy ra "nó trắng".

> Đây là sơ đồ "2 pha" mà mọi bộ phân lớp đều theo: **pha học (learning/training)** và **pha áp dụng (prediction/classification)**.

---

## 3. Ví dụ ứng dụng (slide 125) và các kỹ thuật (slide 126)

**Slide 125 — ví dụ ứng dụng:**
- Dự đoán tế bào u là **lành tính / ác tính** (benign / malignant).
- Phân loại giao dịch thẻ tín dụng: **hợp lệ / gian lận** (legitimate / fraudulent).
- Phân loại cấu trúc bậc hai của protein: **alpha-helix, beta-sheet, random coil**. Đây là ví dụ có **3 lớp**, nên phân lớp không chỉ là nhị phân.
- Phân loại tin tức: **finance, weather, entertainment, sports…** (nhiều lớp).

**Slide 126 — các kỹ thuật phân lớp:**
1. Dựa trên **cây quyết định** (Decision Tree based Methods) → nội dung chính của chương này.
2. Dựa trên **luật** (Rule-based Methods).
3. **Suy luận dựa trên bộ nhớ** (Memory based reasoning), ví dụ k-NN (bổ sung: "học lười", chỉ lưu dữ liệu và so sánh với láng giềng gần nhất).
4. **Mạng nơ-ron** (Neural Networks).
5. **Naïve Bayes** và **mạng niềm tin Bayes** (Bayesian Belief Networks).
6. **Máy vector hỗ trợ** (Support Vector Machines, SVM).

---

## 4. Cây quyết định: ví dụ và cách áp dụng (slide 127 → 135)

### 4.1 Bộ dữ liệu "Cheat" (dùng xuyên suốt chương, slide 127)

| Tid | Refund | Marital Status | Taxable Income | **Cheat** |
|---|---|---|---|---|
| 1 | Yes | Single | 125K | No |
| 2 | No | Married | 100K | No |
| 3 | No | Single | 70K | No |
| 4 | Yes | Married | 120K | No |
| 5 | No | Divorced | 95K | Yes |
| 6 | No | Married | 60K | No |
| 7 | Yes | Divorced | 220K | No |
| 8 | No | Single | 85K | Yes |
| 9 | No | Married | 75K | No |
| 10 | No | Single | 90K | Yes |

Kiểu thuộc tính (ghi chú xanh trên slide): Refund = **categorical** (nhị phân), Marital Status = **categorical** (nominal), Taxable Income = **continuous**, Cheat = **class**. Phân bố lớp: **3 Yes / 7 No**.
(Refund = "được hoàn thuế"; Cheat = "gian lận thuế".)

### 4.2 Mô hình: cây quyết định (slide 127)

```
              Refund
           Yes/     \No
           NO       MarSt
                Single,/   \Married
               Divorced     NO
                  TaxInc
             < 80K/   \> 80K
               NO      YES
```
- **Nút trong (internal node)**: một **phép kiểm tra trên thuộc tính** (attribute test). Các thuộc tính dùng ở đây gọi là **splitting attributes** (mũi tên đỏ trên slide).
- **Nhánh (branch)**: một kết quả của phép kiểm tra.
- **Lá (leaf)**: một **nhãn lớp** (NO / YES).

Kiểm tra: cây này phân lớp **đúng cả 10** bản ghi huấn luyện (Refund=Yes → {1,4,7} đều No; Refund=No & Married → {2,6,9} đều No; Refund=No & Single/Divorced → {3: 70K→NO ✓, 5: 95K→YES ✓, 8: 85K→YES ✓, 10: 90K→YES ✓}).

### 4.3 Một cây khác cho cùng dữ liệu (slide 128)
```
             MarSt
     Married/     \Single, Divorced
        NO        Refund
              Yes/     \No
              NO      TaxInc
                  < 80K/  \> 80K
                    NO     YES
```
Thông điệp đỏ của slide: **"There could be more than one tree that fits the same data!"** Có thể có nhiều cây cùng khớp dữ liệu.
→ Vì vậy cần một **tiêu chí** để chọn cây (nhỏ hơn, tổng quát tốt hơn): chính là các độ đo impurity ở phần sau và nguyên lý Occam's Razor (slide 173).

**Phân tích sâu:** số cây có thể có tăng **theo hàm mũ** theo số thuộc tính. Tìm cây **tối ưu** (nhỏ nhất, chính xác nhất) là bài toán NP-khó (bổ sung). Vì thế các thuật toán dùng **chiến lược tham lam (greedy)** (slide 140): ra quyết định tốt nhất *tại chỗ*, không quay lui.

### 4.4 Decision Tree Classification Task (slide 129 và 136)
Cùng sơ đồ như slide 124, nhưng "Learning algorithm" được thay bằng **Tree Induction algorithm** và Model = **Decision Tree**.
- Slide 129 tô đỏ **Apply Model** (deduction): đây là phần slide 130–135.
- Slide 136 tô đỏ **Tree Induction algorithm** (induction): đây là phần slide 137 trở đi.

### 4.5 Áp dụng cây cho dữ liệu test (slide 130 → 135)
Bản ghi test: **Refund = No, Marital Status = Married, Taxable Income = 80K, Cheat = ?**

Các bước (mỗi slide là một bước):
1. (130) **Bắt đầu từ gốc** (Start from the root of tree).
2. (131) Gốc kiểm tra **Refund** → nhìn giá trị Refund của bản ghi.
3. (132) Refund = **No** → đi nhánh **No** → tới nút **MarSt**.
4. (133) Nhìn Marital Status của bản ghi.
5. (134) = **Married** → đi nhánh Married → gặp **lá NO**.
6. (135) **Assign Cheat to "No"**.

Chú ý: thuộc tính TaxInc **không cần dùng** cho bản ghi này. Mỗi bản ghi chỉ đi theo **một đường từ gốc đến lá**, nên dự đoán rất nhanh, độ phức tạp = độ sâu của cây.

**Ẩn dụ:** trò chơi "20 câu hỏi" hoặc sơ đồ chẩn đoán của bác sĩ: hỏi lần lượt, mỗi câu trả lời dẫn tới câu hỏi tiếp theo, cho tới khi có kết luận.

**Mẹo (bổ sung):** mỗi đường gốc→lá chính là **một luật IF-THEN**: `IF Refund=No AND MarSt=Married THEN Cheat=No`. Đây là lý do cây quyết định dễ diễn giải.

---

## 5. Xây dựng cây: Tree Induction (slide 136 → 140)

### 5.1 Các thuật toán (slide 137)
- **Hunt's Algorithm** (một trong những thuật toán sớm nhất, nền tảng của các thuật toán sau)
- **CART**
- **ID3, C4.5**
- **SLIQ, SPRINT**

(bổ sung, khớp slide 154 và 161: CART, SLIQ, SPRINT dùng **GINI**; ID3, C4.5 dùng **Information Gain** (C4.5 dùng thêm **Gain Ratio**).)

### 5.2 Cấu trúc tổng quát của thuật toán Hunt (slide 138)
Gọi $D_t$ = **tập các bản ghi huấn luyện đi tới nút $t$**.

Thủ tục tổng quát:
1. Nếu $D_t$ chỉ chứa bản ghi **cùng một lớp $y_t$** → $t$ là **lá** mang nhãn $y_t$.
2. Nếu $D_t$ **rỗng** → $t$ là **lá** mang nhãn **lớp mặc định $y_d$** (default class).
3. Nếu $D_t$ chứa bản ghi thuộc **nhiều hơn một lớp** → dùng một **phép kiểm tra thuộc tính (attribute test)** để **chia dữ liệu thành các tập con nhỏ hơn**, rồi **áp dụng đệ quy** thủ tục cho từng tập con.

Hình bên phải slide: bảng Cheat + nút $D_t$ với dấu "?" (chưa biết chia theo gì).

**Pseudo-code (bổ sung, viết gọn để học):**
```
Hunt(D_t):
  if tất cả bản ghi trong D_t cùng lớp y:      return Leaf(y)
  if D_t rỗng:                                  return Leaf(y_d)   # y_d thường = lớp đa số của nút cha
  if hết thuộc tính / mọi bản ghi giống hệt nhau:  return Leaf(lớp đa số)   # xem slide 166
  chọn phép thử tốt nhất A (theo GINI / entropy / ...)
  for mỗi kết quả v của A:
      con_v = Hunt({r ∈ D_t | A(r) = v})
  return Node(A, các con)
```
**Phân tích sâu:**
- Trường hợp 2 (rỗng) xảy ra khi một giá trị thuộc tính **không xuất hiện** trong $D_t$ (ví dụ chia multi-way theo Marital Status, mà ở nút này không có ai "Divorced"). Sách Tan et al. lấy $y_d$ = **lớp đa số của nút cha** (bổ sung).
- Có thêm trường hợp thứ 4 không ghi ở slide 138: các bản ghi có **thuộc tính giống hệt nhau nhưng khác lớp** (dữ liệu nhiễu), nên không thể chia được nữa → lá mang **lớp đa số**. Slide 166 nhắc điều này ("all the records have similar attribute values").
- Đây là thuật toán **chia để trị (divide and conquer)**, **top-down**, **đệ quy**.

### 5.3 Chạy thuật toán Hunt trên bộ Cheat (slide 139)
Slide vẽ 4 bước:

| Bước | Cây | Giải thích |
|---|---|---|
| 1 | Một lá **Don't Cheat** | Chưa chia gì; nhãn = lớp đa số (7 No > 3 Yes). |
| 2 | **Refund**: Yes → *Don't Cheat*; No → *Don't Cheat* | Refund=Yes: {1,4,7} toàn No → **lá thuần**. Refund=No: {2,3,5,6,8,9,10} = 3 Yes, 4 No → tạm gán đa số "Don't Cheat" nhưng **chưa thuần** → còn phải chia. |
| 3 | Dưới Refund=No: **Marital Status**: Single, Divorced → *Cheat*; Married → *Don't Cheat* | Married: {2,6,9} toàn No → thuần. Single/Divorced: {3,5,8,10} = 3 Yes, 1 No → tạm gán đa số "Cheat", chưa thuần. |
| 4 | Dưới Single/Divorced: **Taxable Income**: < 80K → *Don't Cheat*; ≥ 80K → *Cheat* | <80K: {3} (70K, No) ✓; ≥80K: {5,8,10} toàn Yes ✓. Mọi lá đều thuần → dừng. |

Lưu ý ký hiệu: slide 127 ghi "< 80K / > 80K", còn slide 139 ghi "< 80K / >= 80K". Cách viết đúng chuẩn là **$<v$ / $\geq v$** (slide 145) để không bỏ sót giá trị bằng đúng 80K.

**Câu hỏi tự nhiên:** tại sao bước 2 chọn Refund mà không phải Marital Status? Slide 139 **không nói**. Đó chính là câu hỏi "how to determine the best split" (slide 147–148, và phần impurity). Mục 7.4 bên dưới tính thử và sẽ thấy Refund **không** phải lựa chọn tốt nhất theo GINI/entropy.

### 5.4 Chiến lược và các vấn đề (slide 140, 141, 147)
- **Chiến lược tham lam (Greedy strategy)**: chia bản ghi theo phép thử thuộc tính **tối ưu một tiêu chí nào đó** (tại nút hiện tại).
- **Các vấn đề cần giải quyết (Issues):**
  1. **Chia bản ghi thế nào:**
     - a. Làm sao **xác định điều kiện kiểm tra** (attribute test condition)? → slide 141–146
     - b. Làm sao **chọn cách chia tốt nhất**? → slide 147–164
  2. **Khi nào dừng chia?** → slide 165–166 (phần B)

Ba slide 140/141/147 giống nhau, chỉ khác dòng được tô đỏ = "chúng ta đang ở đâu".

**Phân tích sâu, nhược điểm của greedy:** quyết định ở gốc **không bao giờ được xem lại**. Một thuộc tính có vẻ "kém" khi đứng một mình nhưng lại rất mạnh khi **kết hợp** với thuộc tính khác (ví dụ kinh điển: XOR, $y = A \oplus B$, nhìn riêng A hay B đều có gain = 0) sẽ bị bỏ qua (bổ sung).

---

## 6. Cách đặt điều kiện kiểm tra (slide 142 → 146)

### 6.1 Phụ thuộc vào gì? (slide 142)
- **Kiểu thuộc tính:** Nominal (định danh), Ordinal (thứ tự), Continuous (liên tục).
- **Số nhánh:** **2-way split** (nhị phân) hoặc **Multi-way split** (nhiều nhánh).

### 6.2 Thuộc tính định danh, Nominal (slide 143)
Ví dụ CarType ∈ {Family, Sports, Luxury}.
- **Multi-way split:** mỗi giá trị khác nhau một nhánh → 3 nhánh Family | Sports | Luxury.
- **Binary split:** chia các giá trị thành **2 tập con**; **cần tìm cách chia tối ưu**. Ví dụ slide: {Sports, Luxury} vs {Family} **hoặc** {Family, Luxury} vs {Sports}.

Số cách chia nhị phân với $k$ giá trị: $2^{k-1} - 1$ (bổ sung). Với $k=3$: $2^2 - 1 = 3$ cách ({F}|{S,L}, {S}|{F,L}, {L}|{F,S}). Vì nominal không có thứ tự nên **mọi** cách gom nhóm đều hợp lệ.

### 6.3 Thuộc tính thứ tự, Ordinal (slide 144)
Ví dụ Size ∈ {Small < Medium < Large}.
- Multi-way: Small | Medium | Large.
- Binary: {Small, Medium} vs {Large} **hoặc** {Medium, Large} vs {Small}.
- **"What about this split?"** {Small, Large} vs {Medium}: **không hợp lệ** (hoặc ít nhất là vô nghĩa) cho thuộc tính ordinal vì nó **phá vỡ thứ tự**: gom hai đầu mút lại với nhau bỏ qua giá trị ở giữa. Với ordinal, phép chia nhị phân phải giữ thứ tự, tức là có dạng "Size ≤ ngưỡng".
- Số cách chia nhị phân giữ thứ tự với $k$ giá trị: $k-1$ (bổ sung). Với $k = 3$: 2 cách.

### 6.4 Thuộc tính liên tục, Continuous (slide 145, 146)
Hai cách xử lý:
1. **Rời rạc hóa (Discretization)** để biến thành một thuộc tính **ordinal categorical**:
   - **Tĩnh (Static):** rời rạc hóa **một lần ở đầu** (trước khi xây cây).
   - **Động (Dynamic):** các khoảng được tìm (tại mỗi nút) bằng:
     - **equal interval bucketing**: chia khoảng đều nhau về độ rộng (vd. 0–50K, 50–100K, …);
     - **equal frequency bucketing (percentiles)**: mỗi khoảng chứa số bản ghi bằng nhau (vd. tứ phân vị);
     - **clustering**: gom các giá trị gần nhau (liên hệ Ch 8!).
2. **Quyết định nhị phân (Binary Decision):** $(A < v)$ hoặc $(A \geq v)$
   - xét **mọi cách chia có thể** và tìm **ngưỡng cắt tốt nhất** (best cut);
   - có thể **tốn nhiều tính toán hơn** (compute intensive).

Slide 146 minh họa:
- (i) **Binary split:** "Taxable Income > 80K?" → Yes / No.
- (ii) **Multi-way split:** Taxable Income? → $< 10K$ | $[10K, 25K)$ | $[25K, 50K)$ | $[50K, 80K)$ | $> 80K$.

**Ví dụ equal-width vs equal-frequency (bổ sung):** Income = {60, 70, 75, 85, 90, 95, 100, 120, 125, 220}.
- Equal width 2 khoảng: [60, 140) và [140, 220]: 9 giá trị vs 1 giá trị, rất lệch vì giá trị ngoại lai 220.
- Equal frequency 2 khoảng: ngưỡng ở trung vị ≈ 92.5: 5 vs 5.

**Cách tìm ngưỡng tốt nhất (slide 157–158, phần B; bổ sung tóm tắt):** sắp xếp giá trị, lấy các **điểm giữa** giữa 2 giá trị kề nhau làm ứng viên $v$, với mỗi $v$ tính impurity, chọn $v$ tốt nhất. Chỉ cần sắp xếp một lần rồi quét tuyến tính, cập nhật bảng đếm. Xem mục 7.4c.

---

## 7. Chọn cách chia tốt nhất (slide 147, 148), với ví dụ tính tay đầy đủ

### 7.1 Slide 148: "Which test condition is the best?"
Trước khi chia: **10 bản ghi lớp C0, 10 bản ghi lớp C1** (20 bản ghi).

| Phép thử | Các nút con (C0, C1) |
|---|---|
| **Own Car?** | Yes: (6, 4); No: (4, 6) |
| **Car Type?** | Family: (1, 3); Sports: (8, 0); Luxury: (1, 7) |
| **Student ID?** | c1 … c20: mỗi nút đúng **1 bản ghi** (c1…c10 là C0, c11…c20 là C1) |

**Trực giác:**
- *Own Car*: các con gần như vẫn 50/50 → **gần như vô dụng**.
- *Car Type*: Sports thuần C0, Luxury gần thuần C1 → **tốt**.
- *Student ID*: mọi nút con đều **thuần tuyệt đối** → nhìn "hoàn hảo", nhưng **vô dụng** cho dữ liệu mới (một sinh viên mới có ID chưa từng thấy!). Đây là ví dụ về **overfitting** và **thiên lệch của Information Gain** cho thuộc tính nhiều giá trị.

Slide 149 (đầu phần B) kết luận: theo cách tham lam, ưu tiên các nút có **phân bố lớp đồng nhất (homogeneous)**; cần một **độ đo độ vẩn đục (impurity)** của nút: (C0:5, C1:5) = không đồng nhất, **vẩn đục cao**; (C0:9, C1:1) = đồng nhất, **vẩn đục thấp**.

Kết quả tính (bổ sung, chi tiết công thức ở 7.2):

| Phép thử | $GINI_{split}$ | $Entropy_{split}$ | Gain (IG) | SplitInfo | Gain Ratio |
|---|---|---|---|---|---|
| (Cha: 10/10) | 0.5 | 1.0 | — | — | — |
| Own Car | 0.480 | 0.971 | 0.029 | 1.000 | 0.029 |
| Car Type | **0.1625** | 0.380 | 0.620 | 1.522 | **0.408** |
| Student ID | 0 | 0 | **1.000** (max!) | $\log_2 20 = 4.322$ | 0.231 |

→ GINI và IG đều "chọn" Student ID (impurity = 0). **Gain Ratio** phạt Student ID (vì có 20 nhánh) và chọn **Car Type**, đúng với trực giác.
(Chi tiết Car Type: Family $GINI = 1 - (1/4)^2 - (3/4)^2 = 0.375$; Sports $= 0$; Luxury $= 1 - (1/8)^2 - (7/8)^2 = 14/64 = 0.21875$; $GINI_{split} = \tfrac{4}{20}(0.375) + \tfrac{8}{20}(0) + \tfrac{8}{20}(0.21875) = 0.075 + 0.0875 = 0.1625$.)

### 7.2 Các công thức (từ slide 151–163, phần B; Gain Ratio là bổ sung)

Ký hiệu:
- $t$: một nút; $p(j \mid t)$: **tần suất tương đối của lớp $j$ tại nút $t$** = (số bản ghi lớp $j$ ở $t$) / (số bản ghi ở $t$).
- $n_c$: số lớp.
- Nút cha $p$ được chia thành $k$ nút con; $n_i$ = số bản ghi ở con $i$; $n$ = số bản ghi ở nút cha.
- Quy ước: $0 \log_2 0 = 0$.

**(a) GINI index** (slide 152), dùng trong CART, SLIQ, SPRINT:
$$GINI(t) = 1 - \sum_{j} \big[p(j \mid t)\big]^2$$
- Max $= 1 - \frac{1}{n_c}$ khi các lớp phân bố đều (2 lớp: **0.5**) → ít thông tin nhất.
- Min $= 0$ khi tất cả bản ghi thuộc một lớp → nhiều thông tin nhất.
- Diễn giải trực giác (bổ sung): GINI = **xác suất phân lớp sai** nếu ta bốc ngẫu nhiên một bản ghi trong nút và gán cho nó một nhãn bốc ngẫu nhiên theo phân bố lớp của nút.

**(b) Entropy** (slide 159):
$$Entropy(t) = -\sum_{j} p(j \mid t)\,\log_2 p(j \mid t)$$
- Max $= \log_2 n_c$ (2 lớp: **1**), Min $= 0$.
- Trực giác (bổ sung): số **bit trung bình** cần để mã hóa nhãn lớp của một bản ghi trong nút. Nút thuần = không cần bit nào (đã biết chắc).

**(c) Classification error** (slide 162):
$$Error(t) = 1 - \max_{i} P(i \mid t)$$
- Max $= 1 - \frac{1}{n_c}$ (2 lớp: 0.5), Min $= 0$.
- Trực giác: tỉ lệ sai nếu gán **cả nút** bằng lớp đa số.

**(d) Chất lượng một phép chia** = trung bình **có trọng số** của impurity các con (slide 154):
$$M_{split} = \sum_{i=1}^{k} \frac{n_i}{n}\, M(i) \qquad (M = GINI,\ Entropy\ \text{hoặc}\ Error)$$
Slide 151: $\text{Gain} = M_0 - M_{12}$ so với $M_0 - M_{34}$: chọn phép chia có **gain lớn nhất**, tức là **impurity sau chia nhỏ nhất** (vì $M_0$ của nút cha là chung cho mọi phép thử).

**(e) Information Gain** (slide 161), dùng trong ID3, C4.5:
$$GAIN_{split} = Entropy(p) - \sum_{i=1}^{k} \frac{n_i}{n}\, Entropy(i)$$
Chọn phép chia **cực đại GAIN**. Nhược điểm (slide 161): **có xu hướng chọn phép chia có nhiều nhánh, mỗi nhánh nhỏ nhưng thuần**.

**(f) Gain Ratio** (bổ sung, không có trong slide; theo sách Tan §4.3.4 / C4.5):
$$SplitINFO = -\sum_{i=1}^{k} \frac{n_i}{n} \log_2 \frac{n_i}{n}, \qquad GainRATIO_{split} = \frac{GAIN_{split}}{SplitINFO}$$
SplitINFO chính là entropy của **kích thước các nhánh** (không quan tâm lớp): càng nhiều nhánh nhỏ đều nhau → SplitINFO càng lớn → bị **phạt** càng nặng. $k$ nhánh bằng nhau thì $SplitINFO = \log_2 k$.

**Bảng $\log_2$ dùng trong bài (nên chép vào tờ A4):**

| $x$ | 1/10 | 1/8 | 1/6 | 1/5 | 1/4 | 2/7 | 0.3 | 1/3 | 0.4 | 3/7 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\log_2 x$ | −3.3219 | −3 | −2.5850 | −2.3219 | −2 | −1.8074 | −1.7370 | −1.5850 | −1.3219 | −1.2224 |

| $x$ | 4/7 | 0.6 | 2/3 | 0.7 | 5/7 | 3/4 | 0.8 | 5/6 | 7/8 |
|---|---|---|---|---|---|---|---|---|---|
| $\log_2 x$ | −0.8074 | −0.7370 | −0.5850 | −0.5146 | −0.4854 | −0.4150 | −0.3219 | −0.2630 | −0.1926 |

Máy tính không có $\log_2$: $\log_2 x = \dfrac{\ln x}{\ln 2} \approx \dfrac{\ln x}{0.6931}$.

**Entropy nhị phân hay gặp** $H(a, b)$ với 2 lớp (đếm $a$, $b$):
$H(1,1) = 1$; $H(1,2) = 0.9183$; $H(1,3) = 0.8113$; $H(1,4) = 0.7219$; $H(2,3) = 0.9710$; $H(3,4) = 0.9852$; $H(2,5) = 0.8631$; $H(1,5) = 0.6500$; $H(1,7) = 0.5436$; $H(3,7) = 0.8813$; $H(1,9) = 0.4690$.

**GINI nhị phân hay gặp:** $G(1,1)=0.5$; $G(1,2)=G(2,4)=4/9=0.444$; $G(1,3)=0.375$; $G(1,4)=0.32$; $G(2,3)=0.48$; $G(3,4)=24/49=0.490$; $G(2,5)=20/49=0.408$; $G(1,5)=10/36=0.278$; $G(3,7)=0.42$.

---

### 7.3 Bài tập mẫu chính: 10 bản ghi, 2 lớp, 3 thuộc tính (tự thiết kế để luyện thi)

Bài toán: dự đoán **Đi chơi (Play) = Yes/No**.

| # | Trời (Outlook) | Độ ẩm (Humidity) | Gió (Wind) | **Play** |
|---|---|---|---|---|
| 1 | Nắng | Cao | Yếu | No |
| 2 | Nắng | Cao | Mạnh | No |
| 3 | Mây | Cao | Yếu | Yes |
| 4 | Mưa | Cao | Yếu | Yes |
| 5 | Mưa | BT | Yếu | Yes |
| 6 | Mưa | BT | Mạnh | No |
| 7 | Mây | BT | Mạnh | Yes |
| 8 | Nắng | Cao | Yếu | No |
| 9 | Nắng | BT | Yếu | Yes |
| 10 | Mưa | BT | Yếu | Yes |

(BT = bình thường.) Tổng: **6 Yes, 4 No**.

#### Bước 0: impurity của nút gốc
- $p(Yes) = 0.6$, $p(No) = 0.4$.
- $GINI = 1 - 0.6^2 - 0.4^2 = 1 - 0.36 - 0.16 = \mathbf{0.48}$
- $Entropy = -0.6\log_2 0.6 - 0.4\log_2 0.4 = 0.6(0.7370) + 0.4(1.3219) = 0.4422 + 0.5288 = \mathbf{0.9710}$
- $Error = 1 - \max(0.6, 0.4) = \mathbf{0.4}$

#### Bước 1: bảng đếm (count matrix) cho từng thuộc tính

| Outlook | Nắng | Mây | Mưa |
|---|---|---|---|
| Yes | 1 | 2 | 3 |
| No | 3 | 0 | 1 |
| $n_i$ | 4 | 2 | 4 |

| Humidity | Cao | BT |
|---|---|---|
| Yes | 2 | 4 |
| No | 3 | 1 |

| Wind | Yếu | Mạnh |
|---|---|---|
| Yes | 5 | 1 |
| No | 2 | 2 |

#### Bước 2: GINI

**Outlook** (multi-way):
- Nắng (1,3): $1 - (1/4)^2 - (3/4)^2 = 1 - 0.0625 - 0.5625 = 0.375$
- Mây (2,0): $1 - 1 - 0 = 0$
- Mưa (3,1): $0.375$
- $GINI_{split} = \frac{4}{10}(0.375) + \frac{2}{10}(0) + \frac{4}{10}(0.375) = 0.15 + 0 + 0.15 = \mathbf{0.300}$

**Humidity:**
- Cao (2,3): $1 - 0.4^2 - 0.6^2 = 0.48$
- BT (4,1): $1 - 0.8^2 - 0.2^2 = 1 - 0.64 - 0.04 = 0.32$
- $GINI_{split} = 0.5(0.48) + 0.5(0.32) = \mathbf{0.400}$

**Wind:**
- Yếu (5,2): $1 - (5/7)^2 - (2/7)^2 = 1 - 25/49 - 4/49 = 20/49 = 0.4082$
- Mạnh (1,2): $1 - 1/9 - 4/9 = 4/9 = 0.4444$
- $GINI_{split} = 0.7(0.4082) + 0.3(0.4444) = 0.2857 + 0.1333 = \mathbf{0.4190}$

→ Gain GINI: Outlook $0.48 - 0.30 = 0.18$; Humidity $0.08$; Wind $0.061$. **Chọn Outlook.**

#### Bước 3: Entropy và Information Gain

**Outlook:**
- Nắng (1,3): $-\tfrac14\log_2\tfrac14 - \tfrac34\log_2\tfrac34 = 0.25(2) + 0.75(0.4150) = 0.5 + 0.3113 = 0.8113$
- Mây (2,0): $0$
- Mưa (3,1): $0.8113$
- $Entropy_{split} = 0.4(0.8113) + 0.2(0) + 0.4(0.8113) = 0.6490$
- $GAIN = 0.9710 - 0.6490 = \mathbf{0.3219}$

**Humidity:**
- Cao (2,3): $0.4(1.3219) + 0.6(0.7370) = 0.5288 + 0.4422 = 0.9710$
- BT (4,1): $0.8(0.3219) + 0.2(2.3219) = 0.2575 + 0.4644 = 0.7219$
- $Entropy_{split} = 0.5(0.9710) + 0.5(0.7219) = 0.8464$
- $GAIN = 0.9710 - 0.8464 = \mathbf{0.1245}$

**Wind:**
- Yếu (5,2): $\tfrac57(0.4854) + \tfrac27(1.8074) = 0.3467 + 0.5164 = 0.8631$
- Mạnh (1,2): $\tfrac13(1.5850) + \tfrac23(0.5850) = 0.5283 + 0.3900 = 0.9183$
- $Entropy_{split} = 0.7(0.8631) + 0.3(0.9183) = 0.6042 + 0.2755 = 0.8797$
- $GAIN = 0.9710 - 0.8797 = \mathbf{0.0913}$

→ **Chọn Outlook** (IG lớn nhất).

#### Bước 4: Gain Ratio (bổ sung)
- Outlook: nhánh 4/2/4 → $SplitINFO = -2(0.4\log_2 0.4) - 0.2\log_2 0.2 = 2(0.5288) + 0.4644 = 1.5219$ → $GR = 0.3219 / 1.5219 = \mathbf{0.2115}$
- Humidity: nhánh 5/5 → $SplitINFO = 1$ → $GR = \mathbf{0.1245}$
- Wind: nhánh 7/3 → $SplitINFO = 0.7(0.5146) + 0.3(1.7370) = 0.8813$ → $GR = 0.0913 / 0.8813 = \mathbf{0.1036}$

→ Vẫn **chọn Outlook**, nhưng khoảng cách với các thuộc tính khác thu hẹp lại (vì Outlook có 3 nhánh nên bị phạt nhiều hơn).

#### Bước 5: Classification error
- Outlook: Nắng $1 - 3/4 = 0.25$; Mây $0$; Mưa $0.25$ → $0.4(0.25) + 0 + 0.4(0.25) = \mathbf{0.20}$ (gain 0.20)
- Humidity: Cao $1 - 0.6 = 0.4$; BT $1 - 0.8 = 0.2$ → $0.5(0.4) + 0.5(0.2) = \mathbf{0.30}$ (gain 0.10)
- Wind: Yếu $2/7$; Mạnh $1/3$ → $0.7(2/7) + 0.3(1/3) = 0.2 + 0.1 = \mathbf{0.30}$ (gain 0.10)

→ Chọn Outlook. Nhưng chú ý: **Error không phân biệt được Humidity và Wind** (cả hai 0.30), trong khi GINI/entropy đều thấy Humidity tốt hơn. Error **kém nhạy**.

#### Bảng tổng kết nút gốc

| Thuộc tính | $GINI_{split}$ ↓ | $Entropy_{split}$ ↓ | IG ↑ | SplitINFO | Gain Ratio ↑ | $Error_{split}$ ↓ |
|---|---|---|---|---|---|---|
| **Outlook** | **0.300** | **0.649** | **0.322** | 1.522 | **0.212** | **0.20** |
| Humidity | 0.400 | 0.846 | 0.125 | 1.000 | 0.125 | 0.30 |
| Wind | 0.419 | 0.880 | 0.091 | 0.881 | 0.104 | 0.30 |

**Thêm: nếu dùng chia nhị phân cho Outlook (kiểu CART).** Có $2^{3-1} - 1 = 3$ cách:
| Cách chia | (Yes,No) mỗi bên | $GINI_{split}$ |
|---|---|---|
| {Nắng} vs {Mây, Mưa} | (1,3) / (5,1) | $0.4(0.375) + 0.6(1 - 25/36 - 1/36 = 0.2778) = 0.150 + 0.1667 = \mathbf{0.3167}$ |
| {Mây} vs {Nắng, Mưa} | (2,0) / (4,4) | $0.2(0) + 0.8(0.5) = 0.400$ |
| {Mưa} vs {Nắng, Mây} | (3,1) / (3,3) | $0.4(0.375) + 0.6(0.5) = 0.450$ |
→ Cách nhị phân tốt nhất: {Nắng} vs {Mây, Mưa} (0.3167), vẫn tệ hơn multi-way (0.300). Điều này luôn đúng (bổ sung): **multi-way luôn có impurity ≤ mọi cách gộp nhị phân của nó**, vì gộp nhánh không bao giờ làm giảm impurity. Đó chính là "lợi thế không công bằng" của nhiều nhánh.

#### Bước 6: xây các tầng tiếp theo (đệ quy Hunt)
Gốc = **Outlook**:
- **Mây** {3, 7}: (2 Yes, 0 No) → **thuần** → **lá Yes**.
- **Nắng** {1, 2, 8, 9}: (1 Yes, 3 No) → còn vẩn đục, chia tiếp. Chỉ xét Humidity và Wind **trên 4 bản ghi này**:
  - Humidity: Cao {1,2,8} = (0,3); BT {9} = (1,0) → $GINI_{split} = 0$, $Entropy_{split} = 0$, $IG = 0.8113$ (= entropy nút Nắng).
  - Wind: Yếu {1,8,9} = (1,2); Mạnh {2} = (0,1) → $GINI_{split} = 0.75(0.4444) = 0.3333$; $Entropy_{split} = 0.75(0.9183) = 0.6887$; $IG = 0.8113 - 0.6887 = 0.1226$.
  - → **Chọn Humidity**: Cao → **No**, BT → **Yes** (cả hai thuần).
- **Mưa** {4, 5, 6, 10}: (3 Yes, 1 No):
  - Humidity: Cao {4} = (1,0); BT {5,6,10} = (2,1) → $GINI_{split} = 0.75(0.4444) = 0.3333$; $IG = 0.1226$.
  - Wind: Yếu {4,5,10} = (3,0); Mạnh {6} = (0,1) → $GINI_{split} = 0$; $IG = 0.8113$.
  - → **Chọn Wind**: Yếu → **Yes**, Mạnh → **No**.

**Cây cuối cùng:**
```
                    Outlook
           Nắng/      |Mây      \Mưa
          Humidity    YES        Wind
        Cao/   \BT            Yếu/  \Mạnh
        NO     YES            YES    NO
```
Kiểm tra: 10/10 bản ghi được phân lớp đúng (training error = 0).
Áp dụng (deduction) cho bản ghi mới (Mưa, Cao, Mạnh): Outlook = Mưa → Wind = Mạnh → **No**. Humidity không được dùng tới.

Nhận xét: ở nút Nắng, với Wind, $\Delta Error = 0.25 - 0.75 \times \tfrac13 = 0$ trong khi $\Delta GINI = 0.0417 > 0$. Lại thấy classification error "mù" với cải thiện nhỏ.

#### Bước 7: thuộc tính ID (minh họa thiên lệch của IG)
Giả sử thêm cột **ID** (1…10). Chia theo ID: 10 nhánh, mỗi nhánh 1 bản ghi, đều thuần.
- $GINI_{split} = 0$, $Entropy_{split} = 0$, $IG = 0.9710$, **cao nhất có thể** (bằng entropy gốc) → IG "chọn" ID. Sai lầm!
- $SplitINFO = \log_2 10 = 3.3219$ → $GR = 0.971/3.322 = 0.292$.
- Lưu ý trung thực: với chỉ 10 bản ghi, GR(ID) = 0.292 **vẫn lớn hơn** GR(Outlook) = 0.212. Gain Ratio **giảm** thiên lệch chứ **không loại bỏ hoàn toàn**, đặc biệt khi $n$ nhỏ (với $n$ lớn, $\log_2 n$ lớn nên phạt nặng hơn, như ở slide 148 với $n = 20$, Car Type đã thắng Student ID). Trong thực tế, **loại các thuộc tính định danh (ID) trước khi học** (bổ sung).

---

### 7.4 Bài tập thứ hai: chính bộ "Cheat" của slide (3 Yes / 7 No)

Gốc: $GINI = 1 - 0.3^2 - 0.7^2 = 0.42$; $Entropy = 0.3(1.7370) + 0.7(0.5146) = 0.5211 + 0.3602 = 0.8813$; $Error = 0.3$.

**(a) Refund:** Yes (0 Yes, 3 No); No (3 Yes, 4 No)
- GINI: Yes $= 0$; No $= 1 - 9/49 - 16/49 = 24/49 = 0.4898$ → $GINI_{split} = 0.7(0.4898) = \mathbf{0.343}$
- Entropy: No $= \tfrac37(1.2224) + \tfrac47(0.8074) = 0.5239 + 0.4614 = 0.9852$ → $0.7(0.9852) = 0.6897$ → $IG = \mathbf{0.192}$
- SplitINFO $= H(0.3, 0.7) = 0.8813$ → $GR = 0.217$
- Error: $0.7 \times 3/7 = \mathbf{0.30}$ → gain **0**!

**(b) Marital Status** — Single (2 Yes, 2 No), Married (0, 4), Divorced (1, 1)
- Multi-way: $GINI_{split} = 0.4(0.5) + 0.4(0) + 0.2(0.5) = \mathbf{0.300}$; $Entropy_{split} = 0.4(1) + 0 + 0.2(1) = 0.6$ → $IG = \mathbf{0.281}$; SplitINFO $= H(0.4, 0.4, 0.2) = 1.5219$ → $GR = 0.185$.
- Nhị phân {Married} vs {Single, Divorced}: (0,4) / (3,3) → $GINI_{split} = 0.6(0.5) = \mathbf{0.300}$; $IG = 0.281$; SplitINFO $= H(0.4, 0.6) = 0.971$ → $GR = 0.290$.
- (Các cách khác: {Single} vs {M, D} → 0.367; {Divorced} vs {S, M} → 0.400.)

**(c) Taxable Income** (liên tục; sắp xếp: 60 N, 70 N, 75 N, 85 Y, 90 Y, 95 Y, 100 N, 120 N, 125 N, 220 N). Thử các ngưỡng ở điểm giữa:

| $v$ | ≤v (Y,N) | >v (Y,N) | $GINI_{split}$ |
|---|---|---|---|
| 65 | (0,1) | (3,6) | 0.400 |
| 72.5 | (0,2) | (3,5) | 0.375 |
| 80 | (0,3) | (3,4) | 0.343 |
| 87.5 | (1,3) | (2,4) | 0.417 |
| 92.5 | (2,3) | (1,4) | 0.400 |
| **97.5** | **(3,3)** | **(0,4)** | **0.300** |
| 110 | (3,4) | (0,3) | 0.343 |
| 122.5 | (3,5) | (0,2) | 0.375 |
| 172.5 | (3,6) | (0,1) | 0.400 |

→ Ngưỡng tốt nhất **≈ 97** (slide 158 ghi split position **97**, Gini **0.300**, khớp với ta). $IG(\le 97) = 0.281$, $GR = 0.290$.
Mẹo (bổ sung): ngưỡng tối ưu chỉ có thể nằm ở **ranh giới đổi lớp** (giữa 75→85 và 95→100); không cần thử ngưỡng giữa hai bản ghi cùng lớp.

**Tổng kết bộ Cheat:**

| Phép thử | GINI ↓ | IG ↑ | GR ↑ | Error ↓ |
|---|---|---|---|---|
| Refund | 0.343 | 0.192 | 0.217 | 0.30 |
| Marital (3 nhánh) | **0.300** | **0.281** | 0.185 | 0.30 |
| Marital {M} vs {S,D} | **0.300** | **0.281** | **0.290** | 0.30 |
| Income ≤ 97 | **0.300** | **0.281** | **0.290** | 0.30 |

Bài học:
1. Theo GINI/IG, **Refund không phải lựa chọn tốt nhất ở gốc**. Slide 139 chọn Refund chỉ để minh họa cơ chế đệ quy của Hunt, không phải kết quả tối ưu hóa.
2. **Hòa (ties)**: Marital và Income ≤ 97 hòa nhau trên GINI/IG; Gain Ratio ưu tiên phép chia 2 nhánh hơn phép chia 3 nhánh. Khi thi, nếu hòa thì nói rõ là hòa và nêu quy tắc phá hòa (ví dụ: ít nhánh hơn, hoặc thứ tự thuộc tính).
3. **Classification error = 0.30 cho MỌI phép thử** (gain = 0): mọi nút con đều vẫn có đa số là "No", nên số lỗi không đổi. Đây là lý do error **không nên dùng để xây cây** (nó dùng tốt cho cắt tỉa/đánh giá).

---

## 8. Phân tích sâu / đánh giá

**Tại sao cần độ đo impurity?** Greedy cần một **con số** để so sánh các phép thử. Ý tưởng: phép chia tốt là phép chia làm các con **thuần hơn** cha. Gain = impurity(cha) − trung bình có trọng số impurity(con) ≥ 0 (với GINI/entropy luôn ≥ 0, do tính lõm; bổ sung).

**Tại sao trọng số $n_i/n$?** Một nút con thuần nhưng chỉ có 1 bản ghi không nên quan trọng bằng một nút con thuần có 100 bản ghi. Slide 155: *"Larger and purer partitions are sought for."*

**So sánh 3 độ đo (2 lớp, theo $p$ = tỉ lệ lớp 1; slide 164):**
| | Công thức 2 lớp | Max (tại $p=0.5$) | Hình dạng |
|---|---|---|---|
| Entropy | $-p\log_2 p - (1-p)\log_2(1-p)$ | 1 | cong nhất |
| GINI | $2p(1-p)$ | 0.5 | parabol |
| Error | $\min(p, 1-p)$ | 0.5 | hình chữ V (tuyến tính từng khúc) |
- Cả 3 đều = 0 khi thuần, cực đại khi đều; **thứ tự xếp hạng thường giống nhau** (GINI ≈ entropy trong thực tế).
- Error tuyến tính → trung bình có trọng số của các con thường **bằng** error của cha → gain = 0 dù các con đã thuần hơn (ví dụ 7.4). GINI/entropy **lõm thực sự** nên thưởng cho cả cải thiện nhỏ.
- Entropy phạt mạnh hơn khi gần thuần (độ dốc lớn gần 0) và tốn log; GINI rẻ hơn (không có log), được CART dùng.

**Thiên lệch của Information Gain** (slide 161): thuộc tính nhiều giá trị (ID, ngày sinh, mã bưu điện…) cắt dữ liệu thành nhiều mảnh nhỏ → mỗi mảnh dễ "thuần do ngẫu nhiên" → IG cao giả tạo → cây overfit, không tổng quát hóa. Khắc phục: **Gain Ratio** (C4.5, bổ sung), **chỉ dùng phép chia nhị phân** (CART), hoặc loại thuộc tính ID.

**Ưu điểm của cây quyết định** (slide 167, phần B): rẻ khi xây; **phân lớp cực nhanh**; **dễ diễn giải** khi cây nhỏ; độ chính xác tương đương các kỹ thuật khác trên nhiều bộ dữ liệu đơn giản. Thêm (bổ sung): xử lý được cả thuộc tính định danh lẫn liên tục; không cần chuẩn hóa dữ liệu (khác k-means/k-NN!); tự chọn thuộc tính quan trọng.

**Nhược điểm / cạm bẫy (bổ sung, một phần ở slide 168–176):**
- **Overfitting**: cây phát triển hết cỡ khớp cả nhiễu → cần pre-pruning / post-pruning.
- **Greedy, không tối ưu toàn cục**; bỏ lỡ tương tác giữa thuộc tính (XOR).
- **Không ổn định**: thay đổi nhỏ dữ liệu có thể đổi thuộc tính gốc → cả cây khác.
- **Ranh giới quyết định song song trục (axis-parallel)**: mỗi phép thử chỉ dùng 1 thuộc tính, nên ranh giới chéo như $x + y < 1$ phải xấp xỉ bằng nhiều "bậc thang".
- **Data fragmentation**: càng xuống sâu càng ít bản ghi → quyết định dựa trên rất ít dữ liệu, kém tin cậy.
- Tìm ngưỡng cho thuộc tính liên tục tốn kém nếu làm ngây thơ, $O(n^2)$; sắp xếp + quét thì $O(n \log n)$.

---

## 9. Dễ nhầm lẫn

1. **Induction vs Deduction:** induction = **học** mô hình từ training set; deduction = **áp dụng** mô hình lên test set. Đừng đảo ngược.
2. **Training set vs test set:** accuracy phải đo trên test set. Training error = 0 (như cây ở 4.2) **không** có nghĩa là mô hình tốt.
3. **Classification vs Clustering:** classification có nhãn lớp cho sẵn (supervised); clustering không có (unsupervised).
4. **Impurity vs Gain:** impurity càng **nhỏ** càng tốt; gain càng **lớn** càng tốt. Chọn $\min M_{split}$ ⇔ $\max Gain$ (vì $M$ của cha cố định).
5. **Quên trọng số $n_i/n$** khi tính $M_{split}$: lỗi phổ biến nhất khi thi! Không lấy trung bình cộng đơn giản.
6. **Đổi cơ số log**: slide 159 viết "log", slide 160 dùng $\log_2$. Dùng **$\log_2$** (entropy tính bằng bit, max = 1 với 2 lớp). Và $0\log 0 = 0$, không phải "lỗi".
7. **Max của GINI là $1 - 1/n_c$**, không phải 1 (2 lớp: 0.5; 3 lớp: 0.667). **Max của entropy là $\log_2 n_c$** (2 lớp: 1; 3 lớp: 1.585). Max của error = $1 - 1/n_c$.
8. **Chia nhị phân ordinal** phải giữ thứ tự: {Small, Large} vs {Medium} là không hợp lệ (slide 144). Nominal thì gom tùy ý.
9. **Hunt: nút rỗng** → lá với lớp mặc định $y_d$, **không** phải bỏ nhánh. **Nút không thuần nhưng tạm gán nhãn đa số** (slide 139, bước 2–3) chỉ là nhãn tạm thời trong quá trình xây.
10. **Thuộc tính đã dùng có được dùng lại không?** Nominal multi-way: không cần (bổ sung: mọi bản ghi trong nhánh có cùng giá trị). Thuộc tính **liên tục** hoặc nhị phân gộp nhóm: **có thể** dùng lại ở nút sâu hơn với ngưỡng khác.
11. **"< 80K / > 80K" trên slide 127** bỏ sót đúng 80K; dùng $< v$ / $\geq v$. Bản ghi test ở slide 130 có 80K nhưng không bị ảnh hưởng vì nó đi nhánh Married.
12. **Gain Ratio không có trong slide** (bổ sung); slide chỉ nêu *nhược điểm* của IG. Nếu đề hỏi "khắc phục thế nào", nêu Gain Ratio (C4.5) và SplitINFO.
13. **Entropy max = 1 và GINI max = 0.5** (2 lớp): đừng so sánh giá trị GINI với giá trị entropy; chỉ so sánh **cùng một độ đo** giữa các phép thử.

---

## 10. Câu hỏi có thể ra thi (kèm lời giải ngắn)

**Q1. Định nghĩa bài toán phân lớp. Phân biệt training set và test set.**
→ Cho tập bản ghi có nhãn lớp, tìm mô hình class = f(các thuộc tính khác) sao cho bản ghi chưa thấy được gán lớp chính xác nhất. Training set để xây mô hình; test set (tách riêng) để ước lượng độ chính xác trên dữ liệu mới.

**Q2. Mô tả thuật toán Hunt.**
→ $D_t$ = các bản ghi tới nút $t$. (1) cùng lớp $y_t$ → lá $y_t$; (2) rỗng → lá lớp mặc định $y_d$; (3) nhiều lớp → chọn phép thử thuộc tính, chia thành tập con, đệ quy. (+ dừng khi các thuộc tính giống hệt nhau → lá lớp đa số.)

**Q3. Cho cây ở slide 127, phân lớp bản ghi (Refund=No, Divorced, 85K).**
→ Refund=No → MarSt=Divorced (nhánh Single, Divorced) → TaxInc: 85K > 80K → **YES**.

**Q4. Liệt kê các cách chia cho thuộc tính nominal / ordinal / continuous.**
→ Nominal: multi-way hoặc binary (gom tùy ý, $2^{k-1}-1$ cách). Ordinal: multi-way hoặc binary **giữ thứ tự** ($k-1$ cách). Continuous: rời rạc hóa (static/dynamic: equal-width, equal-frequency, clustering) hoặc binary $A < v$ / $A \geq v$ (thử mọi $v$).

**Q5. Phép chia {Small, Large} vs {Medium} của Size có hợp lệ không?**
→ Không (với ordinal): phá thứ tự Small < Medium < Large.

**Q6. Tính GINI, entropy, error của nút (C1 = 2, C2 = 4).**
→ $GINI = 1 - (1/3)^2 - (2/3)^2 = 4/9 = 0.444$; $Entropy = \tfrac13(1.585) + \tfrac23(0.585) = 0.918$; $Error = 1 - 2/3 = 1/3$. (Khớp slide 153/160/163.)

**Q7. Bài toán đầy đủ:** cho bảng 10 bản ghi (như mục 7.3), tính GINI_split / IG / Gain Ratio cho từng thuộc tính, chọn thuộc tính gốc và xây cây.
→ Xem mục 7.3: Outlook (GINI 0.300, IG 0.322, GR 0.212) → con: Mây = Yes; Nắng → Humidity; Mưa → Wind.

**Q8. Tại sao Information Gain ưa thuộc tính nhiều giá trị? Ví dụ và cách khắc phục.**
→ Nhiều nhánh nhỏ dễ thuần → entropy con ≈ 0 → IG ≈ max. Ví dụ Student ID (slide 148): IG = 1 (max) nhưng vô dụng. Khắc phục: Gain Ratio = IG / SplitINFO (SplitINFO = $\log_2 20 = 4.32$ cho Student ID → GR = 0.23 < GR(Car Type) = 0.41); hoặc ép chia nhị phân; hoặc bỏ thuộc tính ID.

**Q9. Tại sao không nên dùng classification error để chọn phép chia?**
→ Nó tuyến tính từng khúc nên thường cho gain = 0 dù các nút con thuần hơn (ví dụ bộ Cheat: mọi phép thử đều có error_split = 0.30 = error cha). GINI/entropy là hàm lõm thực sự nên nhạy hơn.

**Q10. Tìm ngưỡng tốt nhất cho Taxable Income (bộ Cheat) theo GINI.**
→ Sắp xếp, thử các điểm giữa, cập nhật bảng đếm; tốt nhất $v \approx 97$: (3Y,3N) | (0Y,4N), $GINI_{split} = 0.6 \times 0.5 = 0.300$.

**Q11. Tại sao có thể có nhiều cây cùng khớp dữ liệu, và chọn cây nào?**
→ Thứ tự / lựa chọn thuộc tính khác nhau đều có thể cho training error = 0 (slide 127 vs 128). Ưu tiên cây đơn giản hơn (Occam's Razor, slide 173) vì tổng quát hóa tốt hơn; tìm cây tối ưu là bài toán NP-khó nên dùng greedy.

**Q12. Giá trị max/min của GINI, entropy, error với $n_c$ lớp?**
→ Min = 0 cả ba (nút thuần). Max: GINI $1 - 1/n_c$; Entropy $\log_2 n_c$; Error $1 - 1/n_c$ (đạt khi phân bố đều).

---

## 11. Tóm tắt cho tờ A4

**Classification:** training set (records + attributes, 1 attr = class) → học model class = f(attrs) (**induction**) → áp dụng lên test set (**deduction**); accuracy đo trên **test set**. Supervised (khác clustering).
**Kỹ thuật:** Decision tree, Rule-based, Memory-based (k-NN), Neural Nets, Naïve Bayes / Bayesian Belief Nets, SVM.
**Thuật toán cây:** Hunt (gốc), CART (GINI, nhị phân), ID3 / C4.5 (entropy / IG / GainRatio), SLIQ, SPRINT (GINI).
**Áp dụng cây:** gốc → theo nhánh khớp giá trị → lá = nhãn. Mỗi đường = 1 luật IF-THEN.

**Hunt($D_t$):** cùng lớp $y_t$ → lá $y_t$ | rỗng → lá $y_d$ (đa số của cha) | thuộc tính giống hệt → lá đa số | nếu không: chọn phép thử tốt nhất, chia, đệ quy. Greedy, top-down, không quay lui.
**Issues:** (1) cách chia: điều kiện kiểm tra + chọn phép tốt nhất; (2) khi nào dừng.

**Điều kiện kiểm tra:**
- Nominal: multi-way hoặc binary (gom tùy ý; $2^{k-1}-1$ cách).
- Ordinal: multi-way hoặc binary **giữ thứ tự** ($k-1$ cách); {S,L}|{M} sai.
- Continuous: discretization (static / dynamic: equal-width, equal-freq, clustering) hoặc binary $A<v$ / $A \ge v$ (sort, thử midpoints, chỉ cần ở chỗ đổi lớp).

**Công thức** ($p(j|t)$ = tần suất lớp $j$ ở nút $t$; $0\log 0 = 0$):
- $GINI(t) = 1 - \sum_j p(j|t)^2$: max $1 - 1/n_c$ (2 lớp: 0.5), min 0
- $Entropy(t) = -\sum_j p(j|t)\log_2 p(j|t)$: max $\log_2 n_c$ (2 lớp: 1), min 0
- $Error(t) = 1 - \max_i p(i|t)$: max $1 - 1/n_c$, min 0
- $M_{split} = \sum_{i=1}^{k} \frac{n_i}{n} M(i)$ (**trọng số!**); Gain = $M(cha) - M_{split}$ → max
- $IG = Entropy(p) - \sum \frac{n_i}{n} Entropy(i)$: thiên lệch về nhiều nhánh nhỏ thuần
- $SplitINFO = -\sum \frac{n_i}{n}\log_2\frac{n_i}{n}$ ($k$ nhánh đều: $\log_2 k$); $GainRatio = IG / SplitINFO$ (bổ sung, C4.5)
- 2 lớp: $GINI = 2p(1-p)$; Error $= \min(p, 1-p)$; Entropy > GINI ≥ Error. Error kém nhạy (gain thường = 0).
- $\log_2 x = \ln x / 0.6931$

**log2:** 1/8 → −3 | 1/6 → −2.585 | 1/5 → −2.322 | 1/4 → −2 | 2/7 → −1.807 | 0.3 → −1.737 | 1/3 → −1.585 | 0.4 → −1.322 | 3/7 → −1.222 | 4/7 → −0.807 | 0.6 → −0.737 | 2/3 → −0.585 | 0.7 → −0.515 | 5/7 → −0.485 | 3/4 → −0.415 | 0.8 → −0.322 | 5/6 → −0.263 | 7/8 → −0.193
**H(a,b):** (1,1)=1 | (1,2)=.918 | (1,3)=.811 | (1,4)=.722 | (2,3)=.971 | (3,4)=.985 | (2,5)=.863 | (1,5)=.650 | (1,7)=.544 | (3,7)=.881
**G(a,b):** (1,1)=.5 | (1,2)=.444 | (1,3)=.375 | (1,4)=.32 | (2,3)=.48 | (3,4)=.490 | (2,5)=.408 | (1,5)=.278 | (3,7)=.42

**Quy trình thi:** (1) đếm lớp ở cha → impurity cha; (2) bảng đếm cho từng thuộc tính / cách chia; (3) impurity từng con; (4) trung bình **có trọng số**; (5) gain (+ SplitINFO, GR nếu hỏi); (6) chọn max gain; (7) con thuần → lá, con không thuần → lặp lại **chỉ trên bản ghi của con đó**.
**Bộ Cheat (3Y/7N):** GINI 0.42, H 0.881; Refund 0.343; Marital 0.300; Income ≤ 97 → 0.300 (slide 158); Error = 0.30 cho tất cả.
**Ưu điểm cây:** rẻ, dự đoán nhanh, dễ hiểu, chính xác tương đương. **Nhược:** overfitting, greedy, không ổn định, ranh giới song song trục, bias IG.


---

# Chương 4 – Phân lớp (Classification), phần B: Độ đo tạp chất, tiêu chí chia, quá khớp & cắt tỉa (slides 149–176)

> **Phạm vi thực tế của các slide 149–176** (đã đọc từng trang):
> - 149–164: cách chọn **phép chia tốt nhất (best split)** bằng các **độ đo tạp chất (impurity measures)**: Gini, Entropy / Information Gain, Classification Error; cách áp dụng cho thuộc tính nhị phân, định danh (categorical), liên tục (continuous); so sánh 3 độ đo.
> - 165–167: **tiêu chí dừng (stopping criteria)** và ưu điểm của cây quyết định.
> - 168–176: **các vấn đề thực tế**: dưới khớp / quá khớp (underfitting / overfitting), quá khớp do nhiễu và do thiếu dữ liệu, **dao cạo Occam (Occam's Razor)**, **MDL**, **cắt tỉa trước (pre-pruning)** và **cắt tỉa sau (post-pruning)**.
>
> ⚠️ **Lưu ý quan trọng:** Bộ slide **kết thúc ở slide 176 (post-pruning)**. Các chủ đề *ma trận nhầm lẫn (confusion matrix), accuracy, precision/recall, cost matrix, holdout, cross-validation, bootstrap, ROC* **KHÔNG có trong slide**. Slide 168 có nhắc "Missing Values" và "Costs of Classification" nhưng không có slide nào trình bày chi tiết. Mình vẫn viết một phụ lục ngắn ở cuối (đánh dấu **(bổ sung)**) vì chúng có thể xuất hiện trong TD hoặc câu hỏi tổng quát — nhưng hãy ưu tiên ôn phần có trong slide.

---

## 0. Nhắc lại bối cảnh (slides 147–149)

**Slide 147 – Tree Induction (quy nạp cây).** Thuật toán xây cây (Hunt, CART, ID3, C4.5…) dùng **chiến lược tham lam (greedy strategy)**: tại mỗi nút, chọn **một** phép kiểm tra thuộc tính (attribute test) tối ưu một tiêu chí nào đó *ngay tại bước đó*, không quay lui. Ba câu hỏi lớn:
1. Đặc tả điều kiện kiểm tra thế nào? (đã học ở phần trước – binary/multi-way split)
2. **Làm sao xác định phép chia tốt nhất?** ← phần này (chữ đỏ trên slide)
3. Khi nào dừng chia? (slide 165–166)

**Slide 148 – Ví dụ dẫn nhập** (thuộc phần trước, nhắc lại vì slide 161 dùng lại ý này): trước khi chia có 10 bản ghi lớp C0 và 10 bản ghi lớp C1. Ba cách chia:
- *Own Car?* → Yes: (C0:6, C1:4), No: (C0:4, C1:6) — gần như chẳng tách được gì.
- *Car Type?* → Family (1,3), Sports (8,0), Luxury (1,7) — khá "sạch".
- *Student ID?* → 20 nhánh, mỗi nhánh 1 bản ghi → **hoàn toàn sạch** nhưng vô dụng (ID không tổng quát hóa cho sinh viên mới!).

**Slide 149 – Ý tưởng cốt lõi.** Cách tham lam ưu tiên các nút có **phân bố lớp đồng nhất (homogeneous)**. Cần một **độ đo tạp chất (measure of node impurity)**:
- (C0:5, C1:5): **không đồng nhất**, tạp chất **cao** (50/50, đoán kiểu gì cũng sai một nửa).
- (C0:9, C1:1): **đồng nhất**, tạp chất **thấp** (gần như chắc chắn là C0).

> **Trực giác:** Giống như phân loại trái cây vào giỏ. Một giỏ chứa toàn táo là "sạch" (impurity = 0); giỏ nửa táo nửa cam là "bẩn" nhất. Mỗi câu hỏi (phép chia) tốt là câu hỏi làm các giỏ con sạch hơn giỏ cha.

---

## 1. Ba độ đo tạp chất (slide 150)

Slide 150 liệt kê: **Gini Index**, **Entropy**, **Misclassification error** (lỗi phân lớp sai). Cả ba đều:
- = 0 khi nút thuần khiết (một lớp duy nhất),
- đạt cực đại khi các lớp phân bố đều.

Ký hiệu chung: $p(j\mid t)$ = **tần suất tương đối (relative frequency)** của lớp $j$ tại nút $t$ = (số bản ghi lớp $j$ ở nút $t$) / (tổng số bản ghi ở nút $t$). $n_c$ = số lớp.

---

## 2. Khung tổng quát tìm phép chia tốt nhất (slide 151)

Hình trên slide:
- Trước khi chia: nút cha có số đếm (N00, N01) → tạp chất **M0**.
- Chia theo A: hai nút con N1 (N10, N11), N2 (N20, N21) → tạp chất M1, M2 → gộp (trung bình có trọng số) thành **M12**.
- Chia theo B: N3, N4 → M3, M4 → gộp thành **M34**.
- So sánh: $\text{Gain} = M0 - M12$ **vs** $M0 - M34$.

**Quy tắc:** chọn phép chia có **Gain lớn nhất** ⇔ tạp chất sau chia (M12 hay M34) **nhỏ nhất** (vì M0 giống nhau cho mọi ứng viên tại cùng nút).

> **Phân tích sâu:** Vì M0 cố định tại một nút, trong thực tế chỉ cần so sánh tạp chất có trọng số của các nút con. "Gain" chỉ quan trọng khi muốn biết phép chia *có cải thiện hay không* (ví dụ dùng để dừng sớm – slide 175: "dừng nếu không cải thiện Gini/information gain").

---

## 3. Chỉ số Gini (Gini Index) – slides 152–153

### 3.1 Định nghĩa (slide 152)
$$GINI(t) = 1 - \sum_j \big[p(j\mid t)\big]^2$$

- $p(j\mid t)$: tần suất tương đối của lớp $j$ tại nút $t$.
- **Cực đại** $= 1 - \frac{1}{n_c}$ khi các bản ghi phân bố đều giữa các lớp → "ít thông tin thú vị nhất" (least interesting information). Với 2 lớp: max = 0.5.
- **Cực tiểu** $= 0$ khi mọi bản ghi thuộc một lớp → "thông tin thú vị nhất".

**Ý nghĩa trực giác (bổ sung):** $\sum_j p_j^2$ là xác suất để **hai bản ghi rút ngẫu nhiên (có hoàn lại) cùng lớp**. Vậy Gini = xác suất hai bản ghi ngẫu nhiên **khác lớp** = xác suất "gán nhãn sai" nếu ta gán nhãn ngẫu nhiên theo phân bố của nút.

### 3.2 Ví dụ trên slide 152–153 (6 bản ghi, 2 lớp)

| C1 | C2 | $p(C1)$ | $p(C2)$ | Gini |
|---|---|---|---|---|
| 0 | 6 | 0 | 1 | $1-0-1 = 0$ |
| 1 | 5 | 1/6 | 5/6 | $1 - \frac{1}{36} - \frac{25}{36} = \frac{10}{36} = 0.278$ |
| 2 | 4 | 2/6 | 4/6 | $1 - \frac{4}{36} - \frac{16}{36} = \frac{16}{36} = 0.444$ |
| 3 | 3 | 1/2 | 1/2 | $1 - \frac14 - \frac14 = 0.5$ (max) |

Đã kiểm tra lại: đúng như slide.

> **Công thức nhanh cho 2 lớp (bổ sung):** nếu $p$ là tỉ lệ một lớp thì $GINI = 1 - p^2 - (1-p)^2 = 2p(1-p)$. Ví dụ (2,4): $2\cdot\frac13\cdot\frac23 = \frac49 = 0.444$ ✓. Rất tiện khi thi!

---

## 4. Chia theo Gini (slides 154–158)

### 4.1 Gini của một phép chia (slide 154)
Dùng trong **CART, SLIQ, SPRINT**. Khi nút cha $p$ được chia thành $k$ nút con:
$$GINI_{split} = \sum_{i=1}^{k} \frac{n_i}{n}\, GINI(i)$$
- $n_i$: số bản ghi ở nút con $i$; $n$: số bản ghi ở nút cha $p$.
- Đây là **trung bình có trọng số** (weighted average) — nút con càng đông thì càng "có tiếng nói".

Chọn thuộc tính/phép chia có $GINI_{split}$ **nhỏ nhất**.

### 4.2 Thuộc tính nhị phân (slide 155)
Nút cha: C1 = 6, C2 = 6 → Gini = 0.5. Chia theo B?:
- N1 (Yes): C1 = 5, C2 = 2 (7 bản ghi): $GINI(N1) = 1 - (5/7)^2 - (2/7)^2 = 1 - \frac{25}{49} - \frac{4}{49} = \frac{20}{49} \approx 0.408$ (slide làm tròn 0.41).
- N2 (No): C1 = 1, C2 = 4 (5 bản ghi): $GINI(N2) = 1 - (1/5)^2 - (4/5)^2 = 1 - 0.04 - 0.64 = 0.32$.
- $GINI_{split} = \frac{7}{12}(0.408) + \frac{5}{12}(0.32) = 0.238 + 0.133 = \mathbf{0.371}$.

⚠️ **Slide ghi 0.369** — đây là **lỗi số học nhỏ trên slide**. Tính chính xác: $\frac{7}{12}\cdot\frac{20}{49} + \frac{5}{12}\cdot\frac{8}{25} = 0.2381 + 0.1333 = 0.3714$. (Kể cả dùng số làm tròn 0.41 cũng ra 0.3725, không phải 0.369.) Khi thi, hãy ghi **≈ 0.371**; kết luận không đổi: Gini giảm từ 0.5 xuống ~0.37 → phép chia có ích.

**Thông điệp của slide: "Effect of weighing partitions — Larger and purer partitions are sought for"** (tìm phân vùng **vừa lớn vừa sạch**). Một nút con rất sạch nhưng chỉ chứa 1 bản ghi đóng góp ít vào $GINI_{split}$; trọng số $n_i/n$ đảm bảo ta quan tâm tới nơi có nhiều dữ liệu.

### 4.3 Thuộc tính định danh (categorical) – slide 156
Cách làm: với mỗi giá trị khác nhau, đếm số bản ghi mỗi lớp → **ma trận đếm (count matrix)**, rồi dùng nó để quyết định. Dữ liệu: CarType, 10 bản ghi (C1 = 4, C2 = 6).

**(a) Chia nhiều nhánh (multi-way split):** Family (1,4), Sports (2,1), Luxury (1,1).
- Family: $1 - (1/5)^2 - (4/5)^2 = 0.32$
- Sports: $1 - (2/3)^2 - (1/3)^2 = 4/9 = 0.444$
- Luxury: $1 - 0.25 - 0.25 = 0.5$
- $GINI_{split} = \frac{5}{10}(0.32) + \frac{3}{10}(0.444) + \frac{2}{10}(0.5) = 0.16 + 0.133 + 0.1 = \mathbf{0.393}$ ✓

**(b) Chia hai nhánh (two-way split) – tìm cách gom giá trị tốt nhất:**
- {Sports, Luxury} (3,2) vs {Family} (1,4): $GINI = 1 - 0.36 - 0.16 = 0.48$ và $0.32$ → $0.5(0.48) + 0.5(0.32) = \mathbf{0.400}$ ✓
- {Sports} (2,1) vs {Family, Luxury} (2,5): $0.444$ và $1 - \frac{4}{49} - \frac{25}{49} = \frac{20}{49} = 0.408$ → $0.3(0.444) + 0.7(0.408) = 0.133 + 0.286 = \mathbf{0.419}$ ✓

→ Tốt nhất ở đây là **multi-way (0.393)**; trong các cách nhị phân thì {Sports,Luxury}|{Family} (0.400) tốt hơn.

> **Phân tích sâu:**
> - Multi-way thường cho Gini thấp hơn vì chia nhỏ hơn (giải thích tương tự nhược điểm của Information Gain ở slide 161). Nhưng nhiều nhánh → mỗi nhánh ít dữ liệu → dễ quá khớp.
> - Với $k$ giá trị, số cách chia nhị phân là $2^{k-1} - 1$ (bổ sung) — với k = 3 là 3 cách (slide chỉ vẽ 2 trong 3; cách còn lại {Luxury} vs {Family, Sports}: Luxury (1,1) Gini 0.5, {Family,Sports} (3,5) Gini $1-\frac{9}{64}-\frac{25}{64}=0.469$ → $0.2(0.5)+0.8(0.469) = 0.475$ — kém nhất, **(bổ sung)**).
> - CART chỉ dùng chia nhị phân; C4.5 dùng multi-way cho thuộc tính định danh (bổ sung).

### 4.4 Thuộc tính liên tục (continuous) – slides 157–158

**Slide 157:** Dữ liệu 10 bản ghi (Refund, Marital Status, Taxable Income, Cheat). Ý tưởng:
- Dùng **quyết định nhị phân dựa trên một giá trị** $v$: $A < v$ và $A \ge v$ (ví dụ cây "Taxable Income > 80K?").
- Có nhiều lựa chọn cho $v$: **số giá trị chia khả dĩ = số giá trị phân biệt**.
- Mỗi $v$ có một ma trận đếm (số bản ghi mỗi lớp ở hai phía).
- Cách ngây thơ: với mỗi $v$, quét toàn bộ CSDL để đếm và tính Gini → **kém hiệu quả** ($O(N^2)$, bổ sung) vì lặp lại công việc.

**Slide 158 – Cách hiệu quả:**
1. **Sắp xếp** thuộc tính theo giá trị.
2. **Quét tuyến tính** các giá trị, mỗi lần chỉ **cập nhật** ma trận đếm (dời 1 bản ghi từ phía ">" sang phía "≤") và tính Gini.
3. Chọn vị trí chia có Gini **nhỏ nhất**.

Bảng trên slide (Cheat theo Taxable Income đã sắp xếp):

| Thu nhập | 60 | 70 | 75 | 85 | 90 | 95 | 100 | 120 | 125 | 220 |
|---|---|---|---|---|---|---|---|---|---|---|
| Cheat | No | No | No | **Yes** | **Yes** | **Yes** | No | No | No | No |

Vị trí chia (split positions) là các điểm **giữa hai giá trị liền kề**: 55, 65, 72, 80, 87, 92, **97**, 110, 122, 172, 230. Tổng: Yes = 3, No = 7.

| $v$ | ≤v (Yes,No) | >v (Yes,No) | Gini |
|---|---|---|---|
| 55 | (0,0) | (3,7) | 0.420 |
| 65 | (0,1) | (3,6) | 0.400 |
| 72 | (0,2) | (3,5) | 0.375 |
| 80 | (0,3) | (3,4) | 0.343 |
| 87 | (1,3) | (2,4) | 0.417 |
| 92 | (2,3) | (1,4) | 0.400 |
| **97** | **(3,3)** | **(0,4)** | **0.300** ← tốt nhất |
| 110 | (3,4) | (0,3) | 0.343 |
| 122 | (3,5) | (0,2) | 0.375 |
| 172 | (3,6) | (0,1) | 0.400 |
| 230 | (3,7) | (0,0) | 0.420 |

**Kiểm tra tay $v = 97$:** bên trái (3 Yes, 3 No): Gini = 0.5; bên phải (0,4): Gini = 0. $GINI_{split} = \frac{6}{10}(0.5) + \frac{4}{10}(0) = 0.3$ ✓.
**Kiểm tra $v = 80$:** trái (0,3) Gini 0; phải (3,4): $1 - \frac{9}{49} - \frac{16}{49} = \frac{24}{49} = 0.490$; $0.7 \times 0.490 = 0.343$ ✓.

→ Phép chia tốt nhất: **Taxable Income ≤ 97K** (chú ý: slide 157 vẽ cây "> 80K?" chỉ là ví dụ minh họa; 80 là ứng viên tốt thứ hai, đồng hạng với 110).

> **Mẹo (bổ sung):** Gini tối ưu luôn nằm ở **ranh giới nơi nhãn lớp đổi** (ở đây 75|85 → 80 và 95|100 → 97). Nên chỉ cần thử các điểm đó → nhanh hơn nhiều. Trong bảng, các vị trí khác (87, 92…) đều kém hơn.
> **Độ phức tạp (bổ sung):** sắp xếp $O(N\log N)$ + quét $O(N)$, thay vì $O(N^2)$.

---

## 5. Entropy & Information Gain (slides 159–161)

### 5.1 Entropy (slide 159)
$$Entropy(t) = -\sum_j p(j\mid t)\,\log_2 p(j\mid t)$$
(quy ước $0\log 0 = 0$).
- Đo **độ đồng nhất (homogeneity)** của nút (đúng hơn là độ *hỗn loạn*).
- **Cực đại** $= \log_2 n_c$ khi các lớp phân bố đều (với 2 lớp: 1 bit) → ít thông tin nhất.
- **Cực tiểu** $= 0$ khi mọi bản ghi cùng một lớp.
- Các phép tính dựa trên entropy **tương tự** Gini (thay hàm Gini bằng hàm Entropy).

**Trực giác:** Entropy = số **bit trung bình** cần để báo cho người khác biết lớp của một bản ghi rút ngẫu nhiên từ nút. Nút thuần → không cần bit nào (ai cũng biết đáp án). Nút 50/50 → cần đúng 1 bit (như tung đồng xu).

### 5.2 Ví dụ (slide 160)
- (0,6): $-0\log 0 - 1\log 1 = 0$.
- (1,5): $-\frac16\log_2\frac16 - \frac56\log_2\frac56 = \frac16(2.585) + \frac56(0.263) = 0.431 + 0.219 = \mathbf{0.65}$.
  ⚠️ **Slide có lỗi đánh máy**: ghi "$-(5/6)\log_2(1/6)$" — đúng phải là $\log_2(5/6)$. (Nếu dùng $\log_2(1/6)$ ta được 2.585, sai hẳn; kết quả 0.65 của slide là của công thức đúng.)
- (2,4): $\frac13\log_2 3 + \frac23\log_2 1.5 = \frac13(1.585) + \frac23(0.585) = 0.528 + 0.390 = \mathbf{0.92}$ ✓.
- (3,3) (bổ sung): $= 1$ (max).

> **Mẹo tính tay (bổ sung):** $\log_2 x = \ln x / \ln 2 = \ln x / 0.693$. Nhớ vài giá trị: $\log_2 3 = 1.585$, $\log_2 5 = 2.322$, $\log_2 6 = 2.585$, $\log_2 7 = 2.807$. Nếu được, mang máy tính.

### 5.3 Information Gain (slide 161)
$$GAIN_{split} = Entropy(p) - \left(\sum_{i=1}^{k} \frac{n_i}{n}\, Entropy(i)\right)$$
- Nút cha $p$ chia thành $k$ phân vùng; $n_i$ = số bản ghi trong phân vùng $i$; $n$ = số bản ghi ở $p$.
- Đo **mức giảm entropy** nhờ phép chia → chọn phép chia **cực đại GAIN**.
- Dùng trong **ID3 và C4.5**.
- **Nhược điểm:** có xu hướng **ưu tiên phép chia tạo ra nhiều phân vùng, mỗi phân vùng nhỏ nhưng thuần** (chính là bẫy *Student ID* ở slide 148).

**Ví dụ tính tay (dùng dữ liệu slide 155, bổ sung):** cha (6,6) → Entropy = 1.
- N1 (5,2): $\frac57\log_2\frac75 + \frac27\log_2 3.5 = 0.714(0.485) + 0.286(1.807) = 0.347 + 0.516 = 0.863$
- N2 (1,4): $0.2\log_2 5 + 0.8\log_2 1.25 = 0.464 + 0.258 = 0.722$
- Entropy có trọng số: $\frac{7}{12}(0.863) + \frac{5}{12}(0.722) = 0.503 + 0.301 = 0.804$
- $GAIN = 1 - 0.804 = \mathbf{0.196}$.

**Minh họa nhược điểm với slide 148 (bổ sung):** cha (10,10), Entropy = 1.
- Own Car: hai con (6,4),(4,6), mỗi con entropy 0.971 → GAIN = 1 − 0.971 = **0.029**.
- Car Type: Family (1,3) entropy 0.811; Sports (8,0) entropy 0; Luxury (1,7) entropy 0.544 → trung bình $\frac{4}{20}(0.811) + \frac{8}{20}(0) + \frac{8}{20}(0.544) = 0.380$ → GAIN = **0.620**.
- Student ID: 20 con thuần → entropy con = 0 → GAIN = **1.0** (tối đa!) → Information Gain chọn Student ID — **sai về mặt ý nghĩa**.

### 5.4 Gain Ratio – cách khắc phục (bổ sung, không có trên slide nhưng là hệ quả trực tiếp của slide 161)
C4.5 dùng:
$$GainRatio = \frac{GAIN_{split}}{SplitINFO}, \qquad SplitINFO = -\sum_{i=1}^{k}\frac{n_i}{n}\log_2\frac{n_i}{n}$$
SplitINFO lớn khi chia thành nhiều phân vùng nhỏ → **phạt** phép chia nhiều nhánh.
- Student ID: SplitINFO $= \log_2 20 = 4.32$ → GainRatio $= 1/4.32 = 0.231$.
- Car Type: SplitINFO với tỉ lệ (0.2, 0.4, 0.4) $= 0.2\log_2 5 + 2\times0.4\log_2 2.5 = 0.464 + 1.058 = 1.522$ → GainRatio $= 0.620/1.522 = \mathbf{0.408}$ → Car Type thắng ✓.
- Own Car: SplitINFO = 1 → GainRatio = 0.029.

---

## 6. Lỗi phân lớp (Classification Error) – slides 162–163

### 6.1 Định nghĩa (slide 162)
$$Error(t) = 1 - \max_i P(i\mid t)$$
- Đo **lỗi phân lớp sai** mà nút gây ra nếu ta gán cho nút nhãn của **lớp đa số**.
- **Cực đại** $= 1 - \frac{1}{n_c}$ khi phân bố đều; **cực tiểu** $= 0$ khi thuần.

### 6.2 Ví dụ (slide 163)
- (0,6): $1 - \max(0, 1) = 0$
- (1,5): $1 - \max(1/6, 5/6) = 1/6 \approx 0.167$
- (2,4): $1 - \max(2/6, 4/6) = 1/3 \approx 0.333$

Đã kiểm tra: đúng.

**Áp dụng cho slide 155 (bổ sung):** N1 (5,2) error 2/7; N2 (1,4) error 1/5; $Error_{split} = \frac{7}{12}\cdot\frac27 + \frac{5}{12}\cdot\frac15 = \frac{2}{12} + \frac{1}{12} = 0.25$ (cha: 0.5). Mẹo: Error có trọng số = (tổng số bản ghi thiểu số ở các nút con)/n = 3/12.

---

## 7. So sánh các tiêu chí chia (slide 164)

Đồ thị cho bài toán **2 lớp**, trục hoành $p$ = tỉ lệ của một lớp:
- **Entropy** $= -p\log_2 p - (1-p)\log_2(1-p)$: đường cong đỏ, đỉnh **1.0** tại $p = 0.5$.
- **Gini** $= 2p(1-p)$: đường cong xanh (parabol), đỉnh **0.5** tại $p = 0.5$.
- **Misclassification error** $= \min(p, 1-p)$: đường gấp khúc đen (hình chữ Λ), đỉnh **0.5**.

Cả ba: = 0 tại $p = 0$ và $p = 1$, đối xứng quanh 0.5, cực đại tại 0.5.

> **Phân tích sâu (một phần bổ sung):**
> - Entropy và Gini **cong (strictly concave)**, còn Error **tuyến tính từng đoạn**. Hệ quả: Error có thể **không nhận ra cải thiện**. Ví dụ (từ sách Tan, bổ sung): cha (7,3), chia thành N1 (3,0) và N2 (4,3).
>   - Error: cha $= 0.3$; con $= \frac{3}{10}\cdot 0 + \frac{7}{10}\cdot\frac37 = 0.3$ → **không đổi**, Error nói "chia vô ích".
>   - Gini: cha $= 1 - 0.49 - 0.09 = 0.42$; con $= 0 + 0.7 \times \frac{24}{49} = 0.343$ → **giảm**, Gini nhận ra ta đã tách được một nút thuần (3,0).
>   - Entropy: 0.881 → 0.690, cũng giảm.
> - Vì vậy Gini/Entropy được dùng để **xây cây**, còn Error thường dùng để **đánh giá/cắt tỉa**.
> - Gini và Entropy thường cho cây rất giống nhau trong thực tế; Gini tính nhanh hơn (không có log).

---

## 8. Tiêu chí dừng (slides 165–166)

**Slide 165:** quay lại câu hỏi thứ 3 của tree induction: **khi nào dừng chia**.

**Slide 166 – Stopping criteria:**
1. Dừng mở rộng một nút khi **mọi bản ghi thuộc cùng một lớp** (nút đã thuần, không còn gì để tách).
2. Dừng khi **mọi bản ghi có giá trị thuộc tính giống nhau (similar attribute values)** (không còn thuộc tính nào phân biệt được chúng → gán nhãn đa số).
3. **Dừng sớm (early termination)** – bàn sau (chính là pre-pruning, slide 175).

**Ví dụ:** nút có 3 bản ghi {(Single, 90K, Yes), (Single, 90K, No), (Single, 90K, Yes)}: giá trị thuộc tính giống hệt nhau nhưng nhãn khác → không thể chia tiếp → lá với nhãn **Yes** (đa số). Đây cũng là dấu hiệu dữ liệu có **nhiễu** hoặc thiếu thuộc tính.

---

## 9. Ưu điểm của phân lớp bằng cây quyết định (slide 167)
- **Rẻ để xây dựng** (inexpensive to construct) – thuật toán tham lam, không cần tối ưu toàn cục.
- **Cực nhanh khi phân lớp bản ghi mới** – chỉ cần đi từ gốc xuống lá, tối đa = độ sâu cây phép so sánh.
- **Dễ diễn giải** với cây nhỏ – có thể đọc thành luật IF–THEN.
- **Độ chính xác tương đương** các kỹ thuật khác trên nhiều tập dữ liệu đơn giản.

**Nhược điểm (bổ sung, slide không nêu):** dễ quá khớp (→ phần tiếp theo); không ổn định (thay đổi dữ liệu nhỏ có thể đổi cây nhiều); ranh giới quyết định chỉ song song trục tọa độ (axis-parallel), khó biểu diễn quan hệ chéo như $x + y < 1$; tham lam → không đảm bảo cây tối ưu toàn cục.

---

## 10. Các vấn đề thực tế (slide 168)
1. **Underfitting và Overfitting** (dưới khớp và quá khớp) — slides 169–176.
2. **Missing values** (giá trị thiếu) — *chỉ được nêu tên, không có slide chi tiết*.
3. **Costs of classification** (chi phí phân lớp) — *chỉ được nêu tên, không có slide chi tiết*. (Xem phụ lục bổ sung.)

---

## 11. Underfitting & Overfitting (slide 169)

**Đồ thị:** trục hoành = **số nút của cây** (độ phức tạp mô hình, 0 → ~270); trục tung = **lỗi (%)**.
- **Training set** (đỏ, liền): giảm đều từ ~38% xuống ~9% khi cây lớn dần.
- **Test set** (xanh, nét đứt): giảm từ ~43% xuống cực tiểu ~32% quanh 100–180 nút, rồi **tăng trở lại** lên ~38%.
- Đường đứt dọc ở ~180 nút: bên phải là vùng **Overfitting**.

(Các giá trị số mình đọc từ đồ thị, chỉ mang tính ước lượng.)

**Định nghĩa:**
- **Underfitting (dưới khớp):** mô hình **quá đơn giản** → **cả lỗi huấn luyện và lỗi kiểm tra đều lớn** (phía trái đồ thị). Mô hình chưa học được cấu trúc thật của dữ liệu.
- **Overfitting (quá khớp):** cây **quá phức tạp** → lỗi huấn luyện tiếp tục giảm nhưng **lỗi kiểm tra tăng**. Mô hình "học thuộc lòng" cả nhiễu và đặc thù ngẫu nhiên của tập huấn luyện.

**Ví von:** Sinh viên học thuộc lòng đáp án đề cũ (training error = 0) nhưng gặp đề mới thì làm sai (test error cao) = overfitting. Sinh viên chỉ đọc mục lục (sai cả đề cũ lẫn đề mới) = underfitting.

> **Phân tích sâu (bổ sung):** đây là **đánh đổi bias–variance**. Cây nhỏ: bias cao (giả định quá đơn giản), variance thấp. Cây lớn: bias thấp, variance cao (thay đổi mạnh theo mẫu huấn luyện). Điểm tối ưu nằm ở cực tiểu của đường test. Mục tiêu của mọi kỹ thuật ở slide 172–176 là **tìm điểm đó mà không dùng tập test** (tập test chỉ để đánh giá cuối cùng).

---

## 12. Quá khớp do nhiễu (slide 170) – *Overfitting due to Noise*

Hình: hai lớp — chấm tròn đỏ (vùng dưới-trái) và dấu + xanh (vùng trên-phải). Có một **điểm nhiễu (noise point)**: một dấu + nằm tại khoảng (2.5, 0.8), lọt giữa vùng chấm đỏ. Ranh giới quyết định lẽ ra là một đường chéo đơn giản, nhưng cây cố gắng phân đúng điểm nhiễu nên tạo ra một **"túi" hẹp** (hai đoạn ranh giới xiên quanh điểm đó) → **ranh giới bị méo (distorted)**.

**Hậu quả:** các điểm test thật sự thuộc lớp "chấm đỏ" rơi vào túi này sẽ bị phân lớp sai thành "+".

**Ví dụ đời thực:** dữ liệu y tế có một bệnh nhân bị gõ sai nhãn "mắc bệnh" → cây tạo luật riêng "nếu tuổi 34 và cân nặng 61kg thì mắc bệnh" — luật vô nghĩa.

---

## 13. Quá khớp do thiếu mẫu (slide 171) – *Overfitting due to Insufficient Examples*

Hình: chấm đỏ (đặc và rỗng) và dấu × xanh; một đường thẳng đứng ở x ≈ 1.3 là ranh giới học được. Các chấm rỗng ở nửa dưới (x ≈ 1.5–3) được chỉ là **"Misclassified points"**. (Theo sách Tan, ký hiệu đặc là dữ liệu huấn luyện và ký hiệu rỗng là dữ liệu kiểm tra — slide không ghi chú thích rõ nên đây là cách hiểu hợp lý nhất, không chắc chắn 100%.)

Giải thích trên slide:
- **Thiếu điểm dữ liệu ở nửa dưới** của biểu đồ → khó dự đoán đúng nhãn của vùng đó.
- **Số bản ghi huấn luyện không đủ** trong vùng khiến cây phải dự đoán các mẫu test bằng **những bản ghi huấn luyện khác không liên quan** tới nhiệm vụ phân lớp (cây "ngoại suy" ranh giới từ vùng trên → sai ở vùng dưới).

> **Phân tích sâu:** Nhiễu (slide 170) = dữ liệu *sai*; thiếu mẫu (slide 171) = dữ liệu *không đủ đại diện*. Cả hai đều khiến cây đưa ra quyết định dựa trên **quá ít bằng chứng**. Đây là lý do pre-pruning có điều kiện "dừng nếu số mẫu < ngưỡng" (slide 175). Thêm nữa (bổ sung): ở các nút sâu, số bản ghi rất nhỏ nên một thuộc tính bất kỳ có thể *tình cờ* trông như phân tách tốt (*multiple comparison problem*).

---

## 14. Ghi chú về Overfitting (slide 172)
1. Overfitting tạo ra cây **phức tạp hơn mức cần thiết**.
2. **Lỗi huấn luyện không còn là ước lượng tốt** cho hiệu năng trên bản ghi chưa thấy (training error quá lạc quan).
3. **Cần cách mới để ước lượng lỗi** (generalization error – lỗi tổng quát hóa).

→ Hai hướng được slide trình bày: **đưa độ phức tạp mô hình vào đánh giá** (Occam, MDL) và **cắt tỉa** (pre/post-pruning). Các cách ước lượng lỗi khác (pessimistic error, validation set) là **bổ sung** — xem mục 17.

---

## 15. Dao cạo Occam (Occam's Razor) – slide 173
- Giữa **hai mô hình có lỗi tổng quát hóa tương đương**, nên **chọn mô hình đơn giản hơn**.
- Mô hình phức tạp có **khả năng cao hơn bị khớp một cách tình cờ (fitted accidentally) với lỗi trong dữ liệu**.
- Do đó, **nên tính cả độ phức tạp mô hình** khi đánh giá mô hình.

**Ví dụ:** Cây A (5 nút) và cây B (50 nút) cùng có lỗi ước lượng ~12% → chọn A: dễ hiểu hơn, ít khả năng "may mắn" khớp nhiễu, khái quát tốt hơn.

> **Lưu ý:** Occam không nói "mô hình đơn giản luôn tốt hơn" — chỉ nói **khi lỗi tương đương**. Một mô hình quá đơn giản sẽ underfit.

---

## 16. Minimum Description Length – MDL (slide 174)

**Kịch bản trên slide:** Người **A** có bảng dữ liệu đầy đủ $(X_1..X_n, y)$ (biết nhãn). Người **B** có cùng $X$ nhưng nhãn là "?". A muốn **truyền nhãn** cho B với ít bit nhất. A có thể:
- gửi thẳng tất cả nhãn, hoặc
- gửi **một mô hình** (cây quyết định, ví dụ cây trên slide: A? → Yes: 0; No: B? → B1: C? (C1: 0, C2: 1), B2: 1) **cộng với danh sách các bản ghi mà cây phân lớp sai** (để B sửa lại).

$$\text{Cost(Model, Data)} = \text{Cost(Data}\mid\text{Model)} + \text{Cost(Model)}$$
- **Cost** = số bit cần để mã hóa.
- Tìm mô hình có **tổng chi phí nhỏ nhất**.
- **Cost(Data|Model)** mã hóa **các lỗi phân lớp sai** (misclassification errors).
- **Cost(Model)** mã hóa **cây**: mã hóa nút (số nút con) + mã hóa điều kiện chia.

**Trực giác:** cây lớn → ít lỗi (Cost(Data|Model) nhỏ) nhưng tốn bit mô tả cây (Cost(Model) lớn). Cây nhỏ → ngược lại. MDL tự động cân bằng — đây là **Occam's Razor được định lượng hóa**.

**Ví dụ số (bổ sung — sơ đồ mã hóa theo kiểu bài tập sách Tan, slide không cho sơ đồ cụ thể):** giả sử $n = 16$ bản ghi, $m = 8$ thuộc tính, $k = 2$ lớp. Mã hóa: mỗi nút trong (internal node) $\log_2 m = 3$ bit (chỉ thuộc tính dùng để chia), mỗi lá $\log_2 k = 1$ bit (nhãn), mỗi lỗi $\log_2 n = 4$ bit (chỉ số bản ghi bị sai).
- Cây T1: 1 nút trong, 2 lá, 2 lỗi → $3 + 2 + 2\times4 = 13$ bit.
- Cây T2: 4 nút trong, 5 lá, 0 lỗi → $4\times3 + 5\times1 + 0 = 17$ bit.
→ MDL chọn **T1** dù T1 có lỗi huấn luyện cao hơn.

---

## 17. Xử lý Overfitting

### 17.1 Pre-Pruning – Cắt tỉa trước / Quy tắc dừng sớm (slide 175)
- **Dừng thuật toán trước khi cây phát triển đầy đủ.**
- Điều kiện dừng thông thường cho một nút:
  - dừng nếu mọi mẫu thuộc cùng lớp;
  - dừng nếu mọi giá trị thuộc tính giống nhau.
- **Điều kiện chặt hơn (more restrictive):**
  - dừng nếu **số mẫu < ngưỡng do người dùng đặt** (vd. `min_samples_split` trong scikit-learn, bổ sung);
  - dừng nếu **phân bố lớp độc lập với các thuộc tính có sẵn** (ví dụ kiểm định $\chi^2$);
  - dừng nếu việc mở rộng nút **không cải thiện độ đo tạp chất** (Gini hoặc information gain).

**Ví dụ kiểm định $\chi^2$ (bổ sung):** nút có 20 bản ghi (10 Yes, 10 No). Chia theo thuộc tính X: nhánh trái (6 Yes, 4 No), nhánh phải (4 Yes, 6 No). Nếu X độc lập với lớp, kỳ vọng mỗi ô = 5.
$$\chi^2 = \sum\frac{(O - E)^2}{E} = 4\times\frac{(6-5)^2}{5} = 0.8 < 3.84$$
(3.84 = ngưỡng với 1 bậc tự do, α = 0.05) → không bác bỏ độc lập → **dừng**, không chia.

**Ưu/nhược (một phần bổ sung):** ✔ nhanh, cây nhỏ ngay từ đầu. ✘ **khó chọn ngưỡng**: ngưỡng cao → underfit, ngưỡng thấp → vẫn overfit; ✘ **"tầm nhìn ngắn" (horizon effect)**: một phép chia hiện tại không cải thiện gì nhưng có thể mở đường cho phép chia rất tốt ở bước sau (ví dụ kinh điển: XOR — từng thuộc tính riêng lẻ có gain = 0, kết hợp hai thì tách hoàn hảo) → pre-pruning dừng quá sớm.

### 17.2 Post-pruning – Cắt tỉa sau (slide 176)
- **Cho cây phát triển toàn bộ.**
- **Tỉa các nút từ dưới lên (bottom-up).**
- Nếu **lỗi tổng quát hóa giảm** sau khi tỉa → **thay cây con (subtree) bằng một nút lá**.
- **Nhãn của nút lá** = **lớp đa số** của các mẫu trong cây con.
- **Có thể dùng MDL** để post-pruning (tỉa nếu tổng số bit giảm).

**Ví dụ post-pruning bằng ước lượng lỗi bi quan (pessimistic error) — (bổ sung, từ sách/slide gốc Tan, không có trong slide của lớp):**
Công thức: $e'(T) = \dfrac{e(T) + \Omega \cdot L}{N}$, với $e(T)$ = số lỗi huấn luyện, $L$ = số lá, $N$ = số bản ghi, $\Omega = 0.5$ = phạt mỗi lá.
- Nút trước khi chia: Yes = 20, No = 10 → lá đơn, nhãn Yes, 10 lỗi.
  Lỗi huấn luyện $= 10/30 = 0.333$; bi quan $= (10 + 0.5)/30 = 0.350$.
- Sau khi chia thành 4 lá: (Yes 8, No 4), (3, 4), (4, 1), (5, 1) → số lỗi $= 4 + 3 + 1 + 1 = 9$.
  Lỗi huấn luyện $= 9/30 = 0.300$; bi quan $= (9 + 4\times0.5)/30 = 11/30 = 0.367$.
- Lỗi huấn luyện nói "giữ cây con" (0.300 < 0.333), nhưng lỗi bi quan nói **"tỉa"** (0.367 > 0.350) → thay cây con bằng lá **Yes**.

**Các cách ước lượng lỗi tổng quát hóa khác (bổ sung):** *Reduced Error Pruning* — tách một **tập validation** từ dữ liệu huấn luyện, tỉa nếu lỗi trên validation không tăng.

**So sánh pre vs post (bổ sung):** post-pruning thường cho kết quả **tốt hơn** (đã "nhìn thấy" toàn cây, tránh horizon effect) nhưng **tốn tính toán hơn** (phải xây cây đầy đủ trước). C4.5 dùng post-pruning; CART dùng cost-complexity pruning (một dạng post-pruning).

---

## Phụ lục (bổ sung) — các chủ đề KHÔNG có trong slide 149–176 nhưng hay đi kèm

> Chỉ đọc nếu còn thời gian. Slide của lớp **không** trình bày các mục này; chúng thuộc phần cuối Chương 4 sách Tan (Model Evaluation) và slide "Costs of Classification" (168) chỉ nêu tên.

**Ma trận nhầm lẫn (confusion matrix)** cho 2 lớp (+ là lớp quan tâm):

| | Dự đoán + | Dự đoán − |
|---|---|---|
| **Thực tế +** | TP | FN |
| **Thực tế −** | FP | TN |

- Accuracy $= \frac{TP + TN}{TP + TN + FP + FN}$; Error rate = 1 − Accuracy.
- Precision $p = \frac{TP}{TP + FP}$; Recall $r = \frac{TP}{TP + FN}$; $F_1 = \frac{2rp}{r + p} = \frac{2TP}{2TP + FP + FN}$.

**Ví dụ:** TP = 40, FN = 10, FP = 20, TN = 930 (1000 bản ghi, 50 dương).
Accuracy $= 970/1000 = 0.97$; Precision $= 40/60 = 0.667$; Recall $= 40/50 = 0.8$; $F_1 = 80/110 = 0.727$.
**Bẫy lớp mất cân bằng:** mô hình "luôn đoán −" có Accuracy $= 950/1000 = 0.95$ (trông rất tốt!) nhưng Recall = 0.

**Ma trận chi phí (cost matrix):** ví dụ $C(\text{FN}) = 100$, $C(\text{FP}) = 1$, đúng thì 0. Mô hình trên: $10\times100 + 20\times1 = 1020$; mô hình "luôn −": $50\times100 = 5000$ → mô hình trên tốt hơn hẳn dù accuracy chỉ hơn 2%.

**Giá trị thiếu (missing values)** trong cây (theo sách): khi tính gain chỉ dùng bản ghi có giá trị; khi phân bản ghi thiếu xuống, chia theo **trọng số tỉ lệ** với số bản ghi mỗi nhánh (C4.5).

**Phương pháp đánh giá:** Holdout (vd. 2/3 train, 1/3 test); Random subsampling (lặp holdout); **k-fold cross-validation** (chia k phần, lần lượt mỗi phần làm test, lấy trung bình; k = n là leave-one-out); Bootstrap (lấy mẫu có hoàn lại, ~63.2% bản ghi xuất hiện trong mẫu huấn luyện).

---

## Dễ nhầm lẫn

1. **Gini tối thiểu vs Gain tối đa:** chọn phép chia có **$GINI_{split}$ nhỏ nhất** ⇔ **Gain lớn nhất**. Đừng chọn Gini lớn nhất!
2. **Quên trọng số $n_i/n$:** $GINI_{split}$ / entropy sau chia là **trung bình có trọng số**, không phải trung bình cộng thường. Ví dụ slide 155: trung bình thường $(0.408 + 0.32)/2 = 0.364$ ≠ 0.371.
3. **Giá trị cực đại khác nhau:** Gini max $= 1 - 1/n_c$ (2 lớp: 0.5); Entropy max $= \log_2 n_c$ (2 lớp: 1; 4 lớp: 2); Error max $= 1 - 1/n_c$. Entropy với nhiều lớp **có thể > 1**.
4. **log cơ số 2** trong entropy (slide 160 ghi $\log_2$). Dùng ln sẽ ra số khác (nats).
5. **Lỗi trên slide:** slide 155 ghi 0.369 (đúng là ≈ 0.371); slide 160 ghi $\log_2(1/6)$ ở số hạng thứ hai (đúng là $\log_2(5/6)$).
6. **Information Gain thiên vị thuộc tính nhiều giá trị** (Student ID) — dùng Gain Ratio để sửa (bổ sung).
7. **Misclassification error dùng để xây cây kém nhạy** (không thấy cải thiện ở ví dụ (7,3) → (3,0)+(4,3)).
8. **Underfitting ≠ "lỗi test cao":** underfitting = **cả hai lỗi đều cao**; overfitting = **train thấp nhưng test cao** (khoảng cách lớn).
9. **Pre-pruning vs Post-pruning:** *pre* = dừng **trong khi** xây (top-down, quy tắc dừng sớm); *post* = xây **hết** rồi tỉa **từ dưới lên**. Lá sau tỉa nhận nhãn **đa số**.
10. **Tiêu chí dừng "bình thường" vs "chặt hơn":** "cùng lớp" và "cùng giá trị thuộc tính" là điều kiện dừng tự nhiên (luôn có); ngưỡng số mẫu, $\chi^2$, không cải thiện Gini là điều kiện **pre-pruning** thực sự.
11. **MDL:** Cost(Data|Model) = chi phí mã hóa **lỗi**, Cost(Model) = chi phí mã hóa **cây** — đừng đảo ngược.
12. **Vị trí chia của thuộc tính liên tục** là **điểm giữa** hai giá trị đã sắp xếp (97 nằm giữa 95 và 100), không phải chính các giá trị.
13. **Occam:** chỉ ưu tiên mô hình đơn giản **khi lỗi tổng quát hóa tương đương**.

---

## Câu hỏi có thể ra thi (kèm lời giải)

**Q1. Tính Gini, Entropy, Error cho nút (C1 = 3, C2 = 7).**
Gini $= 1 - 0.09 - 0.49 = 0.42$ (hoặc $2(0.3)(0.7) = 0.42$).
Entropy $= 0.3\log_2(10/3) + 0.7\log_2(10/7) = 0.3(1.737) + 0.7(0.515) = 0.521 + 0.360 = 0.881$.
Error $= 1 - 0.7 = 0.3$.

**Q2. Nút cha (C1 = 6, C2 = 6) chia theo A thành N1 (4, 1) và N2 (2, 5). So sánh với phép chia B ở slide 155 (N1 (5,2), N2 (1,4)) theo Gini.**
A: $GINI(N1) = 1 - 0.64 - 0.04 = 0.32$; $GINI(N2) = 1 - \frac{4}{49} - \frac{25}{49} = 0.408$. $GINI_{split} = \frac{5}{12}(0.32) + \frac{7}{12}(0.408) = 0.133 + 0.238 = 0.371$.
B: 0.371 → **bằng nhau** (đối xứng: cùng các phân bố, chỉ đổi vai C1/C2). Gain mỗi phép = 0.5 − 0.371 = 0.129.

**Q3. Cho dãy thuộc tính liên tục đã sắp xếp với nhãn, tìm điểm chia tốt nhất theo Gini.**
Phương pháp: (1) sắp xếp; (2) lấy điểm giữa các giá trị liền kề; (3) quét, cập nhật đếm, tính $GINI_{split}$; (4) chọn nhỏ nhất. Với dữ liệu slide 158: **v = 97**, Gini = 0.300 (trái (3 Yes, 3 No), phải (0, 4)).

**Q4. Tại sao Information Gain thiên vị thuộc tính như Student ID? Cách khắc phục?**
Mỗi giá trị chỉ có 1 bản ghi → mọi nút con thuần → entropy con = 0 → Gain = Entropy(cha) = tối đa. Nhưng thuộc tính không tổng quát hóa được. Khắc phục: **Gain Ratio** = Gain / SplitINFO (bổ sung), hoặc chỉ cho phép chia nhị phân (CART), hoặc loại các thuộc tính kiểu định danh duy nhất.

**Q5. Vẽ và giải thích đường cong lỗi train/test theo số nút.** (slide 169)
Train giảm đơn điệu; test giảm rồi tăng. Trái = underfitting (cả hai cao), phải điểm cực tiểu test = overfitting. Giải thích nguyên nhân: nhiễu (slide 170), thiếu mẫu (slide 171).

**Q6. Phân biệt pre-pruning và post-pruning; ưu nhược điểm.**
Xem mục 17. Pre: nhanh nhưng khó chọn ngưỡng và có horizon effect. Post: tốt hơn thường lệ, tốn chi phí xây cây đầy đủ; lá thay thế mang nhãn đa số; có thể dùng MDL.

**Q7. Giải thích nguyên lý MDL và liên hệ Occam's Razor.**
Tổng bit = bit mã hóa cây + bit mã hóa lỗi; chọn mô hình tối thiểu tổng. Cây phức tạp trả giá Cost(Model); cây đơn giản trả giá Cost(Data|Model). Đây là phiên bản định lượng của Occam: chỉ thêm độ phức tạp khi nó "trả lại" đủ bit nhờ giảm lỗi. Ví dụ ở mục 16: T1 = 13 bit < T2 = 17 bit.

**Q8. Vì sao Misclassification Error ít được dùng làm tiêu chí xây cây?**
Tuyến tính từng đoạn → kém nhạy; ví dụ (7,3) → (3,0) + (4,3): Error không đổi (0.3 → 0.3) trong khi Gini giảm (0.42 → 0.343).

**Q9. Nêu các tiêu chí dừng trong xây cây.** (slide 166, 175)
Cùng lớp; cùng giá trị thuộc tính; dừng sớm: số mẫu < ngưỡng, độc lập lớp–thuộc tính ($\chi^2$), không cải thiện impurity.

**Q10. (bổ sung) Với pessimistic error $\Omega = 0.5$: nút (Yes 20, No 10) chia thành 4 lá với tổng 9 lỗi. Có tỉa không?**
Trước: $(10 + 0.5)/30 = 0.350$; sau: $(9 + 2)/30 = 0.367$ → sau tệ hơn → **tỉa**, thay bằng lá "Yes".

**Q11. Nhân tố nào trên slide 155 cho thấy "Larger and purer partitions are sought for"?**
N1 (7 bản ghi, Gini 0.408) có trọng số 7/12 lớn hơn N2 (5 bản ghi, Gini 0.32); phép chia lý tưởng có các nút con vừa đông vừa sạch để $GINI_{split}$ nhỏ.

---

## Tóm tắt cho tờ A4

**Ký hiệu:** $p_j = p(j\mid t)$ = tỉ lệ lớp $j$ tại nút $t$; $n_c$ = số lớp; $n_i$ = số bản ghi nút con $i$; $n$ = số bản ghi nút cha.

**Độ đo tạp chất (0 nếu thuần, max nếu đều):**
- $GINI(t) = 1 - \sum_j p_j^2$ — max $1 - 1/n_c$; 2 lớp: $2p(1-p)$, max 0.5.
- $Entropy(t) = -\sum_j p_j\log_2 p_j$ — max $\log_2 n_c$; 2 lớp max 1.
- $Error(t) = 1 - \max_j p_j$ — max $1 - 1/n_c$; 2 lớp: $\min(p, 1-p)$.
- Giá trị chuẩn (6 bản ghi): (1,5): G 0.278 / H 0.65 / E 0.167; (2,4): G 0.444 / H 0.92 / E 0.333; (3,3): 0.5 / 1 / 0.5.

**Chia:**
- $GINI_{split} = \sum_i \frac{n_i}{n}GINI(i)$ → **min** (CART, SLIQ, SPRINT).
- $GAIN = Entropy(p) - \sum_i\frac{n_i}{n}Entropy(i)$ → **max** (ID3, C4.5); thiên vị nhiều nhánh nhỏ thuần.
- (bổ sung) $GainRatio = GAIN / SplitINFO$, $SplitINFO = -\sum_i\frac{n_i}{n}\log_2\frac{n_i}{n}$.
- Tổng quát: Gain = M0 − M_children.
- Thuộc tính định danh: ma trận đếm; multi-way hoặc gom nhóm nhị phân ($2^{k-1} - 1$ cách).
- Thuộc tính liên tục: sắp xếp → điểm giữa → quét tuyến tính cập nhật đếm → chọn Gini nhỏ nhất (VD: Income ≤ 97 → 0.300).
- Error kém nhạy (tuyến tính) → dùng Gini/Entropy để xây cây.

**Dừng:** cùng lớp; cùng giá trị thuộc tính; dừng sớm.

**Ưu điểm cây:** rẻ, phân lớp rất nhanh, dễ hiểu (cây nhỏ), chính xác tương đương.

**Underfitting:** mô hình quá đơn giản, train & test đều cao. **Overfitting:** train ↓ test ↑, cây quá phức tạp. Nguyên nhân: **nhiễu**, **thiếu mẫu**. Lỗi train không ước lượng tốt lỗi tổng quát hóa.

**Occam:** lỗi tương đương → chọn mô hình đơn giản hơn.
**MDL:** Cost(Model, Data) = Cost(Data|Model) [lỗi] + Cost(Model) [cây] → min.

**Pre-pruning:** dừng sớm: #mẫu < ngưỡng; $\chi^2$ độc lập; không cải thiện Gini/IG. (Khó chọn ngưỡng, horizon effect.)
**Post-pruning:** cây đầy đủ → tỉa bottom-up → thay subtree bằng lá (lớp đa số) nếu lỗi tổng quát hóa giảm; có thể dùng MDL.
(bổ sung) Pessimistic: $e' = (e + 0.5L)/N$.

**Lỗi slide:** slide 155 → 0.371 (không phải 0.369); slide 160 → $\log_2(5/6)$.


---

