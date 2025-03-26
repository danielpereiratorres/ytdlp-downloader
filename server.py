from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__)

# Create a downloads directory if it doesn't exist
DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')  # Get the YouTube URL from the request
    if not url:
        return jsonify({"error": "No URL provided"}), 400  # If no URL is provided, return an error

    try:
        # Define output filename
        output_template = os.path.join(DOWNLOADS_DIR, "%(title)s.%(ext)s")
        
        # Run yt-dlp with headers to mimic a real browser
        result = subprocess.run([
            "yt-dlp",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "--referer", "https://www.youtube.com/",
            "-f", "best",
            "-o", output_template,
            "--no-playlist",  # Ensure only single video is downloaded
            url
        ], capture_output=True, text=True, check=True)

        # Extract filename from yt-dlp output
        output_lines = result.stdout.split("\n")
        downloaded_file = None
        for line in output_lines:
            if "Destination:" in line:
                downloaded_file = line.split("Destination: ")[-1].strip()
                break

        if not downloaded_file:
            return jsonify({"error": "Failed to determine downloaded file"}), 500

        download_url = f"/files/{os.path.basename(downloaded_file)}"
        return jsonify({"message": "Download successful", "download_url": download_url})

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to download video", "details": e.stderr}), 500

@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOADS_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render assigns a dynamic port, so default to 10000
    app.run(host="0.0.0.0", port=port)
