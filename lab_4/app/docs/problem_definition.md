e# Problem Definition

# Image Retrieval System using Wavelet Hashing (wHash)

## 1. Overview

Trong nhiều ứng dụng thực tế, việc tìm kiếm hình ảnh tương tự (Image Retrieval) là một nhu cầu quan trọng, chẳng hạn như tìm ảnh trùng lặp, phát hiện ảnh đã chỉnh sửa nhẹ hoặc xác định xem một hình ảnh đã tồn tại trong cơ sở dữ liệu hay chưa.

Các phương pháp so sánh trực tiếp từng pixel thường không hoạt động tốt khi ảnh bị thay đổi kích thước, nén JPEG, thêm nhiễu hoặc điều chỉnh độ sáng. Vì vậy, hệ thống này sử dụng **Wavelet Hashing (wHash)** – một kỹ thuật thuộc nhóm **Perceptual Hashing** – nhằm biểu diễn đặc trưng thị giác của ảnh dưới dạng chuỗi bit ngắn gọn.

Thay vì lưu toàn bộ đặc trưng của ảnh, mỗi ảnh được chuyển thành một mã hash. Khi người dùng tải lên một ảnh truy vấn, hệ thống sẽ tạo hash cho ảnh đó, so sánh với hash của các ảnh trong cơ sở dữ liệu bằng khoảng cách Hamming và trả về các ảnh giống nhất.

---

# 2. Problem Statement

Xây dựng một ứng dụng web cho phép người dùng:

- Tải lên một hình ảnh từ máy tính.
- Hệ thống tự động tiền xử lý ảnh.
- Sinh mã Wavelet Hash cho ảnh đầu vào.
- Sinh hoặc tải trước Wavelet Hash của các ảnh trong thư mục dữ liệu.
- Tính khoảng cách Hamming giữa ảnh truy vấn và toàn bộ ảnh trong cơ sở dữ liệu.
- Sắp xếp kết quả theo độ tương đồng.
- Hiển thị ảnh có mức độ giống cao nhất cùng các ảnh tương tự khác.

Mục tiêu là xây dựng một hệ thống tìm kiếm nhanh, đơn giản và có khả năng chống chịu với các biến đổi nhỏ của ảnh.

---

# 3. Objectives

## Functional Objectives

- Upload ảnh từ giao diện web.
- Tiền xử lý ảnh (resize, chuyển grayscale nếu cần).
- Sinh Wavelet Hash cho ảnh đầu vào.
- Sinh Wavelet Hash cho tập ảnh trong thư mục dataset.
- So sánh hash bằng Hamming Distance.
- Trả về Top-K ảnh có khoảng cách nhỏ nhất.
- Hiển thị điểm tương đồng hoặc khoảng cách Hamming.
- Cho phép mở rộng để thêm ảnh mới vào cơ sở dữ liệu.

## Performance Objectives

- Thời gian truy vấn thấp (< 1 giây với vài nghìn ảnh).
- Hash có kích thước nhỏ để giảm chi phí lưu trữ.
- Có khả năng nhận diện ảnh đã:
  - Resize
  - Thêm Gaussian Noise nhẹ
  - JPEG Compression
  - Blur nhẹ
  - Thay đổi độ sáng vừa phải

---

# 4. Scope

## In Scope

- Ứng dụng web sử dụng Flask.
- So sánh ảnh bằng Wavelet Hash.
- Dataset lưu trên thư mục cục bộ.
- Khoảng cách sử dụng Hamming Distance.
- Giao diện web upload và hiển thị kết quả.
- Hỗ trợ định dạng PNG, JPG, JPEG.

## Out of Scope

- Deep Learning Image Retrieval.
- Content-Based Image Retrieval sử dụng CNN.
- Cơ sở dữ liệu phân tán.
- Xử lý video.
- Nhận dạng đối tượng (Object Detection).
- Semantic Search.

---

# 5. Input

Người dùng tải lên:

- PNG
- JPG
- JPEG

Ví dụ:

```
query_image.jpg
```

---

# 6. Output

Hệ thống trả về:

- Ảnh giống nhất.
- Danh sách Top-K ảnh tương tự.
- Giá trị Hamming Distance.
- Thứ hạng (Rank).
- Có thể hiển thị thêm Similarity Score (%).

Ví dụ:

| Rank | Image       | Hamming Distance |
| ---- | ----------- | ---------------- |
| 1    | cat_015.jpg | 3                |
| 2    | cat_102.jpg | 5                |
| 3    | cat_201.jpg | 7                |

---

# 7. System Workflow

```
                 +----------------------+
                 | User Upload Image    |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Image Preprocessing  |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Generate wHash       |
                 +----------+-----------+
                            |
                            |
                            | compare
                            |
                            v
     +-----------------------------------------------+
     | Hash Database (Generated from Dataset Folder)  |
     +-----------------------------------------------+
                            |
                            v
                Compute Hamming Distance
                            |
                            v
                 Rank by Increasing Distance
                            |
                            v
                  Return Top-K Similar Images
```

---

# 8. Technologies

## Backend

- Python 3.x
- Flask
- NumPy
- OpenCV
- Pillow
- PyWavelets

## Frontend

- HTML5
- CSS3
- JavaScript (ES6)
- Bootstrap 5 (Responsive UI)

## Visualization

- Card Layout
- Progress Bar cho Similarity
- Loading Spinner khi tìm kiếm

---

# 9. Suggested Project Structure

```
project/
│
├── app.py
├── requirements.txt
│
├── static/
│   ├── css/
│   │      style.css
│   ├── js/
│   │      app.js
│   ├── uploads/
│   └── dataset/
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── hashing/
│   ├── wavelet_hash.py
│   ├── preprocessing.py
│   └── hamming.py
│
├── cache/
│   └── hashes.pkl
│
└── README.md
```

---

# 10. Main Algorithm

```
Dataset Images
      |
      v
Preprocessing
      |
      v
Wavelet Transform
      |
      v
Coefficient Quantization
      |
      v
Generate Binary Hash
      |
      v
Store Hash
```

Khi truy vấn:

```
Query Image
      |
      v
Preprocessing
      |
      v
Wavelet Hash
      |
      v
Compare with Stored Hashes
      |
      v
Hamming Distance
      |
      v
Sort Ascending
      |
      v
Return Top-K Results
```

---

# 11. Hamming Distance Formula

Cho hai chuỗi hash nhị phân:

```
H1 = 10100110
H2 = 10110100
```

Khoảng cách Hamming:

```
Distance(H1,H2)
= số vị trí bit khác nhau
```

Giá trị càng nhỏ thì hai ảnh càng giống nhau.

---

# 12. Evaluation Metrics

Để đánh giá hệ thống có thể sử dụng:

- Hamming Distance
- Precision@K
- Recall@K
- Top-1 Accuracy
- Top-5 Accuracy
- ROC Curve
- AUC Score

---

# 13. Future Improvements

- Lưu hash trong SQLite hoặc PostgreSQL thay vì file.
- Tiền tính (precompute) hash để tăng tốc truy vấn.
- Kết hợp nhiều loại perceptual hash (aHash, dHash, pHash, wHash).
- Sử dụng Approximate Nearest Neighbor (ANN) cho tập dữ liệu lớn.
- Bổ sung API REST để tích hợp với các hệ thống khác.
- Triển khai Docker và Nginx để phục vụ môi trường production.

---

# 14. Expected Outcome

Sau khi hoàn thành, hệ thống có khả năng:

- Tìm kiếm ảnh tương tự dựa trên nội dung thị giác thay vì tên tệp.
- Chống chịu tương đối tốt trước các biến đổi nhỏ như resize, nén JPEG, nhiễu nhẹ hoặc thay đổi độ sáng.
- Trả về kết quả được xếp hạng theo khoảng cách Hamming, giúp người dùng nhanh chóng xác định ảnh phù hợp nhất trong tập dữ liệu.
