import requests

res = requests.post("http://127.0.0.1:5000/process", json={
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "target_lang": "tr"
})
print(res.status_code)
print(res.json())
