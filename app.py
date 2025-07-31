from flask import Flask, jsonify, request
import yt_dlp

app = Flask(__name__)

def get_video_details(video_url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            formats = info_dict.get('formats', [])

            video_details = {
                "title": info_dict.get('title', ''),
                "description": info_dict.get('description', ''),
                "channel_name": info_dict.get('uploader', ''),
                "download_links": {
                    "audio": next((f['url'] for f in formats if f['ext'] == 'm4a'), None),
                    "video": {
                        f['format_note']: f['url']
                        for f in formats if f['ext'] == 'mp4' and f.get('format_note')
                    }
                }
            }
            return video_details
    except Exception as e:
        return {"error": str(e)}

@app.route('/api/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL parameter is missing"}), 400

    video_details = get_video_details(video_url)
    return jsonify(video_details)

if __name__ == '__main__':
    app.run(debug=True)
