# <center> **COMPUTER VISION** </center>

---

# <center> **Lab 4: So sánh sự tương đồng của hình ảnh sử dụng Wavelet Hashing với Python** </center>

---

## Table of Contents

1. Problem Definition
2. Import Libraries
3. Chuẩn bị và khám phá dữ liệu
4. Tiền xử lý ảnh
5. Tìm hiểu về Wavelet Transform
6. Xây dựng thuật toán Wavelet Hash
7. So sánh mức độ tương đồng bằng khoảng cách Hamming
8. Đánh giá kết quả (Accuracy, Precision, Recall, ROC Curve)
9. Thử nghiệm và trực quan hóa
10. Kết luận

---

# 1. Problem Definition

## 1.1 Giới thiệu

Trong các hệ thống xử lý ảnh hiện đại như tìm kiếm ảnh tương tự, phát hiện ảnh trùng lặp hay kiểm tra vi phạm bản quyền, việc xác định hai hình ảnh có giống nhau hay không là một bài toán quan trọng. Tuy nhiên, việc so sánh trực tiếp giá trị của từng pixel thường không hiệu quả khi ảnh bị thay đổi về kích thước, độ sáng hoặc có một số biến đổi nhỏ.

Một phương pháp được sử dụng để giải quyết vấn đề này là **Wavelet Hashing (Wavelet Hash)**. Thay vì lưu toàn bộ thông tin của ảnh, phương pháp này biểu diễn ảnh bằng một chuỗi bit ngắn gọn (hash code) được tạo ra từ các hệ số Wavelet. Những ảnh có nội dung tương tự thường tạo ra các mã băm gần giống nhau, trong khi các ảnh khác biệt sẽ có mã băm khác biệt đáng kể.

---

## 1.2 Mục tiêu của bài thực hành

Trong bài Lab này, chúng ta sẽ xây dựng một quy trình hoàn chỉnh để so sánh mức độ tương đồng giữa các hình ảnh bằng Wavelet Hashing sử dụng Python.

Cụ thể, Notebook sẽ thực hiện các nhiệm vụ sau:

- Chuẩn bị tập dữ liệu gồm nhiều hình ảnh để so sánh.
- Thực hiện tiền xử lý ảnh trước khi trích xuất đặc trưng.
- Áp dụng phép biến đổi Wavelet để biểu diễn thông tin của ảnh.
- Sinh mã băm (Wavelet Hash) cho từng hình ảnh.
- Tính khoảng cách Hamming giữa các mã băm để đo mức độ tương đồng.
- Đánh giá hiệu quả của phương pháp thông qua các chỉ số như Accuracy, Precision, Recall và ROC Curve.
- Trực quan hóa kết quả bằng hình ảnh và biểu đồ để dễ phân tích.

---

## 1.3 Quy trình thực hiện

Toàn bộ Notebook được triển khai theo quy trình sau:

```
Ảnh đầu vào
      │
      ▼
Tiền xử lý ảnh
      │
      ▼
Biến đổi Wavelet (DWT)
      │
      ▼
Sinh Wavelet Hash
      │
      ▼
Tính khoảng cách Hamming
      │
      ▼
Xác định mức độ tương đồng
      │
      ▼
Đánh giá bằng các chỉ số và trực quan hóa kết quả
```

---

## 1.4 Kết quả mong đợi

Sau khi hoàn thành bài thực hành, người học có thể:

- Hiểu nguyên lý hoạt động của Wavelet Transform trong xử lý ảnh.
- Biết cách xây dựng thuật toán Wavelet Hash bằng Python.
- So sánh mức độ tương đồng giữa các hình ảnh thông qua khoảng cách Hamming.
- Đánh giá chất lượng của phương pháp bằng các thước đo phổ biến trong bài toán phân loại.
- Phân tích kết quả thông qua hình ảnh minh họa và biểu đồ trực quan trong Jupyter Notebook.
