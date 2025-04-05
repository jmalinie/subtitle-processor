from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from processor import process_subtitles
from translator import translate_subtitles as translate_and_upload
from kv_namespace_resolver import get_kv_namespace_id_for_english_original
from threading import Thread
import uuid
import os
import requests

app = Flask(__name__)
CORS(app, origins=["https://elosito.com"])

jobs = {}

# KV bilgilerini .env'den al
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

def kv_get(key, namespace_id):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/storage/kv/namespaces/{namespace_id}/values/{key}"
    headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None

def background_task(job_id, video_id, url, target_lang):
    try:
        namespace_id = get_kv_namespace_id_for_english_original(video_id)
        if not namespace_id:
            jobs[job_id] = {"status": "error", "message": "KV namespace bulunamadı!"}
            return

        kv_key = f"en:{video_id}:{target_lang}"

        if kv_get(kv_key, namespace_id):
            jobs[job_id] = {
                "status": "completed",
                "video_id": video_id,
                "original_json": f"en/original/{video_id}.json",
                "original_txt": f"en/original/{video_id}.txt",
                "translated_json": f"en/translated/{target_lang}/{video_id}.json",
                "translated_txt": f"en/translated/{target_lang}/{video_id}.txt"
            }
            return

        process_subtitles(url, target_lang)
        
        # Çeviri işlemini yap ve hata kontrolü ekle
        translate_and_upload(video_id, "en", target_lang)

        translated_json_path = f"en/translated/{target_lang}/{video_id}.json"
        translated_txt_path = f"en/translated/{target_lang}/{video_id}.txt"

        # Dosyalar gerçekten R2'ye yüklendi mi kontrol edelim (opsiyonel ama önerilir!)
        jobs[job_id] = {
            "status": "completed",
            "video_id": video_id,
            "original_json": f"en/original/{video_id}.json",
            "original_txt": f"en/original/{video_id}.txt",
            "translated_json": translated_json_path,
            "translated_txt": translated_txt_path
        }

    except Exception as e:
        jobs[job_id] = {"status": "error", "message": f"Backend hata: {str(e)}"}

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
