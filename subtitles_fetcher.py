import requests
import json
import os

RAILWAY_API_BASE = "https://youtube-subtitle-api-production.up.railway.app"
DOWNLOAD_FOLDER = "downloads"  # İndirilen altyazıların kaydedileceği klasör

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def fetch_subtitles(video_id):
    url = f"{RAILWAY_API_BASE}/subtitles?video_id={video_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        lang_code = data.get("language_code", "und")
        json_filename = f"{video_id}_{lang_code}.json"
        txt_filename = f"{video_id}_{lang_code}.txt"
        json_path = os.path.join(DOWNLOAD_FOLDER, json_filename)
        txt_path = os.path.join(DOWNLOAD_FOLDER, txt_filename)

        # JSON dosyası
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(data, jf, ensure_ascii=False, indent=2)

        # TXT dosyası (timestamp eşleşmeli)
        with open(txt_path, "w", encoding="utf-8") as tf:
            for i, s in enumerate(data.get("subtitles", {}).get("snippets", []), 1):
                start = s.get("start", 0)
                end = start + s.get("duration", 0)
                text = s.get("text", "")
                tf.write(f"{i}\n{start:.3f} --> {end:.3f}\n{text}\n\n")

        print(f"✔ JSON ve TXT dosyaları kaydedildi: {json_path}, {txt_path}")
        return json_path, txt_path

    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        return None, None

# Test amaçlı doğrudan çalıştırma
if __name__ == "__main__":
    video_id = "dQw4w9WgXcQ"
    fetch_subtitles(video_id)
