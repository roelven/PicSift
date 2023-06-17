from PIL import Image
import pytesseract

def process_image(image_path, languages='eng,deu,nld'):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=languages)
        return text
    except Exception as e:
        raise OCRProcessingError(f"Could not process image: {str(e)}")
