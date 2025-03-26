from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

downloads_dir = "downloads"
os.makedirs(downloads_dir, exist_ok=True)  # Ensure the downloads directory exists

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
        output_path = os.path.join(downloads_dir, "%(title)s.%(ext)s")
        
        # Run yt-dlp with headers to mimic a real browser
        subprocess.run([
            "yt-dlp",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "--referer", "https://www.youtube.com/",
            "-f", "best",
            "-o", output_path,
            url
        ], check=True)

        return jsonify({"message": "Download started successfully"})
    
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to download video", "details": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render assigns a dynamic port, so default to 10000
    app.run(host="0.0.0.0", port=port)
