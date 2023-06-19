import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from apscheduler.schedulers.background import BackgroundScheduler

# Set AWS credentials
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Initialize S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

class StorageError(Exception):
    pass

class B2Storage:
    def __init__(self):
        application_key_id = os.getenv("B2_KEY_ID")
        application_key = os.getenv("B2_APPLICATION_KEY")
        self.bucket_name = os.getenv("B2_BUCKET_NAME")

        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        app_key_cred = B2ApplicationKeyCredentials(application_key_id, application_key)
        b2_api.authorize_account('production', app_key_cred)
        self.bucket = b2_api.get_bucket_by_name(self.bucket_name)

    def upload_image(self, file_path, file_name):
        try:
            file_info = {'how': 'good-file'}
            self.bucket.upload_local_file(
                local_file=file_path,
                file_name=file_name,
                file_infos=file_info,
            )
        except Exception as e:
            raise StorageError(f"Could not upload file: {str(e)}")

    def delete_image(self, file_name):
        try:
            file_version = self.bucket.get_file_version_info_by_name(file_name)
            self.bucket.delete_file_version(file_version.id_, file_version.file_name)
        except Exception as e:
            raise StorageError(f"Could not delete file: {str(e)}")

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
