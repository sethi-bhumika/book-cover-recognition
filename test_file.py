from utils.textExtractor import textExtractor
from utils.argParser import argParser
from utils.writer import excelWriter
from utils.fileValidator import fileValidator
from utils.inputConverter import inputConverter
from utils.infoRecognizer import infoRecognizer

def nottest(obj):
    obj.__test__ = False
    return obj

@nottest
def test_main(path):
    
    validator = fileValidator()
    type = validator.checkPathType(path)

    #if path is of a directory
    files = []
    if type == "dir":
        files = validator.getFilesfromDirectory(path)
    else:   #if single file
        files.append(path)

    
    data = [] #will contain the data to be written after all book entries have been extracted
    #nlp = spacy.load("en_core_web_trf") #used for named entity recognition
    for input in files:
        
        try:
            fileType = validator.checkFileType(input)
            #print(fileType)
            if fileType[0]:   #if image type
                #print("image")
                pass
            else:       #if input not of image type
                converter = inputConverter(fileType[1], input)
                converter.convert()

            #get text info
            extractor = textExtractor()
            ocr_output = extractor.extract(input)       #list containing the coordinates of bounding boxes and the text identified in them
            print("Text extraction through OCR complete")

            #recognize and extract information
            recognizer = infoRecognizer(ocr_output, input)
            book_entry = recognizer.recognize() #returns a list currently, do json object in future!!!
            print("Book information recognized: ", book_entry)

            #append entry to data
            data.append(book_entry)

        except Exception as e:
            print(e)
            continue

    writer = excelWriter("Books_Info.xlsx")
    writer.writeHeaders(['Title', 'ISBN', 'Author(s)', 'Publisher'])
    writer.write(data)
    writer.close()

def test_dir():
    test_main("./test_dir")
    
def test_single_file():
    test_main("./sample.jpeg")

def test_file_validator():
    path = "./not_a_path"
    validator = fileValidator()
    try:
        type = validator.checkPathType(path)
    except Exception:
        assert True

