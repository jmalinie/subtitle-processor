import os

def get_kv_namespace_for_video(video_id):
    """
    İngilizce altyazı dosyaları için video ID'nin ilk karakterine göre doğru KV Namespace ID'sini getirir.
    """
    if not video_id:
        raise ValueError("Boş video ID gönderildi!")

    first_char = video_id[0].lower()

    if first_char.isalnum():
        env_var_name = f"KV_EN_ORIGINAL_{first_char.upper()}"
        namespace_id = os.getenv(env_var_name)

        if namespace_id:
            return namespace_id
        else:
            raise KeyError(f"Environment variable {env_var_name} tanımlı değil!")
    else:
        raise ValueError(f"Geçersiz karakter: {first_char}")
