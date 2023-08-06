import boto3
import os
from botocore.exceptions import BotoCoreError, NoCredentialsError

class StorageManager:
    def __init__(self):
        self.s3 = boto3.client('s3', 
                               endpoint_url=os.getenv('BACKBLAZE_URL'), 
                               aws_access_key_id=os.getenv('BACKBLAZE_ID'), 
                               aws_secret_access_key=os.getenv('BACKBLAZE_KEY'))
        self.bucket_name = os.getenv('BACKBLAZE_BUCKET')

    def upload(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                response = self.s3.upload_fileobj(file, self.bucket_name, file_path)
                return response
        except (BotoCoreError, NoCredentialsError) as e:
            print('An error occurred during file upload:', e)
            return None

    def delete(self, file_name):
        try:
            response = self.s3.delete_object(Bucket=self.bucket_name, Key=file_name)
            return response
        except (BotoCoreError, NoCredentialsError) as e:
            print('An error occurred during file deletion:', e)
            return None
