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
