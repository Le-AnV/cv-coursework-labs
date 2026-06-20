"""
Wavelet Hash Engine - Extracted from notebook
This module contains the core functions for wavelet hashing as defined in self.ipynb
"""

import numpy as np
import cv2
import pywt
from typing import List, Tuple


def preprocess_image(
    image, image_size=128, color_space=cv2.COLOR_BGR2GRAY, remove_background=False
):
    """
    Preprocess image by removing background, resizing, and converting color space.

    Args:
        image (numpy.ndarray): Input image array (BGR/RGB).
        image_size (int): Target size for square resizing. Defaults to 128.
        color_space (int): Target OpenCV color conversion code. Defaults to cv2.COLOR_BGR2GRAY.
        remove_background (bool): Whether to remove background. Defaults to False.

    Returns:
        numpy.ndarray: Preprocessed grayscale image.
    """
    # Remove background
    if remove_background:
        from rembg import remove

        nobg_img = remove(image)
    else:
        nobg_img = image

    # Resize to squares
    resized_img = cv2.resize(nobg_img, (image_size, image_size))

    # Convert to grayscale based on channels
    if len(resized_img.shape) == 3 and resized_img.shape[2] == 4:
        processed_img = cv2.cvtColor(resized_img, cv2.COLOR_BGRA2GRAY)
    else:
        processed_img = cv2.cvtColor(resized_img, color_space)

    return processed_img


def wavelet_transform(image_path, wavelet="haar", level=4):
    """
    Reads an image, preprocesses it, and performs 2D Discrete Wavelet Decomposition.

    Parameters:
    - image_path (str): Path to the input image file.
    - wavelet (str): Name of the wavelet family to use (default is 'haar').
    - level (int): Decomposition level (default is 4).

    Returns:
    - list: Coefficients list [cA_n, (cH_n, cV_n, cD_n), ..., (cH_1, cV_1, cD_1)].
    """
    # Read image from path
    img = cv2.imread(image_path)

    # Resize and normalize image
    processed_img = preprocess_image(image=img, image_size=128, remove_background=False)

    # Perform multi-level 2D Discrete Wavelet Transform
    coeffs = pywt.wavedec2(
        data=processed_img,
        wavelet=wavelet,
        level=level,
    )

    return coeffs


def quantize_coefficients(coeffs, step=2):
    """
    Quantize multi-level wavelet coefficients using a uniform scalar step size.

    Args:
        coeffs (list): Multi-level wavelet coefficients from 'pywt.wavedec2'.
        step (int or float, optional): Quantization step size. Defaults to 2.

    Returns:
        list: Quantized coefficients with the exact same structure as input.
    """

    # Helper function for coefficient quantization
    def quantize_element(c, step=2):
        if isinstance(c, tuple):
            return tuple(np.round(a=arr / step) for arr in c)
        return np.round(a=c / step)

    # Quantize coefficients level by level
    quantized_coeffs = [quantize_element(c=c, step=step) for c in coeffs]

    return quantized_coeffs


def generate_hash(quantized_coeffs):
    """
    Generate binary hash from quantized wavelet coefficients.

    Args:
        quantized_coeffs (list): Quantized coefficients from quantize_coefficients().

    Returns:
        list: A 1D list of binary integers (0 or 1) representing the image hash.
    """
    # Take only cA (approximation coefficients)
    cA = quantized_coeffs[0]

    flattened = cA.flatten()

    median = np.median(flattened)
    hash_code = (flattened > median).astype(np.uint8)

    return hash_code.tolist()


def wavelet_hash(image_path, wavelet="haar", level=4, step=2) -> List[int]:
    """
    Generate a binary hash from an image by pipeline calling DWT, quantization, and hashing.

    Args:
        image_path (str): Path to the input image file.
        wavelet (str, optional): Wavelet type for decomposition. Defaults to "haar".
        level (int, optional): Decomposition level. Defaults to 4.
        step (int or float, optional): Quantization step size. Defaults to 2.

    Returns:
        list: A 1D list of binary integers (0 or 1) representing the image hash.
    """
    # Step 1: Perform 2D Discrete Wavelet Transform
    coeffs = wavelet_transform(image_path=image_path, wavelet=wavelet, level=level)

    # Step 2: Quantize the extracted coefficients
    quantized_coeffs = quantize_coefficients(coeffs=coeffs, step=step)

    # Step 3: Flatten and convert to final binary hash code
    hash_code = generate_hash(quantized_coeffs=quantized_coeffs)

    return hash_code


def hamming_distance(hash1: List[int], hash2: List[int]) -> int:
    """
    Calculate Hamming distance between two binary hashes.

    Args:
        hash1 (list): First binary hash.
        hash2 (list): Second binary hash.

    Returns:
        int: Hamming distance (number of differing bits).
    """
    if len(hash1) != len(hash2):
        raise ValueError("Binary strings must be equal length")
    return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
