import numpy as np


def add_gaussian_noise(
    image: np.ndarray,
    mean: float = 0,
    sigma_range: tuple[float, float] = (10, 25),
) -> np.ndarray:
    """
    Thêm Gaussian noise với sigma được chọn ngẫu nhiên.

    Args:
        image (np.ndarray): Ảnh đầu vào.
        mean (float): Trung bình của Gaussian noise.
        sigma_range (tuple): Khoảng giá trị sigma (min, max).

    Returns:
        np.ndarray: Ảnh sau khi thêm nhiễu.
    """
    if image is None:
        raise ValueError("Input image is None.")

    # Chọn sigma ngẫu nhiên
    sigma = np.random.uniform(
        low=sigma_range[0],
        high=sigma_range[1],
    )

    # Sinh Gaussian noise
    noise = np.random.normal(
        loc=mean,
        scale=sigma,
        size=image.shape,
    ).astype(np.float32)

    # Cộng noise và giới hạn giá trị pixel
    noisy_img = np.clip(
        a=image.astype(np.float32) + noise,
        a_min=0,
        a_max=255,
    ).astype(np.uint8)

    return noisy_img
