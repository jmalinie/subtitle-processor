import os
import json
from openai import OpenAI
from r2_uploader import upload_to_r2
from kv_writer import write_to_kv, check_kv_exists, read_from_kv
from kv_namespace_resolver import get_kv_namespace

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_subtitles(video_id, source_lang, target_lang):
    first_char = video_id[0].upper()

    kv_key = f"{source_lang}:{video_id}:{target_lang}"
    namespace_id = get_kv_namespace(source_lang, video_id, is_translated=True)

    if check_kv_exists(kv_key, namespace_id):
        kv_data = read_from_kv(kv_key, namespace_id)
        print("✅ Çeviri KV üzerinde mevcut, tekrar çeviri yapılmıyor.")
        return kv_data["json"], kv_data["txt"]

    original_json_path = f"downloads/{video_id}_{source_lang}.json"
    with open(original_json_path, "r", encoding="utf-8") as file:
        original_subtitles = json.load(file)

    subtitle_texts = [entry["text"] for entry in original_subtitles["subtitles"]]

    translation_result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Translate from {source_lang} to {target_lang}, strictly do not add any extra comment. Just pure translate."},
            {"role": "user", "content": "\n".join(subtitle_texts)},
        ],
        temperature=0.3,
        max_tokens=4096
    )

    translated_texts = translation_result.choices[0].message.content.strip().split("\n")

    # Satır sayısı eşleşmezse hata önleme
    if len(translated_texts) != len(subtitle_texts):
        raise ValueError(f"Satır sayıları eşleşmiyor! Orijinal: {len(subtitle_texts)}, Çeviri: {len(translated_texts)}")

    translated_subtitles = {
        "language_code": target_lang,
        "subtitles": [
            {
                "text": translated_texts[i],
                "start": entry["start"],
                "duration": entry["duration"]
            }
            for i, entry in enumerate(original_subtitles["subtitles"])
        ]
    }

    json_path = f"downloads/{video_id}_{source_lang}_{target_lang}.json"
    txt_path = f"downloads/{video_id}_{source_lang}_{target_lang}.txt"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(translated_subtitles, file, ensure_ascii=False)

    with open(txt_path, "w", encoding="utf-8") as file:
        file.write("\n".join(translated_texts))

    json_key = f"{source_lang}/translated/{target_lang}/{first_char}/{video_id}.json"
    txt_key = f"{source_lang}/translated/{target_lang}/{first_char}/{video_id}.txt"

    upload_to_r2(json_path, json_key)
    upload_to_r2(txt_path, txt_key)

    kv_value = {"json": json_key, "txt": txt_key}
    write_to_kv(kv_key, kv_value, namespace_id)

    print("✅ Çeviri yapıldı ve KV'ye yazıldı.")

    return json_key, txt_key
