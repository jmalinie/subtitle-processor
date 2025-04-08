import os

def get_kv_namespace(subtitle_lang, video_id, is_translated=False, target_lang=None):
    lang_upper = subtitle_lang.upper()
    first_char = video_id[0].upper()

    special_langs = ["EN", "ES", "DE", "FR", "RU", "ZH"]
    secondary_langs = ["JA", "KO", "AR", "PT", "IT", "HI", "TR", "NL", "SV", "EL", "PL", "VI", "TH", "ID"]

    if is_translated and target_lang:
        return os.getenv(f"KV_{lang_upper}_TRANSLATED_{target_lang.upper()}",
                         os.getenv("KV_DEFAULT_TRANSLATED"))

    if lang_upper in special_langs:
        namespace_id = os.getenv(f"KV_{lang_upper}_ORIGINAL_{first_char}", os.getenv(f"KV_{lang_upper}_ORIGINAL_DEFAULT"))
    elif lang_upper in secondary_langs:
        namespace_id = os.getenv(f"KV_{lang_upper}_ORIGINAL")
    else:
        namespace_id = os.getenv("KV_OTHER_LANGUAGES_ORIGINAL")

    if not namespace_id:
        raise Exception(f"KV namespace tanımlı değil: Dil: {subtitle_lang}, Harf: {first_char}")

    return namespace_id

