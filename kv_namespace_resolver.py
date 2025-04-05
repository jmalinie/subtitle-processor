import os

def get_kv_namespace_id_for_english_original(video_id):
    first_char = video_id[0].upper()

    # Eğer ilk karakter alfanumerik değilse "DEFAULT" kullan.
    if not first_char.isalnum():
        first_char = "DEFAULT"

    env_var_name_upper = f"KV_EN_ORIGINAL_{first_char.upper()}"
    env_var_name_lower = f"KV_EN_ORIGINAL_{first_char.lower()}"

    namespace_id = os.getenv(env_var_name_upper) or os.getenv(env_var_name_lower)

    if namespace_id:
        return namespace_id
    else:
        raise Exception(f"KV namespace tanımlı değil: {env_var_name_upper} veya {env_var_name_lower}")
