# Implementation Plan - Image Processing with OpenCV

## Project Overview

Xây dựng chương trình xử lý ảnh cơ bản bằng Python và OpenCV để thực hiện các phép toán điểm ảnh, bộ lọc tuyến tính và kỹ thuật xử lý ảnh nâng cao.

---

## Technology Stack

- **Ngôn ngữ**: Python 3.x
- **Thư viện chính**: OpenCV, NumPy
- **Định dạng ảnh hỗ trợ**: JPG, JPEG, PNG
- **Phạm vi**: Chỉ xử lý ảnh tĩnh (không video, không GPU, không Deep Learning)

---

## Phase 1: Project Setup & Image I/O

### Task 1.1: Cấu hình môi trường

- [ ] Cài đặt OpenCV
- [ ] Cài đặt NumPy
- [ ] Cấu hình Jupyter Notebook

### Task 1.2: Image Loading & Display

- [ ] Hàm đọc ảnh từ đường dẫn
- [ ] Hàm hiển thị ảnh gốc
- [ ] Hàm hiển thị so sánh (original vs processed)
- [ ] Kiểm thử với ảnh mẫu

---

## Phase 2: Point Operators (Toán tử điểm ảnh)

### Task 2.1: Thay đổi độ sáng

- [ ] Tăng độ sáng (brightness increase)
- [ ] Giảm độ sáng (brightness decrease)
- [ ] Áp dụng clipping để giữ giá trị pixel trong [0, 255]
- [ ] Kiểm thử và hiển thị kết quả

### Task 2.2: Thay đổi độ tương phản

- [ ] Tăng độ tương phản (contrast increase)
- [ ] Giảm độ tương phản (contrast decrease)
- [ ] Sử dụng phép nhân với hằng số cố định
- [ ] Kiểm thử và so sánh kết quả

### Task 2.3: Biến đổi âm bản

- [ ] Tạo ảnh âm bản (image negation)
- [ ] Công thức: `new_pixel = 255 - old_pixel`
- [ ] Hiển thị kết quả

### Task 2.4: Cắt ngưỡng (Thresholding)

- [ ] Chuyển ảnh sang grayscale
- [ ] Áp dụng thresholding tạo ảnh nhị phân
- [ ] Sử dụng ngưỡng cố định
- [ ] So sánh với ảnh gốc

---

## Phase 3: Linear Filters (Lọc tuyến tính)

### Task 3.1: Mean Filter

- [ ] Cài đặt kernel 3x3
- [ ] Áp dụng lọc trung bình (blur effect)
- [ ] Hiển thị kết quả trên ảnh màu

### Task 3.2: Gaussian Filter

- [ ] Cài đặt kernel Gaussian 3x3
- [ ] Áp dụng Gaussian blur
- [ ] So sánh với Mean Filter
- [ ] Nhận xét về hiệu quả làm mờ

### Task 3.3: Sharpen Filter

- [ ] Cài đặt kernel sharpen tiêu chuẩn
- [ ] Tăng cường chi tiết và cạnh
- [ ] Kiểm thử hiệu quả

---

## Phase 4: Advanced Techniques (Bài tập nâng cao)

### Task 4.1: Edge Detection - Sobel Filter

- [ ] Cài đặt Sobel operator (horizontal & vertical)
- [ ] Tính gradient magnitude
- [ ] Hiển thị edge map

### Task 4.2: Edge Detection - Prewitt Filter

- [ ] Cài đặt Prewitt operator
- [ ] So sánh kết quả với Sobel
- [ ] Nhận xét về sự khác biệt

### Task 4.3: Custom Kernel Design

- [ ] Thiết kế ít nhất một kernel tùy chỉnh
- [ ] Áp dụng kernel tùy chỉnh
- [ ] Nhận xét về hiệu ứng tạo ra
- [ ] So sánh với bộ lọc có sẵn

### Task 4.4: Non-linear Filters Comparison

- [ ] Cài đặt Median Filter
- [ ] Cài đặt Bilateral Filter
- [ ] So sánh 4 bộ lọc:
  - Mean Filter
  - Gaussian Filter
  - Median Filter
  - Bilateral Filter

### Task 4.5: Filter Comparison Analysis

- [ ] Tạo bảng so sánh (comparison table)
- [ ] Đánh giá các tiêu chí:
  - Mức độ làm mờ (blur level)
  - Khả năng giữ chi tiết (detail preservation)
  - Khả năng giữ cạnh (edge preservation)
- [ ] Trực quan hóa kết quả

---

## Phase 5: Code Organization & Documentation

### Task 5.1: Modular Code Structure

- [ ] Tạo module xử lý ảnh với các hàm riêng biệt
- [ ] Mỗi chức năng = một hàm
- [ ] Tham số hóa các giá trị (để dễ mở rộng)

### Task 5.2: Documentation

- [ ] Thêm docstring cho từng hàm
- [ ] Giải thích nguyên lý hoạt động
- [ ] Thêm ví dụ sử dụng

### Task 5.3: Testing & Validation

- [ ] Kiểm thử với nhiều ảnh khác nhau
- [ ] Xác minh giá trị pixel không vượt quá [0, 255]
- [ ] Đảm bảo kết quả chính xác

---

## Phase 6: Final Deliverables

### Task 6.1: Presentation & Visualization

- [ ] Tạo notebook trực quan với hình ảnh
- [ ] So sánh ảnh gốc vs xử lý
- [ ] Giải thích từng kỹ thuật

### Task 6.2: Summary Report

- [ ] Tóm tắt kết quả thực hiện
- [ ] Nhận xét về hiệu quả các phương pháp
- [ ] Kết luận

---

## Success Criteria Checklist

- [ ] Đọc được ảnh đầu vào từ path
- [ ] Thực hiện đầy đủ các yêu cầu phần I (Point operators)
- [ ] Thực hiện đầy đủ các yêu cầu phần II (Linear filters)
- [ ] Thực hiện đầy đủ các yêu cầu phần III (Advanced techniques)
- [ ] Hiển thị đúng kết quả của từng phép xử lý
- [ ] So sánh được sự khác biệt giữa các phương pháp lọc
- [ ] Giải thích được tác dụng của từng kỹ thuật
- [ ] Mã nguồn rõ ràng, dễ hiểu và dễ mở rộng

---

## Implementation Notes

### Design Principles

- **Tính mô-đun**: Mỗi chức năng xử lý = một hàm riêng
- **Tính tái sử dụng**: Dễ dàng kế thừa và mở rộng
- **Tính đơn giản**: Ưu tiên triển khai đơn giản cho mục đích học tập
- **Tính linh hoạt**: Có thể mở rộng thành chương trình tương tác

### Default Parameters

- Giá trị độ sáng: ±50 (có thể điều chỉnh)
- Giá trị độ tương phản: 1.5 hoặc 0.7 (có thể điều chỉnh)
- Kernel size: 3x3 (mặc định)
- Threshold value: 128 (mặc định)

---

## Timeline & Milestones

| Phase   | Description         | Priority | Estimated Time |
| ------- | ------------------- | -------- | -------------- |
| Phase 1 | Setup & Image I/O   | High     | 1 session      |
| Phase 2 | Point Operators     | High     | 2 sessions     |
| Phase 3 | Linear Filters      | High     | 2 sessions     |
| Phase 4 | Advanced Techniques | Medium   | 3 sessions     |
| Phase 5 | Code Organization   | Medium   | 1 session      |
| Phase 6 | Final Deliverables  | High     | 1 session      |

---

## Dependencies & Resources

### External Files

- Ảnh mẫu để kiểm thử (sample images)

### References

- OpenCV Documentation
- NumPy Documentation
- Computer Vision Textbooks

---

## Risks & Mitigation

| Risk                      | Impact | Mitigation                  |
| ------------------------- | ------ | --------------------------- |
| Performance với ảnh lớn   | Medium | Tối ưu hóa hoặc resize ảnh  |
| Clipping pixel complexity | Low    | Sử dụng `np.clip()`         |
| Kernel design             | Medium | Bắt đầu với kernel đơn giản |
| Filter comparison         | Low    | Chuẩn bị metrics rõ ràng    |
