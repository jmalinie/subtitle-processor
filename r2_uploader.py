import boto3
from config import R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT, R2_BUCKET_NAME
import os

def upload_to_r2(file_path, r2_key):
    if not os.path.exists(file_path):
        print(f"❌ Dosya bulunamadı: {file_path}")
        return None

    try:
        session = boto3.session.Session()
        s3 = session.client(
    service_name='s3',
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    endpoint_url=R2_ENDPOINT,
    verify=False  # <<< BURAYA EKLE
)

        with open(file_path, 'rb') as f:
            s3.upload_fileobj(f, R2_BUCKET_NAME, r2_key)

        print(f"✅ R2’ye yüklendi: {file_path} → {r2_key}")
        return f"{R2_ENDPOINT}/{R2_BUCKET_NAME}/{r2_key}"

    except Exception as e:
        print(f"❌ R2 yükleme hatası: {e}")
        return None
