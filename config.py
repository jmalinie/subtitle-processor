from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

# Alt yazı API URL’i
SUBTITLE_API_URL = os.getenv("SUBTITLE_API_URL")

# Cloudflare R2 Ayarları
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_ENDPOINT = os.getenv("R2_ENDPOINT")

# KV Namespace
KV_NAMESPACE_ID = os.getenv("KV_NAMESPACE_ID")

# OpenAI Ayarı
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Gerekirse çıktılar için varsayılan dizin (opsiyonel)
LOCAL_OUTPUT_DIR = "outputs"

DEFAULT_ORIGINAL_LANG = "en"
