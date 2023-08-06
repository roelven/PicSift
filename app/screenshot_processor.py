import pytesseract
from PIL import Image
from storage_manager import StorageManager
import os
import asyncio

class ScreenshotProcessor:
    def __init__(self):
        self.storage_manager = StorageManager()

    def process_screenshot(self, image_path):
        text = self.perform_ocr(image_path)
        image_url = self.upload_image(image_path)
        
        # Clean up local file in async way
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.cleanup(image_path))
        loop.close()

        return image_url, text

    def perform_ocr(self, image_path):
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            print('Error while performing OCR:', e)
            return None

    def upload_image(self, image_path):
        try:
            return self.storage_manager.upload(image_path)
        except Exception as e:
            print('Error while uploading image:', e)
            return None

    async def cleanup(self, image_path):
        # Delay to allow other processes (like uploading) to complete
        await asyncio.sleep(1)

        if os.path.isfile(image_path):
            try:
                os.remove(image_path)
                print(f"Cleanup completed, {image_path} has been deleted locally.")
            except Exception as e:
                print('Error while deleting the local file:', e)
