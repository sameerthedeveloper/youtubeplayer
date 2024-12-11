from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_audio', methods=['POST'])
def fetch_audio():
    data = request.get_json()
    video_url = data.get('url')

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            audio_url = info_dict['url']
            title = info_dict.get('title', 'Unknown Title')
            author = info_dict.get('uploader', 'Unknown Author')
            thumbnail = info_dict.get('thumbnail', '')

        return jsonify({
            "title": title,
            "author": author,
            "thumbnail": thumbnail,
            "stream_url": audio_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=1988)