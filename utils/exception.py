#template for throwing custom exceptions
class customException(Exception):

    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)

#invalid file/directory path exception
class pathException(customException):

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return super().__str__()