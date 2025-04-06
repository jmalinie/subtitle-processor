from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from processor import process_subtitles
from translator import translate_subtitles
from threading import Thread
import uuid

app = Flask(__name__)
CORS(app, origins=["https://elosito.com"])

jobs = {}

def background_task(job_id, video_id, url, source_lang, target_lang):
    try:
        process_subtitles(url, source_lang)
        translate_subtitles(video_id, source_lang, target_lang)
        jobs[job_id] = {"status": "completed"}
    except Exception as e:
        jobs[job_id] = {"status": "error", "message": str(e)}

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    url = data.get("url")
    source_lang = data.get("source_lang", "en")
    target_lang = data.get("target_lang")

    if not url or not target_lang:
        return jsonify({"status": "error", "message": "Eksik veri gönderildi."}), 400

    video_id = url.split("watch?v=")[-1].split("&")[0]
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing"}

    Thread(target=background_task, args=(job_id, video_id, url, source_lang, target_lang)).start()

    return jsonify({"status": "ok", "job_id": job_id}), 202

@app.route("/status/<job_id>", methods=["GET"])
def check_status(job_id):
    return jsonify(jobs.get(job_id, {"status": "error", "message": "Geçersiz iş ID."}))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
