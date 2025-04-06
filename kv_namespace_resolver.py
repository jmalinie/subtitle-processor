import os

def get_namespace_id(source_lang, video_id):
    popular_langs = {'en', 'es', 'de', 'fr', 'ru', 'zh'}
    special_langs = {'ja', 'ko', 'ar', 'pt', 'it', 'hi', 'tr', 'nl', 'sv', 'el', 'pl', 'vi', 'th', 'id'}

    first_char = video_id[0].upper()

    if source_lang in popular_langs:
        env_name = f"KV_{source_lang.upper()}_ORIGINAL_{first_char}"
    elif source_lang in special_langs:
        env_name = f"KV_{source_lang.upper()}_ORIGINAL"
    else:
        env_name = "KV_OTHER_LANGS_ORIGINAL"

    namespace_id = os.getenv(env_name)
    if not namespace_id:
        raise Exception(f"Namespace tanımlı değil: {env_name}")
    return namespace_id

