from PIL import Image
import pytesseract
import io
import cv2
import numpy as np

class OCRResult:
    def __init__(self, text, confidence, raw):
        self.text = text
        self.confidence = confidence
        self.raw = raw

class OCRService:
    def __init__(self, settings):
        self.settings = settings
        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

    def solve_from_bytes(self, data, crop=None):
        img = Image.open(io.BytesIO(data))
        return self.solve_from_pil(img, crop)

    def solve_from_pil(self, img, crop=None):
        if crop:
            img = img.crop(crop)

        scale = self.settings.OCR_RESIZE_FACTOR
        img = img.resize((img.width * scale, img.height * scale), Image.LANCZOS).convert('L')

        np_img = np.array(img)
        np_img = cv2.GaussianBlur(np_img, (5, 5), 0)
        _, np_img = cv2.threshold(np_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        processed = Image.fromarray(np_img)
        text = pytesseract.image_to_string(processed, config='--psm 8')

        return OCRResult(text.strip(), 0.0, text)
