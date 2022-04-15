from abc import ABC, abstractmethod
import os
from .exception import pathException

class fileValidatorInterface(ABC):

    @abstractmethod
    def checkFileType(self, path):
        pass

#validates the path and informs if it is a file or a directory
class fileValidator(fileValidatorInterface):

    def __init__(self):
        pass

    def checkFileType(self, path):
        if not os.path.exists(path):
            raise pathException("No such file or directory")
        elif os.path.isfile(path):
            return 0
        else:
            return 1
