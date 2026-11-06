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
