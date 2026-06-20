# 2. Implementation

---

## 2.1 Tổng quan quy trình triển khai

Để xây dựng hệ thống so sánh mức độ tương đồng của hình ảnh bằng **Wavelet Hashing**, Notebook sẽ được triển khai theo các bước tuần tự từ chuẩn bị dữ liệu đến đánh giá kết quả.

```text
                 +----------------------+
                 |   Input Images       |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |   Image Preprocessing |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |  Wavelet Transform    |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Generate Wavelet Hash |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Hamming Distance      |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Similarity Decision   |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Performance Evaluation|
                 +----------------------+
```

---

## 2.2 Bước 1 - Import thư viện

Đầu tiên, Notebook sẽ import các thư viện cần thiết phục vụ cho việc xử lý ảnh, tính toán số học, trực quan hóa dữ liệu và đánh giá kết quả.

Các thư viện dự kiến sử dụng:

- `numpy`: xử lý mảng và tính toán số học.
- `matplotlib.pyplot`: hiển thị hình ảnh và biểu đồ.
- `Pillow (PIL)` hoặc `OpenCV`: đọc và xử lý ảnh.
- `pywt` (PyWavelets): thực hiện biến đổi Wavelet.
- `sklearn.metrics`: tính Accuracy, Precision, Recall, ROC Curve và Confusion Matrix.

---

## 2.3 Bước 2 - Chuẩn bị dữ liệu

Tập dữ liệu sẽ bao gồm nhiều hình ảnh dùng để kiểm tra mức độ tương đồng.

Trong bước này sẽ:

- Đọc toàn bộ ảnh từ thư mục dữ liệu.
- Hiển thị một số ảnh mẫu để quan sát trực quan.
- Xây dựng các cặp ảnh cần so sánh.
- Gán nhãn (`1`: tương tự, `0`: không tương tự) phục vụ cho quá trình đánh giá.

---

## 2.4 Bước 3 - Tiền xử lý ảnh

Để đảm bảo tính nhất quán khi trích xuất đặc trưng, mỗi ảnh sẽ được tiền xử lý trước khi áp dụng Wavelet Transform.

Các thao tác có thể bao gồm:

- Chuyển ảnh sang ảnh xám (Grayscale).
- Chuẩn hóa kích thước về cùng một độ phân giải.
- Chuẩn hóa kiểu dữ liệu và giá trị pixel.
- Hiển thị kết quả trước và sau tiền xử lý bằng `matplotlib`.

---

## 2.5 Bước 4 - Áp dụng Wavelet Transform

Sau khi tiền xử lý, ảnh sẽ được biến đổi sang miền Wavelet bằng phép biến đổi Wavelet rời rạc (Discrete Wavelet Transform - DWT).

Mục tiêu của bước này là:

- Tách thông tin tần số thấp và tần số cao.
- Thu được các hệ số Wavelet đại diện cho đặc trưng của ảnh.
- Trực quan hóa các thành phần Wavelet để quan sát sự khác biệt.

---

## 2.6 Bước 5 - Sinh Wavelet Hash

Dựa trên các hệ số Wavelet thu được, hệ thống sẽ tạo ra một mã băm nhị phân (Wavelet Hash) đại diện cho mỗi hình ảnh.

Quá trình này thường bao gồm:

- Lượng tử hóa các hệ số Wavelet.
- Chuyển đổi sang chuỗi bit có độ dài cố định.
- Lưu trữ mã băm để phục vụ việc so sánh.

Kết quả của bước này là mỗi ảnh được biểu diễn bằng một vector nhị phân thay vì toàn bộ ma trận pixel.

---

## 2.7 Bước 6 - Tính khoảng cách Hamming

Để đo mức độ tương đồng giữa hai ảnh, Notebook sẽ tính khoảng cách Hamming giữa hai mã băm.

Khoảng cách Hamming biểu diễn số lượng bit khác nhau giữa hai chuỗi nhị phân:

- Giá trị nhỏ → Hai ảnh có xu hướng tương tự.
- Giá trị lớn → Hai ảnh có xu hướng khác nhau.

Khoảng cách này sẽ được tính cho tất cả các cặp ảnh trong tập dữ liệu.

---

## 2.8 Bước 7 - Đưa ra quyết định tương đồng

Sau khi tính khoảng cách Hamming, hệ thống sẽ so sánh giá trị này với một ngưỡng (`threshold`) được xác định trước.

- Nếu khoảng cách nhỏ hơn hoặc bằng ngưỡng, cặp ảnh được xem là **tương tự**.
- Nếu khoảng cách lớn hơn ngưỡng, cặp ảnh được xem là **không tương tự**.

Kết quả dự đoán sẽ được lưu lại để so sánh với nhãn thực tế.

---

## 2.9 Bước 8 - Đánh giá hiệu quả

Cuối cùng, hiệu quả của phương pháp sẽ được đánh giá thông qua các chỉ số:

- **Accuracy**: Tỷ lệ dự đoán đúng trên toàn bộ dữ liệu.
- **Precision**: Tỷ lệ dự đoán tương tự chính xác.
- **Recall (Sensitivity)**: Khả năng phát hiện đúng các cặp ảnh tương tự.
- **Specificity**: Khả năng nhận diện đúng các cặp ảnh không tương tự.
- **ROC Curve và AUC**: Đánh giá khả năng phân biệt giữa hai lớp.
- **Confusion Matrix**: Trực quan hóa kết quả phân loại.

Các kết quả sẽ được biểu diễn dưới dạng bảng và biểu đồ nhằm hỗ trợ việc phân tích và so sánh.

---

## 2.10 Kết quả mong muốn

Sau khi hoàn thành toàn bộ quy trình triển khai, hệ thống có khả năng:

- Sinh mã băm Wavelet cho mỗi hình ảnh.
- Đo lường mức độ tương đồng giữa các cặp ảnh thông qua khoảng cách Hamming.
- Phân loại các cặp ảnh thành tương tự hoặc không tương tự.
- Đánh giá và trực quan hóa hiệu quả của phương pháp bằng nhiều chỉ số khác nhau.
