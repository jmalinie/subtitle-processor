from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from processor import process_subtitles
from translator import translate_subtitles as translate_and_upload
from threading import Thread
import uuid
import os
import requests

app = Flask(__name__)
CORS(app, origins=["https://elosito.com"])

# İşlerin durumunu tutmak için global dict
jobs = {}

# KV Namespace ve Account bilgilerini .env'den al
KV_NAMESPACE_ID = os.getenv("KV_NAMESPACE_ID")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

def kv_get(key):
    """KV'den veri sorgulama fonksiyonu"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/storage/kv/namespaces/{KV_NAMESPACE_ID}/values/{key}"
    headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None

def background_task(job_id, video_id, url, target_lang):
    try:
        # Öncelikle KV'de var mı kontrol et
        kv_key = f"en:{video_id}:{target_lang}"
        if kv_get(kv_key):
            # KV'de varsa indirme ve çeviri yapma
            jobs[job_id] = {
                "status": "completed",
                "video_id": video_id,
                "original_json": f"en/original/{video_id}.json",
                "original_txt": f"en/original/{video_id}.txt",
                "translated_json": f"en/translated/{target_lang}/{video_id}.json",
                "translated_txt": f"en/translated/{target_lang}/{video_id}.txt"
            }
            return

        # KV'de yoksa indir ve çevir
        process_subtitles(url, target_lang)
        translate_and_upload(video_id, "en", target_lang)

        jobs[job_id] = {
            "status": "completed",
            "video_id": video_id,
            "original_json": f"en/original/{video_id}.json",
            "original_txt": f"en/original/{video_id}.txt",
            "translated_json": f"en/translated/{target_lang}/{video_id}.json",
            "translated_txt": f"en/translated/{target_lang}/{video_id}.txt"
        }

    except Exception as e:
        jobs[job_id] = {"status": "error", "message": str(e)}

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

    video_id = url.split("watch?v=")[-1].split("&")[0]
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing"}

    thread = Thread(target=background_task, args=(job_id, video_id, url, target_lang))
    thread.start()

    return jsonify({"status": "ok", "job_id": job_id}), 202

@app.route("/status/<job_id>", methods=["GET"])
def check_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"status": "error", "message": "Geçersiz iş ID."}), 404
    return jsonify(job)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
