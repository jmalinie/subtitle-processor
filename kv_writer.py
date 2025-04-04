import requests
import json
import os
from kv_namespace_resolver import get_kv_namespace_id_for_english_original

# KV için Cloudflare API
CLOUDFLARE_API_BASE = "https://api.cloudflare.com/client/v4/accounts"
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

def write_to_kv(video_id, value_dict):
    try:
        namespace_id = get_kv_namespace_id_for_english_original(video_id)
    except Exception as e:
        print(f"❌ KV namespace belirlenemedi: {e}")
        return

    kv_key = video_id.lower()  # normalize ediyoruz
    url = f"{CLOUDFLARE_API_BASE}/{CLOUDFLARE_ACCOUNT_ID}/storage/kv/namespaces/{namespace_id}/values/{kv_key}"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.put(url, headers=headers, data=json.dumps(value_dict))
        if response.ok:
            print(f"✅ KV’ye yazıldı: {kv_key}")
        else:
            print(f"❌ KV hatası ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ KV bağlantı hatası: {e}")
