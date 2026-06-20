# Implementation

# Image Retrieval System using Wavelet Hashing

## 1. System Architecture

Hệ thống được xây dựng theo mô hình Client–Server với kiến trúc ba tầng:
ss

```
+------------------------------------------------------+
|                     Client Browser                   |
|------------------------------------------------------|
| HTML | CSS | Bootstrap | JavaScript | Fetch API      |
+-------------------------+----------------------------+
                          |
                          | HTTP Request / Response
                          |
+-------------------------v----------------------------+
|                   Flask Web Server                   |
|------------------------------------------------------|
| Routing | Business Logic | Image Processing | Search |
+-------------------------+----------------------------+
                          |
        +-----------------+------------------+
        |                                    |
        |                                    |
+-------v--------+                  +--------v---------+
| Uploaded Image |                  | Dataset Images   |
| (User Query)   |                  | (Local Folder)   |
+-------+--------+                  +--------+---------+
        |                                    |
        |                                    |
        +-----------------+------------------+
                          |
                          v
                Image Preprocessing Module
                          |
                          v
                 Wavelet Hash Generation
                          |
                          v
                 Hamming Distance Matching
                          |
                          v
                  Ranking & Top-K Results
                          |
                          v
                 Render Result to Browser
```

---

# 2. Technology Stack

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
- Bootstrap 5
- JavaScript (ES6)
- Fetch API (tùy chọn)

## Data Storage

- Dataset lưu trên thư mục cục bộ.
- Hash được lưu trong bộ nhớ hoặc file cache (`pickle` hoặc `JSON`) để giảm thời gian xử lý.

---

# 3. Directory Structure

```
image-retrieval/
│
├── app.py
├── requirements.txt
│
├── static/
│   ├── css/
│   │     style.css
│   │
│   ├── js/
│   │     app.js
│   │
│   ├── uploads/
│   │
│   └── dataset/
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── hashing/
│   ├── preprocessing.py
│   ├── wavelet_hash.py
│   ├── hamming.py
│   └── search_engine.py
│
├── cache/
│   └── hashes.pkl
│
└── README.md
```

---

# 4. System Workflow

## Step 1: User Upload

Người dùng chọn một ảnh từ máy tính và gửi đến Flask Server thông qua biểu mẫu trên giao diện web.

---

## Step 2: Image Preprocessing

Ảnh được chuẩn hóa trước khi tạo hash nhằm giảm ảnh hưởng của các khác biệt không cần thiết.

Các bước tiền xử lý có thể bao gồm:

1. Đọc ảnh.
2. Chuyển sang grayscale.
3. Resize về kích thước cố định.
4. Chuẩn hóa dữ liệu.
5. (Tùy chọn) áp dụng bộ lọc làm mượt để giảm nhiễu.

---

## Step 3: Wavelet Hash Generation

Sau tiền xử lý:

1. Áp dụng biến đổi Wavelet.
2. Trích xuất các hệ số xấp xỉ.
3. Lượng tử hóa hệ số.
4. Chuyển thành chuỗi bit nhị phân.
5. Sinh mã Wavelet Hash đại diện cho ảnh.

---

## Step 4: Dataset Hash Loading

Đối với tập dữ liệu:

- Nếu hash đã được tính trước thì đọc trực tiếp từ cache.
- Nếu chưa có cache thì tính hash cho toàn bộ ảnh và lưu lại.

Việc tiền tính hash giúp giảm đáng kể thời gian truy vấn.

---

## Step 5: Similarity Computation

Với mỗi ảnh trong dataset:

```
distance = Hamming(query_hash, dataset_hash)
```

Khoảng cách càng nhỏ thì hai ảnh càng giống nhau.

---

## Step 6: Ranking

Sau khi tính khoảng cách Hamming:

- Sắp xếp theo thứ tự tăng dần.
- Lấy Top-K ảnh gần nhất.
- Chuẩn bị dữ liệu trả về giao diện.

---

## Step 7: Display Result

Trang kết quả hiển thị:

- Ảnh truy vấn.
- Danh sách ảnh tương tự.
- Thứ hạng.
- Khoảng cách Hamming.
- (Tùy chọn) tỷ lệ tương đồng được suy diễn từ khoảng cách.

---

# 5. Core Algorithm

```
function Search(query_image):

    query_hash = GenerateWaveletHash(query_image)

    results = []

    for image in dataset:

        dataset_hash = image.hash

        distance = Hamming(query_hash, dataset_hash)

        results.append(
            (image, distance)
        )

    sort(results by distance ascending)

    return TopK(results)
```

---

# 6. Preprocessing Pipeline

```
Original Image
        │
        ▼
Read Image
        │
        ▼
Resize
        │
        ▼
Convert to Grayscale
        │
        ▼
(Optional) Denoising
        │
        ▼
Wavelet Transform
        │
        ▼
Generate Hash
```

---

# 7. Frontend Components

## index.html

Chức năng:

- Chọn ảnh.
- Xem trước ảnh.
- Gửi yêu cầu tìm kiếm.
- Hiển thị trạng thái đang xử lý.

## result.html

Hiển thị:

- Ảnh đầu vào.
- Top-K kết quả.
- Khoảng cách Hamming.
- Thông tin xếp hạng.

## style.css

Định nghĩa:

- Responsive layout.
- Card hiển thị ảnh.
- Hiệu ứng hover.
- Khoảng cách và kiểu chữ.

## app.js

Xử lý:

- Preview ảnh trước khi upload.
- Kiểm tra định dạng tệp.
- Hiển thị loading spinner.
- Gửi request bằng Fetch API hoặc biểu mẫu HTML.

---

# 8. Caching Strategy

Để tối ưu hiệu năng:

- Hash của dataset được tính một lần.
- Kết quả lưu vào `cache/hashes.pkl`.
- Chỉ tính lại khi dataset thay đổi.

Ví dụ:

```
dataset/
    cat1.jpg
    cat2.jpg
    dog3.jpg

↓

hashes.pkl

{
    "cat1.jpg": "...",
    "cat2.jpg": "...",
    "dog3.jpg": "..."
}
```

---

# 9. Time Complexity

Giả sử:

- `N` là số lượng ảnh trong dataset.
- `L` là độ dài mã hash.

Thời gian cho một truy vấn:

- Sinh hash ảnh đầu vào: `O(L)`.
- So sánh với toàn bộ dataset: `O(N × L)`.
- Sắp xếp kết quả: `O(N log N)`.

Với `L` cố định, chi phí chủ yếu tăng theo số lượng ảnh `N`.

---

# 10. Error Handling

Hệ thống cần xử lý các trường hợp:

- Người dùng không chọn ảnh.
- Định dạng tệp không hợp lệ.
- Ảnh bị hỏng hoặc không đọc được.
- Dataset rỗng.
- Không tìm thấy ảnh tương tự.
- Lỗi trong quá trình sinh hash.

Thông báo lỗi phải rõ ràng và không làm dừng toàn bộ ứng dụng.

---

# 11. Security Considerations

- Giới hạn định dạng tệp tải lên (`jpg`, `jpeg`, `png`).
- Kiểm tra kích thước tệp để tránh tải lên quá lớn.
- Đổi tên tệp tải lên nhằm tránh ghi đè hoặc khai thác đường dẫn.
- Không thực thi bất kỳ nội dung nào từ phía người dùng.
- Lưu ảnh tải lên trong thư mục riêng biệt và có cơ chế dọn dẹp định kỳ nếu cần.

---

# 12. Scalability

Khi quy mô dữ liệu tăng:

- Chuyển từ lưu hash trong file sang SQLite hoặc PostgreSQL.
- Lưu hash dưới dạng cấu trúc nhị phân để giảm dung lượng.
- Thêm cơ chế lập chỉ mục hoặc tiền xử lý để tăng tốc truy vấn.
- Tách riêng các thành phần giao diện và xử lý nghiệp vụ nếu cần triển khai ở quy mô lớn.

---

# 13. Expected Implementation Outcome

Sau khi triển khai, hệ thống có thể:

- Nhận ảnh đầu vào từ người dùng thông qua giao diện web.
- Sinh Wavelet Hash cho ảnh truy vấn.
- So sánh với các hash đã lưu của tập dữ liệu.
- Tính khoảng cách Hamming và xếp hạng kết quả.
- Trả về Top-K ảnh tương tự với thời gian phản hồi ngắn và kiến trúc đủ rõ ràng để mở rộng trong tương lai.
