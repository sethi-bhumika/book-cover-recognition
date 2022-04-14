from abc import ABC, abstractmethod
import argparse

class argParserInterface(ABC):

    # self.parser = argparse.ArgumentParser()

    @abstractmethod
    def parse(self):
        pass

    # @abstractmethod
    # def addFlag(self):
    #     pass

class argParser(argParserInterface):

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        #add argument flags
        requiredArg = self.parser.add_argument_group('required arguments')
        requiredArg.add_argument("-p", "--path", help = "enter file or directory path", type=str, required=True)
        

    def parse(self):
        return self.parser.parse_args() #returns a list of args





