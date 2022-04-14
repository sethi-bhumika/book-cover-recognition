#interface and impleementation of the class to extract text from the input image using easyOCR library

from abc import ABC, abstractmethod
import easyocr

class textExtractorInterface(ABC):

    @abstractmethod
    def extract(self):
        pass

class textExtractor(textExtractorInterface):

    def __init__(self):
        pass

    def extract(self, image_path):
        print("Extracting Text...")
        reader = easyocr.Reader(['en'])
        result = reader.readtext(image_path, paragraph=True)
        return result