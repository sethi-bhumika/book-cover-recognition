import argparse
from html import entities
import spacy
import nltk
from utils.textExtractor import textExtractor
from utils.argParser import argParser


def main():
    
    #parse cli arguments
    parser = argParser()    #add language as flag!!!!
    args = parser.parse()

    #check file/directory validity

    #convert to image

    #get text info
    image_path = args.path
    extractor = textExtractor()
    ocr_output = extractor.extract(image_path)
    print("OCR done")

    #entity recognition -- put all the following functions in a separate class+interface
    nlp = spacy.load("en_core_web_trf")
    authors = []
    # nltk.download('averaged_perceptron_tagger')
    for box in ocr_output:
        sentence = box[1]
        print("string", sentence)
        # tokens = nltk.word_tokenize(sentence)
        # tokens = []
        # tokens.append(sentence)
        # tagged = nltk.pos_tag(tokens)
        # print("pos_tag", tagged)
        # entities = nltk.chunk.ne_chunk(tagged)
        # print("NER:", entities)
        doc = nlp(sentence)
        print("NERS:")
        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)
            if ent.label_ == "PERSON":
                authors.append(ent.text)


    # full = " ".join([box[1] for box in ocr_output])
    # 

    
        

    #recognize book title
    title = None
    area = 0
    for box in ocr_output:
        x = box[0][1][0]-box[0][0][0]
        y = box[0][2][1]-box[0][1][1]
        area = max(area, x*y)
        #area = max(area, y)
        if y == area:
            title = box[1]
    #check for summary bounding box!!!

    print("title", title)


    #recognize ISBN number if present
    #recognize author(s)
    print("author(s):", authors)

    #recognize publisher

    #add in excel sheet


if __name__ == "__main__":
    main()