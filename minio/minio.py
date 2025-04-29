import boto3
import uuid
import os
from botocore.exceptions import ClientError

# Настройки
bucket_name = os.getenv("MLFLOW_BUCKET_NAME")
region_name = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
endpoint_url = os.getenv("AWS_ENDPOINT_URL", "http://127.0.0.1:8456")
test_key = f"mlflow-test-{uuid.uuid4()}.txt"
test_content = "Test file for checking S3 permissions."

# Создание клиента
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=region_name,
    endpoint_url=endpoint_url
)

print(f"Проверяем доступ к бакету: {bucket_name}")

# 1. Проверяем ListBucket
try:
    s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
    print(" Успешно: ListBucket разрешён (чтение содержимого бакета)")
except ClientError as e:
    print(f" Ошибка ListBucket: {e}")

# 2. Проверяем PutObject (запись файла)
try:
    s3.put_object(Bucket=bucket_name, Key=test_key, Body=test_content.encode())
    print(f" Успешно: PutObject разрешён (запись файла {test_key})")
except ClientError as e:
    print(f" Ошибка PutObject: {e}")

# 3. Проверяем DeleteObject (удаление файла)
try:
    s3.delete_object(Bucket=bucket_name, Key=test_key)
    print(f" Успешно: DeleteObject разрешён (удаление тестового файла)")
except ClientError as e:
    print(f" Ошибка DeleteObject: {e}")
