# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from processor import process_subtitles
from translator import translate_subtitles as translate_and_upload

app = Flask(__name__)
CORS(app, resources={r"/process": {"origins": "*"}})  # Gerekirse sadece "https://elosito.com" yaz

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/process", methods=["POST", "OPTIONS"])
@cross_origin(origins="*")  # Gerekirse sadece "https://elosito.com"
def process():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight'})
        response.headers.add("Access-Control-Allow-Origin", "*")  # Gerekirse "https://elosito.com"
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    data = request.get_json()
    url = data.get("url")
    target_lang = data.get("target_lang")

    if not url or not target_lang:
        return jsonify({"status": "error", "message": "Eksik veri gönderildi."}), 400

    try:
        video_id = process_subtitles(url, target_lang)
        translate_and_upload(video_id, "en", target_lang)

        return jsonify({
            "status": "ok",
            "video_id": video_id,
            "original_json": f"en/original/{video_id}.json",
            "translated_json": f"en/translated/{target_lang}/{video_id}.json"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
