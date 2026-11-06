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
