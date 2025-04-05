import os

def get_kv_namespace_id_for_english_original(video_id):
    first_char = video_id[0].upper()
    env_var_name = f"KV_EN_ORIGINAL_{first_char}"
    
    # Debug için log ekleyelim
    print(f"🛠️ DEBUG: Env var aranıyor: {env_var_name}")
    namespace_id = os.getenv(env_var_name)
    print(f"🛠️ DEBUG: Bulunan namespace_id: {namespace_id}")

    if namespace_id:
        return namespace_id
    else:
        raise KeyError(f"{env_var_name} tanımlı değil veya okunamadı!")
