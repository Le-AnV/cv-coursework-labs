"""
Cache Manager - Handles caching of dataset hashes
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
import pickle
from .wavelet_hash_engine import wavelet_hash
import logging

logger = logging.getLogger(__name__)


class HashCache:
    """Manages caching of image hashes from dataset."""

    def __init__(self, cache_dir: str = "cache"):
        """
        Initialize the cache manager.

        Args:
            cache_dir (str): Directory to store cache files. Defaults to "cache".
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        self.cache_file = self.cache_dir / "hashes.pkl"
        self.metadata_file = self.cache_dir / "metadata.json"
        self.hashes = {}
        self.load_cache()

    def load_cache(self):
        """Load cached hashes from disk."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "rb") as f:
                    self.hashes = pickle.load(f)
                logger.info(f"Loaded {len(self.hashes)} cached hashes")
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")
                self.hashes = {}
        else:
            self.hashes = {}

    def save_cache(self):
        """Save hashes to disk."""
        try:
            with open(self.cache_file, "wb") as f:
                pickle.dump(self.hashes, f)
            logger.info("Cache saved successfully")
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")

    def get_hash(self, image_path: str) -> List[int]:
        """
        Get hash for image, either from cache or by computing it.

        Args:
            image_path (str): Path to the image.

        Returns:
            list: Binary hash.
        """
        if image_path in self.hashes:
            return self.hashes[image_path]

        return None

    def set_hash(self, image_path: str, hash_value: List[int]):
        """
        Store hash in cache.

        Args:
            image_path (str): Path to the image.
            hash_value (list): Binary hash.
        """
        self.hashes[image_path] = hash_value

    def clear_cache(self):
        """Clear all cached hashes."""
        self.hashes = {}
        if self.cache_file.exists():
            os.remove(self.cache_file)
        logger.info("Cache cleared")

    def build_dataset_cache(
        self, dataset_dir: str, wavelet: str = "haar"
    ) -> Dict[str, List[int]]:
        """
        Build hash cache for all images in dataset directory.

        Args:
            dataset_dir (str): Path to dataset directory.
            wavelet (str): Wavelet type to use. Defaults to "haar".

        Returns:
            dict: Mapping of image paths to hashes.
        """
        dataset_path = Path(dataset_dir)
        if not dataset_path.exists():
            logger.warning(f"Dataset directory not found: {dataset_dir}")
            return {}

        image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}
        cached_count = 0
        computed_count = 0

        for image_file in sorted(dataset_path.rglob("*")):
            if image_file.is_file() and image_file.suffix.lower() in image_extensions:
                image_path_str = str(image_file)

                # Check if already cached
                if image_path_str in self.hashes:
                    cached_count += 1
                    continue

                try:
                    hash_value = wavelet_hash(image_path_str, wavelet=wavelet)
                    self.hashes[image_path_str] = hash_value
                    computed_count += 1
                    logger.debug(f"Computed hash for {image_file.name}")
                except Exception as e:
                    logger.error(f"Failed to compute hash for {image_path_str}: {e}")

        if computed_count > 0:
            self.save_cache()

        logger.info(
            f"Dataset cache: {cached_count} from cache, {computed_count} newly computed"
        )
        return self.hashes

    def search_similar(
        self, query_hash: List[int], top_k: int = 5
    ) -> List[Tuple[str, int, float]]:
        """
        Find top-K similar images based on Hamming distance.

        Args:
            query_hash (list): Binary hash of query image.
            top_k (int): Number of top results to return. Defaults to 5.

        Returns:
            list: List of tuples (image_path, hamming_distance, similarity_percentage).
        """
        from .wavelet_hash_engine import hamming_distance

        if not self.hashes:
            logger.warning("No cached hashes available for comparison")
            return []

        distances = []
        total_bits = len(query_hash) if query_hash else 0

        for image_path, cached_hash in self.hashes.items():
            try:
                distance = hamming_distance(query_hash, cached_hash)
                similarity = (1 - distance / total_bits) * 100 if total_bits > 0 else 0
                distances.append((image_path, distance, similarity))
            except Exception as e:
                logger.debug(f"Error comparing with {image_path}: {e}")

        # Sort by Hamming distance (ascending)
        distances.sort(key=lambda x: x[1])

        return distances[:top_k]
