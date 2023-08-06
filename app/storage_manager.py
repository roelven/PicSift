from backblaze.b2 import B2
import os

class StorageManager:
    def __init__(self):
        self.b2 = B2()
        self.bucket_name = os.getenv('BACKBLAZE_BUCKET')

    def upload(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                self.b2.authorize_account(os.getenv('BACKBLAZE_ID'), os.getenv('BACKBLAZE_KEY'))
                response = self.b2.upload_file(self.bucket_name, file, file_path)
                return response['contentUrl']
        except Exception as e:
            print('An error occurred during file upload:', e)
            return None

    def delete(self, file_url):
        try:
            self.b2.authorize_account(os.getenv('BACKBLAZE_ID'), os.getenv('BACKBLAZE_KEY'))
            file_name = file_url.rsplit('/', 1)[-1]
            response = self.b2.delete_file_version(file_name, file_url)
            return response
        except Exception as e:
            print('An error occurred during file deletion:', e)
            return None
