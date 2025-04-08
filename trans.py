import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_srt_subtitles(srt_path, source_lang, target_lang):
    with open(srt_path, 'r', encoding='utf-8') as f:
        srt_content = f.read()

    prompt = f"""You will translate the provided subtitles from {source_lang} to {target_lang}.

Instructions:
- Preserve the original numbering and timestamps exactly as provided.
- Translate the subtitle text naturally, fluently, and accurately.
- Do NOT merge or split subtitle blocks.
- Return only the translated subtitles in valid SRT format, without extra comments or formatting."""

    translation_result = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": srt_content}
        ],
        temperature=0.2,
        max_tokens=4096
    )

    translated_srt_content = translation_result.choices[0].message.content.strip()

    translated_srt_path = srt_path.replace(f"_{source_lang}.srt", f"_{source_lang}_{target_lang}.srt")
    with open(translated_srt_path, 'w', encoding='utf-8') as f:
        f.write(translated_srt_content)

    return translated_srt_path
