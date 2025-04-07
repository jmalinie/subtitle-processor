import json 
from youtube_transcript_api import YouTubeTranscriptApi

def fetch_subtitles(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['en', 'es', 'de', 'fr', 'ru', 'zh', 'ja', 'ko', 'ar', 'pt', 'it', 'hi', 'tr', 'nl', 'sv', 'el', 'pl', 'vi', 'th', 'id'])

    subtitle_lang = transcript.language_code
    subtitle_data = transcript.fetch()  # Burası zaten dict tipinde subtitle verisi döner.

    response_json = {
        "language_code": subtitle_lang,
        "subtitles": subtitle_data  # subtitle_data zaten JSON serializable'dır
    }

    json_path = f"downloads/{video_id}_{subtitle_lang}.json"
    txt_path = f"downloads/{video_id}_{subtitle_lang}.txt"

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(response_json, f, ensure_ascii=False)

    with open(txt_path, 'w', encoding='utf-8') as f:
        for entry in subtitle_data:
            f.write(entry["text"] + '\n')

    return json_path, txt_path, subtitle_lang
