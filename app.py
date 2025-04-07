from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from processor import process_subtitles
from translator import translate_subtitles
from threading import Thread
import uuid
import os

app = Flask(__name__)
CORS(app, origins=["https://elosito.com"])

jobs = {}

def background_task(job_id, url, target_lang):
    try:
        # Önce altyazılar işlenir ve dil bilgisi alınır
        video_id, subtitle_lang = process_subtitles(url)

        # Altyazı dil bilgisiyle çeviri yapılır
        translate_subtitles(video_id, subtitle_lang, target_lang)

        # Başarıyla tamamlandı
        jobs[job_id] = {
            "status": "completed",
            "video_id": video_id,
            "subtitle_lang": subtitle_lang
        }

    except Exception as e:
        # Hata varsa hata mesajını yaz
        jobs[job_id] = {
            "status": "error",
            "message": str(e)
        }

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    url = data.get("url")
    target_lang = data.get("target_lang")

    if not url or not target_lang:
        return jsonify({"status": "error", "message": "Eksik veri gönderildi."}), 400

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing"}

    # Arka plan işini başlat
    Thread(target=background_task, args=(job_id, url, target_lang)).start()

    return jsonify({"status": "ok", "job_id": job_id}), 202

@app.route("/status/<job_id>", methods=["GET"])
def check_status(job_id):
    return jsonify(jobs.get(job_id, {
        "status": "error",
        "message": "Geçersiz iş ID."
    }))

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    app.run(host="0.0.0.0", port=8080)
