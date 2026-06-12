from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import cv2
import io
import base64

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB


def read_image_from_file_storage(fs):
    data = fs.read()
    arr = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img


def encode_image_to_base64(img):
    success, buf = cv2.imencode(".png", img)
    if not success:
        raise RuntimeError("Failed to encode image")
    b = base64.b64encode(buf.tobytes()).decode("utf-8")
    return f"data:image/png;base64,{b}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files["image"]
    img = read_image_from_file_storage(file)
    if img is None:
        return jsonify({"error": "Cannot decode image"}), 400

    action = request.form.get("action", "CROP")

    try:
        if action == "GRAYSCALE":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            out = gray
        elif action == "CROP":
            x = int(request.form.get("x", 0))
            y = int(request.form.get("y", 0))
            w = int(request.form.get("width", 0))
            h = int(request.form.get("height", 0))
            h_img, w_img = img.shape[:2]
            if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > w_img or y + h > h_img:
                return jsonify({"error": "Invalid crop coordinates"}), 400
            out = img[y : y + h, x : x + w]
        elif action == "RESIZE":
            new_w = int(request.form.get("width", 0))
            new_h = int(request.form.get("height", 0))
            keep = request.form.get("keep_ratio", "false").lower() == "true"
            h_img, w_img = img.shape[:2]
            if keep and new_w > 0 and new_h > 0:
                # compute ratio-based dims by fitting to requested box
                aspect = w_img / h_img
                if new_w / new_h > aspect:
                    new_w = int(new_h * aspect)
                else:
                    new_h = int(new_w / aspect)
            if new_w <= 0 or new_h <= 0:
                return jsonify({"error": "Invalid resize dimensions"}), 400
            if new_w < w_img or new_h < h_img:
                interp = cv2.INTER_AREA
            else:
                interp = cv2.INTER_LINEAR
            out = cv2.resize(img, (new_w, new_h), interpolation=interp)
        else:
            return jsonify({"error": "Unknown action"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Prepare base64
    img_base64 = encode_image_to_base64(out)

    h_out, w_out = out.shape[:2]
    return jsonify({"image_base64": img_base64, "width": w_out, "height": h_out})


@app.route("/download", methods=["POST"])
def download():
    data = request.get_json(force=True)
    b64 = data.get("image_base64")
    if not b64:
        return jsonify({"error": "No image data"}), 400
    if b64.startswith("data:image"):
        b64 = b64.split(",", 1)[1]
    raw = base64.b64decode(b64)
    return send_file(
        io.BytesIO(raw),
        mimetype="image/png",
        as_attachment=True,
        download_name="result.png",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
