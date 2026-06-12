# Problem Definition: Ứng Dụng Xử Lý Ảnh Web (Flask Image Processing App)

---

## 1. Tổng Quan Dự Án

**Tên dự án:** Flask Image Processor  
**Ngôn ngữ lập trình:** Python  
**Framework:** Flask (backend) + HTML/CSS (frontend)  
**Mục tiêu:** Xây dựng một web application cho phép người dùng tải ảnh lên, thực hiện các thao tác xử lý ảnh cơ bản và tải về kết quả.

---

## 2. Phát Biểu Bài Toán

Hiện nay, người dùng thường phải cài đặt phần mềm phức tạp (Photoshop, GIMP, OpenCV script...) để thực hiện các thao tác xử lý ảnh cơ bản như chuyển đổi không gian màu hoặc cắt/thay đổi kích thước ảnh. Bài toán đặt ra là **xây dựng một công cụ xử lý ảnh đơn giản, chạy trên nền web**, không yêu cầu cài đặt phần mềm phía người dùng, dễ sử dụng và trả về kết quả có thể tải về ngay lập tức.

---

## 3. Đầu Vào (Input)

| Thành phần           | Mô tả                                                    |
| -------------------- | -------------------------------------------------------- |
| **File ảnh**         | Người dùng tải lên từ máy tính qua giao diện web         |
| **Định dạng hỗ trợ** | `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`                 |
| **Tham số xử lý**    | Người dùng chọn loại thao tác và nhập thông số tương ứng |

---

## 4. Các Chức Năng Xử Lý (Processing Features)

### 4.1. Chuyển Đổi Không Gian Màu (Color Space Conversion)

| Chức năng               | Mô tả                                                                 |
| ----------------------- | --------------------------------------------------------------------- |
| **BGR → HSV**           | Chuyển ảnh sang không gian màu Hue-Saturation-Value                   |
| **BGR → LAB**           | Chuyển ảnh sang không gian màu CIE L\*a\*b\* (toàn bộ 3 kênh)         |
| **BGR → L (Lightness)** | Trích xuất kênh L từ không gian LAB — ảnh grayscale biểu diễn độ sáng |

### 4.2. Crop Ảnh (Image Cropping)

- Người dùng nhập tọa độ cắt: `x_start`, `y_start`, `width`, `height`
- Ảnh được cắt theo vùng chỉ định
- Kiểm tra tính hợp lệ của tọa độ (không vượt kích thước ảnh gốc)

### 4.3. Resize Ảnh (Image Resizing)

- Người dùng nhập kích thước mong muốn: `width` × `height` (pixel)
- Hỗ trợ tùy chọn giữ nguyên tỉ lệ khung hình (keep aspect ratio)
- Sử dụng phép nội suy phù hợp (INTER_AREA cho thu nhỏ, INTER_LINEAR cho phóng to)

---

## 5. Đầu Ra (Output)

| Thành phần         | Mô tả                                                     |
| ------------------ | --------------------------------------------------------- |
| **Ảnh kết quả**    | Hiển thị preview trực tiếp trên trình duyệt sau khi xử lý |
| **Tải về**         | Nút download để lưu ảnh đã xử lý về máy tính              |
| **Định dạng xuất** | `.png` (mặc định, đảm bảo không mất chất lượng)           |
| **Thông tin ảnh**  | Hiển thị kích thước ảnh gốc và ảnh kết quả                |

---

## 6. Kiến Trúc Hệ Thống

```
[Trình duyệt (HTML/CSS)]
        │
        │  HTTP Request (multipart/form-data)
        ▼
[Flask Server (Python)]
        │
        ├── /upload         → Nhận và lưu ảnh tạm thời
        ├── /process        → Xử lý ảnh theo tham số
        └── /download       → Trả về file ảnh đã xử lý
        │
        ▼
[OpenCV / Pillow (xử lý ảnh)]
        │
        ▼
[File hệ thống tạm (temp folder)]
```

---

## 7. Công Nghệ Sử Dụng

| Thành phần      | Công nghệ                                    |
| --------------- | -------------------------------------------- |
| **Backend**     | Python 3.x, Flask                            |
| **Xử lý ảnh**   | OpenCV (`cv2`), NumPy                        |
| **Frontend**    | HTML5, CSS3 (vanilla)                        |
| **Giao tiếp**   | HTTP REST (form submission)                  |
| **Lưu trữ tạm** | Thư mục `uploads/` và `outputs/` trên server |

---

## 8. Cấu Trúc Thư Mục Dự Kiến

```
flask-image-processor/
│
├── app.py                  # Flask application chính
├── requirements.txt        # Danh sách thư viện
│
├── static/
│   └── css/
│       └── style.css       # Stylesheet
│
├── templates/
│   └── index.html          # Giao diện chính
│
├── uploads/                # Ảnh gốc tải lên (tạm thời)
└── outputs/                # Ảnh kết quả (tạm thời)
```

---

## 9. Yêu Cầu Phi Chức Năng

- **Đơn giản:** Giao diện rõ ràng, dễ sử dụng, không yêu cầu đăng nhập
- **Nhẹ:** Không dùng database, không framework CSS phức tạp
- **Bảo mật cơ bản:** Kiểm tra định dạng file tải lên, giới hạn kích thước file
- **Dọn dẹp:** Tự động xóa file tạm sau khi người dùng tải về

---

## 10. Phạm Vi Ngoài Dự Án (Out of Scope)

- Xác thực người dùng / đăng nhập
- Lưu lịch sử ảnh
- Xử lý hàng loạt nhiều ảnh cùng lúc
- Deploy lên cloud (chỉ chạy local)
- Các thao tác xử lý ảnh nâng cao (filter, detect object, v.v.)

---

## 11. Tiêu Chí Hoàn Thành (Definition of Done)

- [ ] Người dùng có thể tải ảnh lên từ máy tính
- [ ] Chuyển đổi sang HSV hiển thị đúng kết quả
- [ ] Chuyển đổi sang LAB hiển thị đúng kết quả
- [ ] Trích xuất kênh L (Lightness) hoạt động đúng
- [ ] Crop ảnh theo tọa độ nhập vào hoạt động đúng
- [ ] Resize ảnh theo kích thước nhập vào hoạt động đúng
- [ ] Ảnh kết quả hiển thị preview trên trình duyệt
- [ ] Nút tải về hoạt động và lưu đúng file
