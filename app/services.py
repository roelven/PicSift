from database import DatabaseClient, DatabaseError
from storage import B2Storage, StorageError
from ocr import process_image, OCRProcessingError
from search import index_screenshot, SearchError

db_client = DatabaseClient()

class ProcessingError(Exception):
    pass

def create_screenshot(screenshot_file, db, es):
    try:
        # Process the image with Tesseract
        text = process_image(screenshot_file)

        # Upload the image to cloud storage
        image_url = upload_image(screenshot_file)

        # Save the image URL and text in the database
        screenshot_id = db_client.save_screenshot({
            'image_url': image_url,
            'text': text,
        }, db)

        # Index the screenshot in Elasticsearch
        index_screenshot({
            'id': screenshot_id,
            'image_url': image_url,
            'text': text,
        }, es)

        return screenshot_id

    except (OCRProcessingError, StorageError, DatabaseError, SearchError) as e:
        raise ProcessingError(f"Could not process screenshot: {str(e)}")

def process_screenshot(screenshot_id, db, es):
    try:
        # Retrieve the screenshot data
        screenshot = db_client.get_screenshot(screenshot_id, db)

        # Process the image with Tesseract
        text = process_image(screenshot['image_url'])

        # Update the screenshot in the database
        db_client.update_screenshot(screenshot_id, {'text': text}, db)

        # Update the screenshot in Elasticsearch
        index_screenshot({
            'id': screenshot_id,
            'image_url': screenshot['image_url'],
            'text': text,
        }, es)

    except (OCRProcessingError, DatabaseError, SearchError) as e:
        raise ProcessingError(f"Could not process screenshot: {str(e)}")
