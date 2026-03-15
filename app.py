import os
import sys
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OUTPUT_FOLDER = "downloaded_videos"

def ensure_folder():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

<<<<<<< HEAD
def build_command(url, mode, quality="720"):
=======
def build_command(url, mode):
>>>>>>> 062ae2ca8c5fe4ccf7f9416bafb2edc322af802c
    base = [sys.executable, "-m", "yt_dlp", "-o",
            os.path.join(OUTPUT_FOLDER, "%(title)s.%(ext)s")]

    if mode == "audio":
        # Extract audio as MP3
        base += ["-x", "--audio-format", "mp3", "--audio-quality", "0"]
    elif mode == "playlist":
<<<<<<< HEAD
        # Download full playlist at selected quality
        base += ["-f", f"best[height<={quality}][ext=mp4]", "--yes-playlist"]
    else:
        # Single video selected quality
        base += ["-f", f"best[height<={quality}][ext=mp4]", "--no-playlist"]
=======
        # Download full playlist at 720p
        base += ["-f", "best[height<=720][ext=mp4]", "--yes-playlist"]
    else:
        # Single video 720p
        base += ["-f", "best[height<=720][ext=mp4]", "--no-playlist"]
>>>>>>> 062ae2ca8c5fe4ccf7f9416bafb2edc322af802c

    base.append(url)
    return base

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url", "").strip()
    mode = data.get("mode", "video")  # video | audio | playlist
<<<<<<< HEAD
    quality = data.get("quality", "720")
=======
>>>>>>> 062ae2ca8c5fe4ccf7f9416bafb2edc322af802c

    if not url:
        return jsonify({"success": False, "message": "No URL provided."}), 400

    ensure_folder()
<<<<<<< HEAD
    command = build_command(url, mode, quality)
=======
    command = build_command(url, mode)
>>>>>>> 062ae2ca8c5fe4ccf7f9416bafb2edc322af802c

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        return jsonify({
            "success": True,
            "message": "Download completed successfully!",
            "output": result.stdout[-500:] if result.stdout else ""
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "success": False,
            "message": "Download failed. Check the URL and try again.",
            "error": e.stderr[-300:] if e.stderr else ""
        }), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
