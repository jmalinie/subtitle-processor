import os

def get_kv_namespace_id_for_english_original(video_id):
    first_char_upper = video_id[0].upper()
    first_char_lower = video_id[0].lower()

    namespace_upper = os.getenv(f"KV_EN_ORIGINAL_{first_char_upper}")
    namespace_lower = os.getenv(f"KV_EN_ORIGINAL_{first_char_lower}")

    print(f"🔍 DEBUG UPPER ({first_char_upper}): {namespace_upper}")
    print(f"🔍 DEBUG LOWER ({first_char_lower}): {namespace_lower}")

    if namespace_upper:
        return namespace_upper
    if namespace_lower:
        return namespace_lower

    raise Exception(f"KV namespace tanımlı değil: KV_EN_ORIGINAL_{first_char_upper} veya KV_EN_ORIGINAL_{first_char_lower}")

