# Implementation Plan: Flask Image Processor

---

## 1. Thông Tin Dự Án

| Mục           | Chi tiết              |
| ------------- | --------------------- |
| **Ngôn ngữ**  | Python 3.10s          |
| **Framework** | Flask                 |
| **Xử lý ảnh** | OpenCV, NumPy         |
| **Frontend**  | HTML5, CSS3 (vanilla) |
| **Đóng gói**  | Docker                |
| **Deploy**    | Docker Hub → Cloud    |

---

## 2. Cấu Trúc Thư Mục

```
flask-image-processor/
│
├── app.py                  # Flask app chính, định nghĩa các route
├── requirements.txt        # Thư viện Python
├── Dockerfile              # Build image Docker
├── .dockerignore
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   └── index.html
│
└── uploads/                # Thư mục tạm (tạo lúc runtime, không commit)
```

---

## 3. Chi Tiết Các Route Flask

| Route       | Method | Mô tả                                                     |
| ----------- | ------ | --------------------------------------------------------- |
| `/`         | GET    | Render trang chủ `index.html`                             |
| `/process`  | POST   | Nhận ảnh + tham số, xử lý, trả về ảnh kết quả dạng base64 |
| `/download` | POST   | Nhận ảnh đã xử lý, trả về file để tải về                  |

> Không dùng session, không lưu file lâu dài — ảnh xử lý xong trả thẳng về response.

---

## 4. Các Chức Năng Xử Lý Ảnh

### 4.1. Chuyển Đổi Không Gian Màu

```
convert_color(image, mode)
  mode = "HSV"  → cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  mode = "LAB"  → cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
  mode = "L"    → tách kênh L từ LAB, trả về ảnh grayscale
```

### 4.2. Crop Ảnh

```
crop_image(image, x, y, width, height)
  → Validate: x+width <= img.width, y+height <= img.height
  → Return: img[y:y+height, x:x+width]
```

### 4.3. Resize Ảnh

```
resize_image(image, new_width, new_height, keep_ratio=False)
  → Nếu keep_ratio: tính lại width/height theo tỉ lệ gốc
  → Thu nhỏ: INTER_AREA
  → Phóng to: INTER_LINEAR
```

---

## 5. Luồng Xử Lý Chính (Request Flow)

```
User chọn ảnh + chọn thao tác + nhập tham số
        │
        ▼
POST /process  (multipart/form-data)
        │
        ├── Đọc file ảnh từ request
        ├── Decode sang numpy array (cv2.imdecode)
        ├── Gọi hàm xử lý tương ứng
        ├── Encode kết quả sang base64 PNG
        └── Trả về JSON { image_base64, width, height }
        │
        ▼
Frontend hiển thị preview ảnh kết quả
        │
        ▼
User nhấn "Tải về"
        │
        ▼
POST /download  → trả về file PNG (send_file với mimetype image/png)
```

---

## 6. Giao Diện (Frontend)

Một trang duy nhất `index.html` gồm:

- **Upload zone:** Input file + preview ảnh gốc
- **Control panel:** Tabs hoặc select để chọn chức năng
  - Tab Color Space: radio chọn HSV / LAB / L
  - Tab Crop: input x, y, width, height
  - Tab Resize: input width, height + checkbox keep ratio
- **Nút "Xử lý":** Gửi request AJAX đến `/process`
- **Vùng kết quả:** Hiển thị ảnh sau xử lý + thông tin kích thước
- **Nút "Tải về":** Gửi request đến `/download`

---

## 7. requirements.txt

```
flask==3.0.3
opencv-python-headless==4.9.0.80
numpy==1.26.4
```

> Dùng `opencv-python-headless` (không GUI) phù hợp môi trường Docker/server.

---

## 8. Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads

EXPOSE 5000

CMD ["python", "app.py"]
```

---

## 9. .dockerignore

```
__pycache__/
*.pyc
*.pyo
uploads/
.env
.git
```

---

## 10. Kế Hoạch Triển Khai (Deploy)

```
Bước 1: Build image
  docker build -t flask-image-processor .

Bước 2: Test local
  docker run -p 5000:5000 flask-image-processor
  → Truy cập http://localhost:5000

Bước 3: Tag image
  docker tag flask-image-processor <dockerhub_username>/flask-image-processor:latest

Bước 4: Push lên Docker Hub (bạn tự thực hiện)
  docker push <dockerhub_username>/flask-image-processor:latest

Bước 5: Pull và chạy trên cloud
  docker pull <dockerhub_username>/flask-image-processor:latest
  docker run -d -p 5000:5000 flask-image-processor
```

---

## 11. Thứ Tự Implement

| Bước | File                   | Nội dung                                           |
| ---- | ---------------------- | -------------------------------------------------- |
| 1    | `requirements.txt`     | Khai báo thư viện                                  |
| 2    | `app.py`               | Khởi tạo Flask, viết 3 route và các hàm xử lý ảnh  |
| 3    | `templates/index.html` | Giao diện upload, control panel, preview, download |
| 4    | `static/css/style.css` | Styling giao diện                                  |
| 5    | `Dockerfile`           | Đóng gói ứng dụng                                  |
| 6    | `.dockerignore`        | Loại trừ file không cần thiết                      |
| 7    | Test local             | Chạy `python app.py` rồi test từng chức năng       |
| 8    | Test Docker            | Build và chạy container, kiểm tra lại              |

---

## 12. Các Điểm Lưu Ý Kỹ Thuật

- **Không lưu file:** Ảnh được xử lý hoàn toàn trong bộ nhớ (in-memory), không ghi ra disk, tránh vấn đề dọn dẹp file tạm trên server
- **Base64 transfer:** Ảnh kết quả trả về dạng base64 trong JSON để hiển thị preview, sau đó dùng lại khi download
- **opencv-python-headless:** Bắt buộc dùng bản headless trong Docker vì không có display server
- **Flask debug mode:** Tắt khi build production (`debug=False` hoặc dùng biến môi trường `FLASK_ENV=production`)
- **File size limit:** Giới hạn upload tối đa 10MB bằng `app.config['MAX_CONTENT_LENGTH']`
