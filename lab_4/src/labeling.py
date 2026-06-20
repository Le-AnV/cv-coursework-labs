import os
import random
import pandas as pd

# Đường dẫn thư mục chứa ảnh gốc
original_dir = "../assets/Animals-10/original"

# Lấy danh sách file ảnh
filenames = sorted(
    [filename for filename in os.listdir(original_dir) if filename.endswith(".png")]
)

# Đặt seed để kết quả có thể tái lập
random.seed(42)

rows = []

for filename in filenames:
    stem = filename.removesuffix(".png")

    # ==========================
    # Positive pairs (label = 1)
    # ==========================

    # Original -> Noise (cùng ảnh)
    rows.append(
        {
            "image_1": f"assets/Animals-10/original/{filename}",
            "image_2": f"assets/Animals-10/noise/{stem}_noise.png",
            "transform": "gaussian_noise",
            "label": 1,
        }
    )

    # Original -> Rotation (cùng ảnh)
    rows.append(
        {
            "image_1": f"assets/Animals-10/original/{filename}",
            "image_2": f"assets/Animals-10/rotate/{stem}_rotate.png",
            "transform": "rotation",
            "label": 1,
        }
    )

    # ==========================
    # Negative pairs (label = 0)
    # ==========================

    # Chọn ngẫu nhiên một ảnh KHÁC
    other_filename = random.choice([f for f in filenames if f != filename])
    other_stem = other_filename.removesuffix(".png")

    # Original -> Original khác ảnh
    rows.append(
        {
            "image_1": f"assets/Animals-10/original/{filename}",
            "image_2": f"assets/Animals-10/original/{other_filename}",
            "transform": "different_original",
            "label": 0,
        }
    )

    # Original -> Noise của ảnh khác
    rows.append(
        {
            "image_1": f"assets/Animals-10/original/{filename}",
            "image_2": f"assets/Animals-10/noise/{other_stem}_noise.png",
            "transform": "different_noise",
            "label": 0,
        }
    )

    # Original -> Rotation của ảnh khác
    rows.append(
        {
            "image_1": f"assets/Animals-10/original/{filename}",
            "image_2": f"assets/Animals-10/rotate/{other_stem}_rotate.png",
            "transform": "different_rotation",
            "label": 0,
        }
    )

# Tạo DataFrame
df = pd.DataFrame(rows)

# Lưu ra CSV
df.to_csv(
    "../assets/image_pairs.csv",
    index=False,
)

print(df.head())
print()
print(df["label"].value_counts())
