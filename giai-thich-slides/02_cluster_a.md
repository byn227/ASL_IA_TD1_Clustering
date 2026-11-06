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
