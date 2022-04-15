from abc import ABC, abstractmethod
import xlsxwriter

class writerInterface(ABC):

    @abstractmethod
    def writeHeaders(self):
        pass

    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def close(self):
        pass

class excelWriter(writerInterface):

    #creates a .xlsx workbook and adds a sheet to it
    def __init__(self, workbookName):
        self.workbook = xlsxwriter.Workbook(workbookName)
        self.worksheet = self.workbook.add_worksheet()

    #create row containing field headings
    def writeHeaders(self, headers):
        col = 0
        for header in headers:
            self.worksheet.write(0, col, header)
            col += 1
        

    #writes dataa row-wise into the sheet from a list of lusts
    def write(self, data):
        row, column = 1, 0
        for entry in data:
            for field in entry:     #iterate over all the fields in a single row
                self.worksheet.write(row, column, field)
                column += 1
            row += 1

    def close(self):
        self.workbook.close()