import json
from youtube_transcript_api import YouTubeTranscriptApi

def fetch_subtitles(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    subtitles_fetched = []

    # Mevcut tüm altyazıları al
    for transcript in transcript_list:
        subtitle_lang = transcript.language_code

        subtitle_data = transcript.fetch()

        response_json = {
            "language_code": subtitle_lang,
            "subtitles": [
                {"text": entry["text"], "start": entry["start"], "duration": entry["duration"]}
                for entry in subtitle_data
            ]
        }

        json_path = f"downloads/{video_id}_{subtitle_lang}.json"
        txt_path = f"downloads/{video_id}_{subtitle_lang}.txt"

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(response_json, f, ensure_ascii=False, indent=4)

        with open(txt_path, 'w', encoding='utf-8') as f:
            for entry in subtitle_data:
                f.write(entry["text"] + '\n')

        subtitles_fetched.append((json_path, txt_path, subtitle_lang))

    return subtitles_fetched

