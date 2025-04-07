import os
import re
from subtitles_fetcher import fetch_subtitles
from r2_uploader import upload_to_r2
from kv_writer import write_to_kv

def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", url)
    if not match:
        raise ValueError("Geçersiz YouTube URL'si")
    return match.group(1)

def process_subtitles(youtube_url: str):
    video_id = extract_video_id(youtube_url)

    json_path, txt_path, subtitle_lang = fetch_subtitles(video_id)

    if not json_path or not txt_path:
        raise Exception("Altyazılar alınamadı")

    first_char = video_id[0].upper()
    json_key = f"{subtitle_lang}/original/{first_char}/{video_id}.json"
    txt_key = f"{subtitle_lang}/original/{first_char}/{video_id}.txt"

    upload_to_r2(json_path, json_key)
    upload_to_r2(txt_path, txt_key)

    kv_key = f"{subtitle_lang}:{video_id}:original"
    kv_value = {
        "json": json_key,
        "txt": txt_key
    }

    write_to_kv(kv_key, kv_value)

    return video_id, subtitle_lang
