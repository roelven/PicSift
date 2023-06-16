try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


class OCRError(Exception):
    pass


class OCR:
    def __init__(self):
        self.check_pytesseract_path()

    @staticmethod
    def check_pytesseract_path():
        try:
            pytesseract.get_tesseract_version()
        except pytesseract.TesseractNotFoundError:
            raise OCRError(
                "Tesseract not found. Please install and set the path correctly."
            )

    def extract_text(self, image_path):
        try:
            return pytesseract.image_to_string(Image.open(image_path))
        except Exception as e:
            raise OCRError(f"Could not process image: {e}")
