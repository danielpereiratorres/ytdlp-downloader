from flask import Flask, request, jsonify
import yt_dlp
import os  # Ensure the import is present

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')  # Get the YouTube URL from the request
    if not url:
        return jsonify({"error": "No URL provided"}), 400  # If no URL is provided, return an error

    try:
        ydl_opts = {
            'format': 'best',  # You can adjust the format as needed
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Adjust output directory
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)  # Just get info without downloading
            video_url = info_dict.get("url")  # Get the direct URL of the video

        return jsonify({"download_url": video_url})  # Return the direct download URL

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500  # Improved error message

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # Use Railway-assigned port, default to 5001 locally
    app.run(host="0.0.0.0", port=port)
