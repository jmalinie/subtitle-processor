import os
import re
from subtitles_fetcher import fetch_subtitles
from r2_uploader import upload_to_r2
from kv_writer import write_to_kv
from kv_namespace_resolver import get_kv_namespace_id_for_english_original

def extract_video_id(url: str) -> str:
    # YouTube video ID'sini URL'den çıkarır
    match = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", url)
    if not match:
        raise ValueError("Geçersiz YouTube URL'si")
    return match.group(1)

def process_subtitles(youtube_url: str, target_lang: str) -> str:
    video_id = extract_video_id(youtube_url)
    json_path, txt_path = fetch_subtitles(video_id)

    if not json_path or not txt_path:
        raise Exception("Altyazılar alınamadı")

    # R2 anahtarları
    json_key = f"en/original/{video_id}.json"
    txt_key = f"en/original/{video_id}.txt"

    # R2'ye yükleme
    upload_to_r2(json_path, json_key)
    upload_to_r2(txt_path, txt_key)

    # KV'ye yol kaydı
    kv_key = f"en:{video_id}:original"
    kv_value = {
        "json": json_key,
        "txt": txt_key
    }

    # namespace_id eksikti, buraya eklendi
    namespace_id = get_kv_namespace_id_for_english_original(video_id)
    write_to_kv(kv_key, kv_value, namespace_id=namespace_id)

    return video_id
