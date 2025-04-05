import os

def get_kv_namespace_for_video(video_id: str) -> str:
    """
    Video ID'nin ilk karakterine göre doğru KV namespace ID'sini döner.
    Örn: M ile başlayan video için KV_EN_ORIGINAL_M değişkenine bakar.
    """
    if not video_id:
        raise ValueError("Boş video ID gönderildi!")

    first_char = video_id[0].lower()
    if not first_char.isalnum():
        raise ValueError(f"Geçersiz karakter: {first_char}")

    env_var = f"KV_EN_ORIGINAL_{first_char.upper()}"
    namespace_id = os.getenv(env_var)

    if not namespace_id:
        raise KeyError(f"Hata: {env_var} environment variable'ı tanımlı değil!")

    return namespace_id


def get_kv_namespace_id_for_english_original(video_id: str) -> str:
    """
    Bu fonksiyon backward compatibility için bırakılmıştır.
    Eski sistemde bu isimle çağrılıyordu.
    """
    return get_kv_namespace_for_video(video_id)
