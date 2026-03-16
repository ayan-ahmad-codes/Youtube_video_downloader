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

def build_command(url, mode, quality="720"):
    if "spotify.com" in url.lower():
        # SpotDL natively handles Spotify (song, album, playlist)
        # We run it with output path directed to OUTPUT_FOLDER
        return [sys.executable, "-m", "spotdl", "--output", f"{OUTPUT_FOLDER}/{{artists}} - {{title}}.{{ext}}", url]

    base = [sys.executable, "-m", "yt_dlp", "-o",
            os.path.join(OUTPUT_FOLDER, "%(title)s.%(ext)s")]

    if mode == "audio":
        # Extract audio as MP3
        base += ["-x", "--audio-format", "mp3", "--audio-quality", "0"]
    elif mode == "playlist":
        # Download full playlist at selected quality
        base += ["-f", f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best", "--merge-output-format", "mp4", "--yes-playlist"]
    else:
        # Single video selected quality
        base += ["-f", f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best", "--merge-output-format", "mp4", "--no-playlist"]

    base.append(url)
    return base

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url", "").strip()
    mode = data.get("mode", "video")  # video | audio | playlist
    quality = data.get("quality", "720")

    if not url:
        return jsonify({"success": False, "message": "No URL provided."}), 400

    ensure_folder()
    command = build_command(url, mode, quality)

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        out_str = str(result.stdout) if result.stdout else ""
        out_clip = out_str[len(out_str)-500:] if len(out_str) > 500 else out_str
        return jsonify({
            "success": True,
            "message": "Download completed successfully!",
            "output": out_clip
        })
    except subprocess.CalledProcessError as e:
        err_str = str(e.stderr) if e.stderr else ""
        err_clip = err_str[len(err_str)-300:] if len(err_str) > 300 else err_str
        return jsonify({
            "success": False,
            "message": "Download failed. Check the URL and try again.",
            "error": err_clip
        }), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
