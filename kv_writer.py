# kv_writer.py
import os
import json
import requests

# Çevre değişkenlerinden alınan varsayılan namespace
DEFAULT_NAMESPACE_ID = os.getenv("KV_NAMESPACE_ID")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

def write_to_kv(key, value, namespace_id=None):
    if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_API_TOKEN:
        raise ValueError("Cloudflare API kimlik bilgileri eksik!")

    if not namespace_id:
        if not DEFAULT_NAMESPACE_ID:
            raise ValueError("Varsayılan KV namespace tanımlı değil!")
        namespace_id = DEFAULT_NAMESPACE_ID

    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/storage/kv/namespaces/{namespace_id}/values/{key}"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.put(url, headers=headers, data=json.dumps(value))

    if response.status_code == 200:
        print(f"✅ KV’ye yazıldı: {key} → {namespace_id}")
    else:
        print(f"❌ KV hatası: {response.status_code}", response.text)
