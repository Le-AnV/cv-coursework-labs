"""
Flask Web Application for Image Retrieval using Wavelet Hashing
"""

import os
import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from werkzeug.utils import secure_filename
from hashing import wavelet_hash, hamming_distance
from hashing.cache_manager import HashCache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)

# Configuration
APP_ROOT = Path(__file__).resolve().parent
UPLOAD_FOLDER = APP_ROOT / "static" / "uploads"
CACHE_FOLDER = APP_ROOT / "cache"
DATASET_ROOT = Path(__file__).resolve().parent.parent / "assets" / "Animals-10"
DATASET_FOLDER = DATASET_ROOT / "original"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "tiff", "tif"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
TOP_K_RESULTS = 2
WAVELET_TYPE = "haar"

# Create necessary directories
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
CACHE_FOLDER.mkdir(parents=True, exist_ok=True)

# App config
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# Initialize cache manager
cache_manager = HashCache(cache_dir=str(CACHE_FOLDER))


def allowed_file(filename):
    """Check if file has allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_absolute_dataset_path():
    """Get absolute path to dataset folder."""
    return str(DATASET_FOLDER)


def build_dataset_image_url(image_path: str) -> str:
    """Convert a dataset file path into a browser-safe URL."""
    path_obj = Path(image_path)
    try:
        relative_path = path_obj.resolve().relative_to(DATASET_ROOT.resolve())
    except Exception:
        relative_path = path_obj.name

    return url_for(
        "serve_dataset_image", image_path=str(relative_path).replace("\\", "/")
    )


@app.route("/", methods=["GET"])
def index():
    """Render the home page."""
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload_image():
    """
    Handle image upload and process for search.

    Returns:
        JSON response with upload status and results
    """
    try:
        # Check if file is in request
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if not allowed_file(file.filename):
            return (
                jsonify(
                    {
                        "error": f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
                    }
                ),
                400,
            )

        # Generate unique filename
        filename = secure_filename(file.filename)
        timestamp = str(int(__import__("time").time() * 1000))
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # Save uploaded file
        file.save(filepath)
        logger.info(f"File uploaded: {filepath}")

        # Generate hash for uploaded image
        query_hash = wavelet_hash(filepath, wavelet=WAVELET_TYPE)
        logger.info(f"Generated hash for uploaded image: {len(query_hash)} bits")

        # Build/load dataset cache
        dataset_path = get_absolute_dataset_path()
        if not Path(dataset_path).exists():
            logger.warning(f"Dataset not found at {dataset_path}")
            return (
                jsonify({"error": f"Dataset folder not found at {dataset_path}"}),
                500,
            )

        cache_manager.build_dataset_cache(dataset_path, wavelet=WAVELET_TYPE)

        # Search for similar images
        results = cache_manager.search_similar(query_hash, top_k=TOP_K_RESULTS)

        if not results:
            return jsonify({"error": "No similar images found in dataset"}), 404

        # Format results
        formatted_results = []
        for rank, (image_path, distance, similarity) in enumerate(results, 1):
            try:
                image_name = Path(image_path).name
                image_url = build_dataset_image_url(image_path)

                formatted_results.append(
                    {
                        "rank": rank,
                        "name": image_name,
                        "path": image_path,
                        "image_url": image_url,
                        "hamming_distance": int(distance),
                        "similarity": f"{similarity:.2f}",
                        "total_bits": len(query_hash),
                    }
                )
            except Exception as e:
                logger.error(f"Error formatting result for {image_path}: {e}")

        response = {
            "success": True,
            "query_image": {
                "filename": filename,
                "path": url_for("static", filename=f"uploads/{filename}"),
                "hash_length": len(query_hash),
            },
            "results": formatted_results,
            "total_results": len(formatted_results),
        }

        logger.info(f"Search completed: found {len(formatted_results)} similar images")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error during image processing: {e}")
        return jsonify({"error": f"Error processing image: {str(e)}"}), 500


@app.route("/api/image/<path:filename>")
def serve_image(filename):
    """
    Serve images from any path (for dataset images).

    Args:
        filename (str): Full path to image file.

    Returns:
        Image file or error
    """
    try:
        # Security check: prevent path traversal
        filepath = Path(filename)

        # Check if file exists and is readable
        if not filepath.exists() or not filepath.is_file():
            logger.warning(f"Image not found: {filename}")
            return jsonify({"error": "Image not found"}), 404

        # Serve the file
        return send_from_directory(filepath.parent, filepath.name)
    except Exception as e:
        logger.error(f"Error serving image {filename}: {e}")
        return jsonify({"error": "Failed to serve image"}), 500


@app.route("/dataset-images/<path:image_path>")
def serve_dataset_image(image_path):
    """Serve images from the dataset folder."""
    try:
        file_path = (DATASET_ROOT / image_path).resolve()
        if not file_path.exists() or not file_path.is_file():
            logger.warning(f"Dataset image not found: {image_path}")
            return jsonify({"error": "Image not found"}), 404

        try:
            file_path.relative_to(DATASET_ROOT.resolve())
        except ValueError:
            return jsonify({"error": "Invalid image path"}), 400

        return send_from_directory(file_path.parent, file_path.name)
    except Exception as e:
        logger.error(f"Error serving dataset image {image_path}: {e}")
        return jsonify({"error": "Failed to serve image"}), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get statistics about the application."""
    try:
        dataset_path = get_absolute_dataset_path()
        dataset_size = len(
            [
                f
                for f in Path(dataset_path).rglob("*")
                if f.suffix.lower() in ALLOWED_EXTENSIONS
            ]
        )
        cached_images = len(cache_manager.hashes)

        return (
            jsonify(
                {
                    "dataset_size": dataset_size,
                    "cached_images": cached_images,
                    "cache_file_size": (
                        os.path.getsize(cache_manager.cache_file)
                        if cache_manager.cache_file.exists()
                        else 0
                    ),
                    "wavelet_type": WAVELET_TYPE,
                    "top_k_results": TOP_K_RESULTS,
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/clear-cache", methods=["POST"])
def clear_cache():
    """Clear the hash cache."""
    try:
        cache_manager.clear_cache()
        logger.info("Cache cleared by user")
        return jsonify({"success": True, "message": "Cache cleared successfully"}), 200
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        return jsonify({"error": str(e)}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return (
        jsonify(
            {
                "error": f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
            }
        ),
        413,
    )


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # Initialize dataset cache on startup
    try:
        dataset_path = get_absolute_dataset_path()
        if Path(dataset_path).exists():
            logger.info(f"Building initial dataset cache from {dataset_path}")
            cache_manager.build_dataset_cache(dataset_path, wavelet=WAVELET_TYPE)
        else:
            logger.warning(f"Dataset not found at {dataset_path}")
    except Exception as e:
        logger.error(f"Error building initial cache: {e}")

    # Run Flask app
    app.run(debug=True, host="0.0.0.0", port=5000)
