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
