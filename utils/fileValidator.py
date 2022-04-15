from abc import ABC, abstractmethod
import os
import magic
from .exception import pathException

class fileValidatorInterface(ABC):

    @abstractmethod
    def checkPathType(self, path):
        pass

    @abstractmethod
    def checkFileType(self, path):
        pass

    @abstractmethod
    def getFilesfromDirectory(self, path):
        pass


class fileValidator(fileValidatorInterface):

    def __init__(self):
        self.pathType = None
        self.imageTypes = ['image/jpeg', 'image/png', 'image/tiff']

    #validates the path and informs if it is a file or a directory
    def checkPathType(self, path):
        if not os.path.exists(path):
            raise pathException("No such file or directory")
        elif os.path.isfile(path):
            self.pathType = "file"
        else:
            self.pathType = "dir"
        return self.pathType

    #checks the file type from its mimetype if it is an image
    def checkFileType(self, path):
        mime = magic.Magic(mime=True)
        type = mime.from_file(path)
        if type in self.imageTypes:
            return [True, type]
        else:
            return [False, type]

    #iterates through the directory and returns a list of valid files
    def getFilesfromDirectory(self, path):
        files = []
        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            if os.path.isfile(f):
                files.append(f)
        return files

        
