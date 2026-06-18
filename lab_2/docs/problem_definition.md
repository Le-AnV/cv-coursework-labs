# Problem Definition

## Đề tài

Xây dựng chương trình xử lý ảnh cơ bản bằng Python và OpenCV để thực hiện các phép toán điểm ảnh, các bộ lọc tuyến tính và một số kỹ thuật xử lý ảnh nâng cao.

---

## Mô tả bài toán

Ảnh số thường cần được xử lý trước khi sử dụng trong các bài toán Computer Vision hoặc phân tích hình ảnh. Các kỹ thuật xử lý ảnh cơ bản giúp cải thiện chất lượng ảnh, làm nổi bật thông tin quan trọng và hỗ trợ việc nhận dạng đặc trưng trong ảnh.

Bài toán yêu cầu xây dựng chương trình đọc một ảnh màu từ máy tính và áp dụng nhiều kỹ thuật xử lý ảnh khác nhau để quan sát sự thay đổi của ảnh sau mỗi phép biến đổi.

---

## Mục tiêu

Sau khi hoàn thành bài tập, sinh viên có thể:

- Hiểu cách biểu diễn ảnh số.
- Hiểu nguyên lý hoạt động của các phép toán điểm ảnh.
- Hiểu cơ chế của các bộ lọc tuyến tính.
- Hiểu cách phát hiện cạnh trong ảnh.
- So sánh hiệu quả của các phương pháp xử lý ảnh khác nhau.
- Làm quen với thư viện OpenCV trong Python.

---

# Functional Requirements

## I. Toán tử điểm ảnh

### 1. Thay đổi độ sáng

- Tăng độ sáng ảnh.
- Giảm độ sáng ảnh.
- Sử dụng giá trị cố định.
- Khi giá trị pixel vượt ngoài khoảng [0,255], áp dụng clipping về khoảng hợp lệ.

### 2. Thay đổi độ tương phản

- Tăng độ tương phản.
- Giảm độ tương phản.
- Thực hiện bằng cách nhân mỗi điểm ảnh với một hằng số cố định.

### 3. Biến đổi âm bản

- Tạo ảnh âm bản từ ảnh gốc bằng cách đảo ngược giá trị điểm ảnh.

### 4. Cắt ngưỡng

- Chuyển ảnh thành ảnh nhị phân dựa trên giá trị ngưỡng cố định.
- Thực hiện trên ảnh grayscale được chuyển đổi từ ảnh màu.

---

## II. Lọc tuyến tính

### 1. Lọc trung bình (Mean Filter)

- Làm mờ ảnh bằng cách lấy giá trị trung bình trong vùng lân cận.
- Sử dụng kernel mặc định 3x3.

### 2. Lọc Gaussian

- Làm mờ ảnh bằng Gaussian Filter.
- Sử dụng kernel mặc định 3x3.

### 3. Làm sắc nét (Sharpen)

- Tăng cường chi tiết và cạnh của ảnh.
- Sử dụng kernel sharpen tiêu chuẩn.

---

## III. Bài tập nâng cao

### 1. Phát hiện cạnh

- Sobel Filter.
- Prewitt Filter.
- Hiển thị kết quả để quan sát và so sánh cạnh được phát hiện.

### 2. Kernel tự thiết kế

- Tạo và áp dụng ít nhất một kernel tùy chỉnh.
- Mục tiêu là tạo hiệu ứng khác với các bộ lọc có sẵn.

### 3. So sánh bộ lọc

- So sánh trực quan kết quả của:
  - Mean Filter
  - Gaussian Filter
  - Median Filter
  - Bilateral Filter

- Nhận xét:
  - Mức độ làm mờ.
  - Khả năng giữ chi tiết.
  - Khả năng giữ cạnh.

### 4. Lọc phi tuyến

- Median Filter.
- Bilateral Filter.

---

# Constraints

## Ngôn ngữ lập trình

- Python 3.x

## Thư viện sử dụng

- OpenCV
- NumPy

## Định dạng ảnh

- JPG
- JPEG
- PNG

## Giới hạn

- Chỉ xử lý ảnh tĩnh.
- Không sử dụng Deep Learning.
- Không xử lý video.
- Không sử dụng GPU.

---

# Input

- Ảnh màu.
- Đọc từ đường dẫn (path) trên máy tính.
- Giai đoạn đầu có thể sử dụng ảnh mẫu để kiểm thử.

---

# Output

- Ảnh kết quả sau mỗi phép xử lý.
- Hình ảnh so sánh giữa ảnh gốc và ảnh đã xử lý.
- Các nhận xét trực quan về sự khác biệt giữa các phương pháp lọc.

---

# Implementation Assumptions

- Mỗi chức năng xử lý ảnh được triển khai thành một hàm riêng.
- Sử dụng giá trị tham số cố định trong giai đoạn đầu.
- Ưu tiên triển khai đơn giản để phục vụ mục tiêu học tập.
- Có thể mở rộng thành chương trình tương tác ở giai đoạn sau.

---

# Success Criteria

Bài tập được xem là hoàn thành khi:

- Đọc được ảnh đầu vào từ path.
- Thực hiện đầy đủ các yêu cầu trong đề bài.
- Hiển thị đúng kết quả của từng phép xử lý.
- So sánh được sự khác biệt giữa các phương pháp lọc.
- Giải thích được tác dụng của từng kỹ thuật xử lý ảnh.
- Mã nguồn rõ ràng, dễ hiểu và dễ mở rộng.
