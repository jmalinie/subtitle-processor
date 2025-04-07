import os
import json
from openai import OpenAI
from r2_uploader import upload_to_r2
from kv_writer import write_to_kv
from kv_namespace_resolver import get_kv_namespace

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_subtitles(video_id, source_lang, target_lang):
    original_json_path = f"downloads/{video_id}_{source_lang}.json"

    with open(original_json_path, "r", encoding="utf-8") as file:
        original_subtitles = json.load(file)

    subtitle_texts = [entry["text"] for entry in original_subtitles["subtitles"]]

    translation_result = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Translate these subtitles from {source_lang} to {target_lang} preserving their original meaning:"},
            {"role": "user", "content": "\n".join(subtitle_texts)},
        ],
        temperature=0.3,
        max_tokens=4096
    )

    translated_texts = translation_result.choices[0].message.content.strip().split("\n")

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

    first_char = video_id[0].upper()
    json_key = f"{source_lang}/translated/{target_lang}/{first_char}/{video_id}.json"
    txt_key = f"{source_lang}/translated/{target_lang}/{first_char}/{video_id}.txt"

    upload_to_r2(json_path, json_key)
    upload_to_r2(txt_path, txt_key)

    kv_key = f"{source_lang}:{video_id}:{target_lang}"
    kv_value = {"json": json_key, "txt": txt_key}

    namespace_id = get_kv_namespace(source_lang, video_id, is_translated=True)
    write_to_kv(kv_key, kv_value, namespace_id)

    return json_path, txt_path
