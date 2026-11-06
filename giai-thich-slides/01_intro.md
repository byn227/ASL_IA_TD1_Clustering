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
