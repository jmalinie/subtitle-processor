from youtube_transcript_api import YouTubeTranscriptApi

def fetch_subtitles(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    subtitles_fetched = []

    for transcript in transcript_list:
        subtitle_lang = transcript.language_code
        subtitle_data = transcript.fetch()

        txt_path = f"downloads/{video_id}_{subtitle_lang}.txt"
        srt_path = f"downloads/{video_id}_{subtitle_lang}.srt"

        # TXT olarak kaydet
        with open(txt_path, 'w', encoding='utf-8') as f:
            for entry in subtitle_data:
                f.write(entry.text + '\n')

        # SRT olarak kaydet
        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write(to_srt(subtitle_data))

        subtitles_fetched.append((txt_path, srt_path, subtitle_lang))

    return subtitles_fetched

# SRT formatına dönüştürme fonksiyonu
def to_srt(subtitle_entries):
    srt_output = []
    for i, entry in enumerate(subtitle_entries, start=1):
        start_time = format_srt_timestamp(entry['start'])
        end_time = format_srt_timestamp(entry['start'] + entry['duration'])
        text = entry['text']
        srt_output.append(f"{i}\n{start_time} --> {end_time}\n{text}\n")
    return "\n".join(srt_output)

# Zaman damgalarını SRT formatına çeviren yardımcı fonksiyon
def format_srt_timestamp(seconds):
    millisec = int(seconds % 1 * 1000)
    s, m = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02},{millisec:03}"
