import os
import re
from subtitles_fetcher import fetch_subtitles
from r2_uploader import upload_to_r2
from kv_writer import write_to_kv, check_kv_exists

def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", url)
    if not match:
        raise ValueError("Geçersiz YouTube URL'si")
    return match.group(1)

def get_kv_namespace(subtitle_lang, video_id):
    lang_upper = subtitle_lang.upper()
    first_char = video_id[0].upper()

    # özel dillere göre KV namespace düzenlemesi
    special_langs = ["EN", "ES", "DE", "FR", "RU", "ZH"]
    secondary_langs = ["JA", "KO", "AR", "PT", "IT", "HI", "TR", "NL", "SV", "EL", "PL", "VI", "TH", "ID"]

    if lang_upper in special_langs:
        namespace_id = os.getenv(f"KV_{lang_upper}_ORIGINAL_{first_char}", os.getenv(f"KV_{lang_upper}_ORIGINAL_DEFAULT"))
    elif lang_upper in secondary_langs:
        namespace_id = os.getenv(f"KV_{lang_upper}_ORIGINAL")
    else:
        namespace_id = os.getenv("KV_OTHER_LANGUAGES_ORIGINAL")

    if not namespace_id:
        raise Exception(f"KV namespace tanımlı değil: Dil: {subtitle_lang}, Harf: {first_char}")

    return namespace_id

def process_subtitles(youtube_url: str, target_lang: str) -> tuple:
    video_id = extract_video_id(youtube_url)
    first_char = video_id[0].upper()

    # Altyazı mevcut mu kontrolü (KV):
    subtitle_lang = 'en'  # varsayılan ilk dil genellikle İngilizce olur
    namespace_id = get_kv_namespace(subtitle_lang, video_id)
    kv_key = f"{subtitle_lang}:{video_id}:original"

    if check_kv_exists(kv_key, namespace_id):
        print("✅ KV üzerinde zaten mevcut, tekrar yükleme yapılmıyor.")
        return video_id, subtitle_lang

    # KV'de yoksa altyazıyı getir ve işle
    json_path, txt_path, subtitle_lang = fetch_subtitles(video_id)

    if not json_path or not txt_path:
        raise Exception("Altyazılar alınamadı")

    json_key = f"{subtitle_lang}/original/{first_char}/{video_id}.json"
    txt_key = f"{subtitle_lang}/original/{first_char}/{video_id}.txt"

    upload_to_r2(json_path, json_key)
    upload_to_r2(txt_path, txt_key)

    kv_value = {"json": json_key, "txt": txt_key}
    write_to_kv(kv_key, kv_value, namespace_id)

    return video_id, subtitle_lang
