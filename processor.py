import os

def get_kv_namespace_id_for_english_original(video_id):
    first_char = video_id[0].upper()

    # Harf ve rakam kontrolü (A-Z ve 0-9)
    if not first_char.isalnum():
        first_char = "DEFAULT"

    env_var_name = f"KV_EN_ORIGINAL_{first_char}"
    namespace_id = os.getenv(env_var_name)
    
    if namespace_id:
        return namespace_id

    # Eğer bulunamadıysa varsayılan namespace'e yönlendir
    namespace_id_default = os.getenv("KV_EN_ORIGINAL_DEFAULT")
    if namespace_id_default:
        return namespace_id_default

    raise Exception(f"KV namespace tanımlı değil: {env_var_name} ve varsayılan namespace bulunamadı!")
