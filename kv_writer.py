import requests
import os
import json

CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

def write_to_kv(key, value, namespace_id):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/storage/kv/namespaces/{namespace_id}/values/{key}"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers, data=json.dumps(value))
    
    if response.status_code == 200:
        print(f"✅ KV’ye yazıldı: {key}")
    else:
        raise Exception(f"❌ KV'ye yazılamadı ({response.status_code}): {response.text}")
