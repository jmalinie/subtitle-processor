import os

def get_kv_namespace(subtitle_lang, video_id, is_translated=False):
    lang_upper = subtitle_lang.upper()
    first_char = video_id[0].upper()

    special_langs = ["EN", "ES", "DE", "FR", "RU", "ZH"]
    secondary_langs = ["JA", "KO", "AR", "PT", "IT", "HI", "TR", "NL", "SV", "EL", "PL", "VI", "TH", "ID"]

    if lang_upper in special_langs:
        namespace_id = os.getenv(f"KV_{lang_upper}_{'TRANSLATED' if is_translated else 'ORIGINAL'}_{first_char}",
                                 os.getenv(f"KV_{lang_upper}_{'TRANSLATED' if is_translated else 'ORIGINAL'}_DEFAULT"))
    elif lang_upper in secondary_langs:
        namespace_id = os.getenv(f"KV_{lang_upper}_{'TRANSLATED' if is_translated else 'ORIGINAL'}")
    else:
        namespace_id = os.getenv(f"KV_OTHER_LANGUAGES_{'TRANSLATED' if is_translated else 'ORIGINAL'}")

    if not namespace_id:
        raise Exception(f"KV namespace tanımlı değil: Dil: {subtitle_lang}, Harf: {first_char}")

    return namespace_id
