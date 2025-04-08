import os
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
        return kv_data["srt"], kv_data["txt"]

    original_srt_path = f"downloads/{video_id}_{source_lang}.srt"
    with open(original_srt_path, "r", encoding="utf-8") as file:
        original_srt_content = file.read()

    prompt = f"""Translate the provided subtitles from {source_lang} to {target_lang}.

Instructions:
- Keep the exact same subtitle block numbers and timestamps. Do NOT modify or merge timestamps.
- Translate each subtitle block separately, line by line. Do NOT merge or split subtitle blocks under any circumstances.
- Provide only the translated subtitles in valid SRT format, preserving the original number of blocks exactly.
- Do not add extra comments, notes, or formatting."""


    translation_result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": original_srt_content},
        ],
        temperature=0.2,
        
    )

    translated_srt_content = translation_result.choices[0].message.content.strip()

    srt_path = f"downloads/{video_id}_{source_lang}_{target_lang}.srt"
    txt_path = f"downloads/{video_id}_{source_lang}_{target_lang}.txt"

    with open(srt_path, "w", encoding="utf-8") as file:
        file.write(translated_srt_content)

    with open(txt_path, "w", encoding="utf-8") as file:
        subtitle_lines = [block.split('\n', 2)[2] for block in translated_srt_content.strip().split('\n\n') if len(block.split('\n', 2)) == 3]
        file.write("\n".join(subtitle_lines))

    srt_key = f"{source_lang}/translated/{target_lang}/{first_char}/{video_id}.srt"
    txt_key = f"{source_lang}/translated/{target_lang}/{first_char}/{video_id}.txt"

    upload_to_r2(srt_path, srt_key)
    upload_to_r2(txt_path, txt_key)

    kv_value = {"srt": srt_key, "txt": txt_key}
    write_to_kv(kv_key, kv_value, namespace_id)

    print("✅ Çeviri yapıldı ve KV'ye yazıldı.")

    return srt_key, txt_key
