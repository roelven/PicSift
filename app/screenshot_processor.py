from abc import ABC, abstractmethod
from storage_manager import S3StorageManager
import pytesseract
import os
import shutil

class ScreenshotProcessor:
    def __init__(self, storage_manager: S3StorageManager):
        self.storage_manager = storage_manager

    def process_screenshot(self, image_path: str):
        # Extract text from image
        text = pytesseract.image_to_string(image_path)

        # Upload image to cloud storage
        image_url = self.storage_manager.upload(image_path)

        # Remove local image file
        os.remove(image_path)

        return image_url, text
