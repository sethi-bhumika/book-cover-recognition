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
        result = reader.readtext(image_path, paragraph=True, x_ths=0.8, contrast_ths=0.5, batch_size=4,  y_ths = 0.6)
        return result