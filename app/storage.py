import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from apscheduler.schedulers.background import BackgroundScheduler

# Set AWS credentials
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')

# Initialize S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

class StorageError(Exception):
    pass

def upload_image(image_path, bucket_name):
    s3 = boto3.client('s3')

    try:
        with open(image_path, 'rb') as data:
            s3.upload_fileobj(data, bucket_name, os.path.basename(image_path))
    except (NoCredentialsError, BotoCoreError, ClientError) as e:
        raise StorageError(f"Could not upload image to S3: {str(e)}")

def delete_image(image_name, bucket_name):
    s3 = boto3.client('s3')

    try:
        s3.delete_object(Bucket=bucket_name, Key=image_name)
    except (NoCredentialsError, BotoCoreError, ClientError) as e:
        raise StorageError(f"Could not delete image from S3: {str(e)}")


def cleanup_temp_files():
    folder = '/tmp'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        # If the file is more than an hour old, delete it
        if os.path.getmtime(file_path) < time.time() - 1 * 3600:
            os.remove(file_path)

scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_temp_files, 'interval', hours=1)
scheduler.start()
