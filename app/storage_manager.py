from abc import ABC, abstractmethod
import boto3
import os

class StorageManager(ABC):
    @abstractmethod
    def upload(self, file_path: str) -> str:
        pass

class S3StorageManager(StorageManager):
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = os.getenv('S3_BUCKET_NAME')

    def upload(self, file_path: str) -> str:
        file_name = os.path.basename(file_path)
        self.s3_client.upload_file(file_path, self.bucket_name, file_name)
        return f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
