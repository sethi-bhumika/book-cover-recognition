# import spacy
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
from utils.textExtractor import textExtractor
from utils.argParser import argParser
from utils.writer import excelWriter
from utils.fileValidator import fileValidator
from utils.inputConverter import inputConverter
from utils.infoRecognizer import infoRecognizer


def main():
    
    #parse cli arguments
    parser = argParser()    #add language as flag!!!! or bounding box viewer
    args = parser.parse()

    #check file/directory validity
    validator = fileValidator()
    type = validator.checkPathType(args.path)

    #if path is of a directory
    files = []
    if type == "dir":
        files = validator.getFilesfromDirectory(args.path)
    else:   #if single file
        files.append(args.path)

    
    data = [] #will contain the data to be written after all book entries have been extracted
    #nlp = spacy.load("en_core_web_trf") #used for named entity recognition
    for input in files:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        try:
            fileType = validator.checkFileType(input)
            print(fileType)
            if fileType[0]:   #if image type
                print("image")
            else:       #if input not of image type
                converter = inputConverter(fileType[1], input)
                converter.convert()

            #get text info
            extractor = textExtractor()
            ocr_output = extractor.extract(input)       #list containing the coordinates of bounding boxes and the text identified in them
            print("Text extraction through OCR complete")

            #recognize and extract information
            recognizer = infoRecognizer(ocr_output)
            book_entry = recognizer.recognize() #returns a list currently, do json object in future!!!
            print("Book information recognized: ", book_entry)

            #append entry to data
            data.append(book_entry)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        except Exception as e:
            print(e)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            continue

    

    #entity recognition -- put all the following functions in a separate class+interface
    
    # data = []
    # entry = []
    # authors = []
    # publisher = []
    # isbn = ""
    # # nltk.download('averaged_perceptron_tagger')
    # for box in ocr_output:
    #     sentence = box[1]
    #     print("string", sentence)
    #     index = sentence.lower().find('isbn')
    #     if ( index != -1):
    #         isbn = sentence[index+5:]
    #     # tokens = nltk.word_tokenize(sentence)
    #     # tokens = []
    #     # tokens.append(sentence)
    #     # tagged = nltk.pos_tag(tokens)
    #     # print("pos_tag", tagged)
    #     # entities = nltk.chunk.ne_chunk(tagged)
    #     # print("NER:", entities)
    #     doc = nlp(sentence)
    #     print("NERS:")
    #     for ent in doc.ents:
    #         print(ent.text, ent.start_char, ent.end_char, ent.label_)
    #         if ent.label_ == "PERSON":
    #             #fuzzy search in publisher list #do this for all strings??
    #             match = False
    #             file1 = open('publishers.txt', 'r')
    #             lines = file1.readlines()
    #             for line in lines:
    #                 if fuzz.ratio(ent.text.lower(), line.lower()) >= 80:
    #                     publisher.append(ent.text)
    #                     ent.label_ = "ORG"
    #                     match = True
    #                     print("matched with", line)
    #                     break
                    
    #             #else
    #             if match is False:
    #                 authors.append(ent.text)
    #         elif ent.label_ == "ORG":
    #             publisher.append(ent.text)


    # # full = " ".join([box[1] for box in ocr_output])
    # # 

    
        

    # #recognize book title
    # title = None
    # area = 0
    # for box in ocr_output:
    #     x = box[0][1][0]-box[0][0][0]
    #     y = box[0][2][1]-box[0][1][1]
    #     if len(box[1]) <= 100:   #assumes that there are atmost 100 characters in the title
    #         area = max(area, x*y)
    #         if x*y == area:
    #             title = box[1]
    #     #area = max(area, y)
        
    # #check for summary bounding box!!!

    # print("~~~~~~~~~~~~~~Info extracted~~~~~~~~~~~~~~~")

    # print("title:", title)
    # entry.append(title)


    # #recognize ISBN number if present
    # print("isbn:", isbn)
    # entry.append(isbn)

    # #recognize author(s)
    # print("author(s):", authors)
    # entry.append(str(authors))

    # #recognize publisher
    # print("publisher:", publisher)
    # entry.append(str(publisher))

    # data.append(entry)

    #add data in excel sheet
    writer = excelWriter("Books_Info.xlsx")
    writer.writeHeaders(['Title', 'ISBN', 'Author(s)', 'Publisher'])
    writer.write(data)
    writer.close()
    print(data)


if __name__ == "__main__":
    main()