import os

def get_kv_namespace_id_for_english_original(video_id: str) -> str:
    """
    Belirtilen video_id'nin ilk karakterine göre doğru KV namespace ID'sini döndürür.
    Environment variable şu formatta olmalıdır: KV_EN_ORIGINAL_A, KV_EN_ORIGINAL_B, ..., KV_EN_ORIGINAL_9
    """
    if not video_id:
        raise ValueError("❌ Video ID boş gönderildi.")

    first_char = video_id[0].upper()

    if not first_char.isalnum():
        raise ValueError(f"❌ Video ID'nin ilk karakteri geçersiz: '{first_char}'")

    env_var = f"KV_EN_ORIGINAL_{first_char}"
    namespace_id = os.getenv(env_var)

    if not namespace_id:
        raise KeyError(f"❌ Gerekli environment variable bulunamadı: {env_var}")

    return namespace_id
