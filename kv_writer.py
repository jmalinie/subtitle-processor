import requests
import os
import json

def write_to_kv(key, value, namespace_id):
    headers = {
        "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_TOKEN')}",
        "Content-Type": "application/json"
    }
    url = f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('CLOUDFLARE_ACCOUNT_ID')}/storage/kv/namespaces/{namespace_id}/values/{key}"
    response = requests.put(url, headers=headers, data=json.dumps(value))
    if response.status_code != 200:
        raise Exception(f"KV'ye yazma başarısız oldu: {response.text}")
    print(f"✅ KV'ye yazıldı: {key}")

def check_kv_exists(key, namespace_id):
    headers = {
        "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_TOKEN')}"
    }
    url = f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('CLOUDFLARE_ACCOUNT_ID')}/storage/kv/namespaces/{namespace_id}/values/{key}"
    response = requests.get(url, headers=headers)
    return response.status_code == 200
