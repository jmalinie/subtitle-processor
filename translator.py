import json
import os
from openai import OpenAI
from config import OPENAI_API_KEY
from r2_uploader import upload_to_r2
from kv_writer import write_to_kv

client = OpenAI(api_key=OPENAI_API_KEY)

def translate_text(text, source_lang, target_lang):
    prompt = f"Translate the following subtitle from {source_lang} to {target_lang}:\n\n{text}\n\nJust translate, no extra comments."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def translate_subtitles(video_id, source_lang, target_lang, namespace_id):
    original_json_path = f"downloads/{video_id}_{source_lang}.json"
    if not os.path.exists(original_json_path):
        raise Exception(f"JSON dosyası bulunamadı: {original_json_path}")

    with open(original_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    snippets = data.get("subtitles", {}).get("snippets", [])
    if not snippets:
        raise Exception("Altyazılar alınamadı")

    translated_snippets = []
    for snippet in snippets:
        translated_text = translate_text(snippet["text"], source_lang, target_lang)
        translated_snippets.append({
            "start": snippet["start"],
            "duration": snippet["duration"],
            "text": translated_text
        })

    translated_data = {
        "language": target_lang,
        "language_code": target_lang,
        "translated_from": source_lang,
        "video_id": video_id,
        "snippets": translated_snippets
    }

    # Dosya isimleri
    json_filename = f"{video_id}_{source_lang}_{target_lang}.json"
    txt_filename = f"{video_id}_{source_lang}_{target_lang}.txt"
    json_path = os.path.join("downloads", json_filename)
    txt_path = os.path.join("downloads", txt_filename)

    # JSON dosyasını kaydet
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(translated_data, jf, ensure_ascii=False, indent=2)

    # TXT dosyasını kaydet
    with open(txt_path, "w", encoding="utf-8") as tf:
        for snippet in translated_snippets:
            tf.write(snippet["text"] + "\n")

    print(f"✅ Çeviri dosyaları oluşturuldu: {json_path}, {txt_path}")

    # R2 yükleme
    json_key = f"{source_lang}/translated/{target_lang}/{video_id}.json"
    txt_key = f"{source_lang}/translated/{target_lang}/{video_id}.txt"
    upload_to_r2(json_path, json_key)
    upload_to_r2(txt_path, txt_key)

    # KV'ye yaz
    kv_key = f"{source_lang}:{video_id}:{target_lang}"
    kv_value = {
        "json": json_key,
        "txt": txt_key
    }
    write_to_kv(kv_key, kv_value, namespace_id=namespace_id)

    print("🎉 Çeviri işlemi tamamlandı ve KV'ye yazıldı!")
