import cv2
import numpy as np


def rotate_and_crop(
    image: np.ndarray,
    angle_range: tuple[float, float] = (-5, 5),
) -> np.ndarray:
    """
    Xoay ảnh với góc ngẫu nhiên, crop nhẹ vùng trung tâm và
    resize về kích thước ban đầu.

    Args:
        image (np.ndarray): Ảnh đầu vào.
        angle_range (tuple): Khoảng góc xoay (độ), ví dụ (-5, 5).

    Returns:
        np.ndarray: Ảnh sau khi xoay.
    """
    if image is None:
        raise ValueError("Input image is None.")

    # Chọn góc xoay ngẫu nhiên
    angle = np.random.uniform(
        low=angle_range[0],
        high=angle_range[1],
    )

    # Kích thước ảnh
    height, width = image.shape[:2]
    center = (width / 2, height / 2)

    # Ma trận xoay
    rotation_matrix = cv2.getRotationMatrix2D(
        center=center,
        angle=angle,
        scale=1.0,
    )

    # Xoay ảnh
    rotated = cv2.warpAffine(
        src=image,
        M=rotation_matrix,
        dsize=(width, height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT,
    )

    # Crop 95% vùng trung tâm
    crop_ratio = 0.95
    crop_width = int(width * crop_ratio)
    crop_height = int(height * crop_ratio)

    start_x = (width - crop_width) // 2
    start_y = (height - crop_height) // 2

    cropped = rotated[
        start_y : start_y + crop_height,
        start_x : start_x + crop_width,
    ]

    # Resize về kích thước ban đầu
    result = cv2.resize(
        src=cropped,
        dsize=(width, height),
        interpolation=cv2.INTER_LINEAR,
    )

    return result
