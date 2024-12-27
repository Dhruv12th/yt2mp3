from flask import Flask, request, jsonify, render_template
import yt_dlp
import webbrowser
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    format = request.args.get('format')
    if not url or format != "mp3":
        return jsonify({"error": "Invalid request"}), 400

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }
            ],
            'cookiefile': 'youtube.txt',
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Ensure files are saved as .mp3
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=false)  # Download the file
            file_name = ydl.prepare_filename(info).replace(".webm", ".mp3")  # Ensure MP3 file extension

        return jsonify({"title": info['title'], "file_path": file_name}, webbrowser.open_new_tab(info['url']))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
