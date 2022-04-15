from abc import ABC, abstractmethod
import cv2
from pyzbar.pyzbar import decode
from fuzzywuzzy import fuzz
import spacy
import os
from os.path import dirname, abspath

class infoRecognizerInterface(ABC):

    # @abstractmethod
    # def getTitle(self):
    #     pass

    # @abstractmethod
    # def getAuthors(self):
    #     pass

    # @abstractmethod
    # def getPublishers(self):
    #     pass

    # @abstractmethod
    # def getISBN(self):
    #     pass

    @abstractmethod
    def recognize(self):
        pass

class infoRecognizer(infoRecognizerInterface):

    #initializes with OCR text as input
    def __init__(self, text, impath):
        self.text = text
        self.input = impath
        d = dirname(dirname(abspath(__file__)))
        file = os.path.join(d, "publishers.txt")
        self.datasetFile = file
        print("Recognizing book information...")
    
    #get the title of the book by finding bounding box with largest area
    def getTitle(self):
        title = None
        area = 0
        for box in self.text:
            x = box[0][1][0]-box[0][0][0]       #width of bounding box
            y = box[0][2][1]-box[0][1][1]       #height of bounding box
            if len(box[1]) <= 100:   #assumes that there are atmost 100 characters in the title to avoid summary box being recognized as title
                area = max(area, x*y)
                if x*y == area:
                    title = box[1]
        return title

    #named entity recognition for identifying publisher and author names
    def ner(self):

        publisher = set()
        authors = set()

        nlp = spacy.load("en_core_web_trf") #model used for named entity recognition
        for box in self.text:
            sentence = box[1]
            doc = nlp(sentence)

            for ent in doc.ents:
                #print(ent.text, ent.start_char, ent.end_char, ent.label_)

                #assumes that publisher name will be identified as an organization with label ORG
                if ent.label_ == 'ORG':
                    #print("publisher here", ent.text)
                    publisher.add(ent.text)
                
                elif ent.label_ == 'PERSON':
                    #if text label is "PERSON", it is assumed to be either the author name or publisher name
                    #to clarify this, we perform a fuzzy search on the dataset containing a list of well known publishers
                    match = False
                    dataset = open(self.datasetFile, 'r')
                    lines = dataset.readlines()
                    for line in lines:
                        #if fuzzy matching score is more than 80
                        if fuzz.ratio(ent.text.lower(), line.lower()) >= 80:
                            publisher.add(line[:-1])
                            ent.label_ = "ORG"
                            match = True
                            #print("matched with", line)
                            break   #assuming that there is one publisher for a single edition image
                    
                    #no match found so person is taken to be an author
                    if match is False:
                        authors.add(ent.text)
        return [authors, publisher]

    #function for fuzzy searching additional strings in the publisher dataset
    def getPublisher(self):
        publisher = set()
        for box in self.text:
            match = False
            dataset = open(self.datasetFile, 'r')
            lines = dataset.readlines()
            for line in lines:
                #if fuzzy matching score is more than 80
                if fuzz.ratio(box[1].lower(), line.lower()) >= 80:
                    publisher.add(line[:-1])
                    match = True
                    #print("matched with", line)
                    break   #assuming that there is one publisher for a single edition image
            if match is True:
                break
        return publisher




    #get ISBN number using ISBN keyword search
    def getISBN(self):
        isbn = None
        for box in self.text:
            sentence= box[1] #string recognized in the bounding box
            isbn_match = sentence.lower().find('isbn')
            if ( isbn_match != -1):
                isbn = sentence[isbn_match+5:]  #get the number displayed after the dtring 'isbn'
        return isbn

    def getISBNfromBarcode(self):
        isbn = None
        print("Trying ISBN from barcode...")
        img = cv2.imread(self.input)
        detectedBarcodes = decode(img)
        if not detectedBarcodes:
            print("No Barcode detected")
        else:
            for barcode in detectedBarcodes:              
                if barcode.data!="":
                    return str(barcode.data)[2:-1]
        return isbn
        

    def recognize(self):
        title = self.getTitle()
        isbn = self.getISBN()
        if isbn is None:
            isbn = self.getISBNfromBarcode()
        ner_output = self.ner()
        authors, publisher = ner_output[0], ner_output[1]
        addPublisher = self.getPublisher()
        publishers = publisher.union(addPublisher)
        return [title, isbn, str(list(authors)), str(list(publishers))]