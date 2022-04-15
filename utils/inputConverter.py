from abc import ABC, abstractmethod
from .exception import fileTypeException

class inputConverterInterface(ABC):       

    @abstractmethod
    def convert(self):
        pass

class inputConverter(inputConverterInterface):

    def __init__(self, filetype, filepath):
        self.input = filepath
        self.inputType = filetype

    def convert(self):
        raise fileTypeException(("Not implemented yet for input type: "+ self.inputType))