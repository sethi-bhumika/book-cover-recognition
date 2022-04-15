# book-cover-recognition

Submitter Name: Bhumika
Roll No: 2019CSB1152
Course: CS305
===============================================

1. What does the program do?

The application is an implementation of a command line tool which recognizes and extracts metadata from book cover images. The path to a file or a directory is given as the -p or --path flag through the CLI, and the extracted fields, which include Title, Author names, ISBN number and Publisher Name, are written in an Excel workbook of the .xlsx format.

2. Description of the implementation

The information extraction works in two major components: OCR(optical character recognition using EasyOCR library(https://github.com/JaidedAI/EasyOCR)) and NER(named entity recognition using NLP library spaCy(https://spacy.io/)).

Through OCR, resuts are obtained in the form of bounding boxes containing text strings. This is passed to the information extractor, which uses the following heuristics to recognise fields:

- Title: This is selected as the text contained in the bounding box of the largest area and containing fewer than 100 characters. Note that the character limit assumption is necessary as boxes containing summary paragraphs etc. might have a larger area in combined images.

- ISBN Number: This is done in two ways to make the recognition system robust. First the keyword 'ISBN'(irrespective of case) is searched. If it is present, the number present right next to it is taken as the ISBN.
Secondly, in cases where only ISBN Barcode is present or the keyword could not be identified, the barcode data is used to find the ISBN, using pyzbar library.

- Author(s): For identification of authors, the entities labelled as 'PERSON' by the spaCy library are appended to a set. Set is used to avoid duplication due to the presence of the same name at multiple locations on the cover page.

-Publishers: Similar to the case of authors, the entities labelled as 'ORG' are considered to be publishers. However, it was observed in practice, that the spaCy model was ocassionaly labelling publisher names as people names. So, in addition, a dataset of already known publishers is used to fuzzy match with the OCR output strings to identify the publishing organization.

SOLID coding practices:


3. To compile:
Create a virtual env to install the dependencies, example commands to do so are as follows:
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

For running tests(test_file.py):
$ coverage run -m pytest -vv
$ coverage report

For running the program: (usage)
$ python main.py [-h|--help] -p|--path <file or directory path>

4. Directory Structure:


5. Screenshots:
![sample input image](./sample.jpeg "Input Image")
![excel output](.mdImages/xloutput "Writes output in .xlsx format")
![terminal output](.mdImages/terminaloutput "Terminal")
![test coverage 96%](.mdImages/terminaloutput "Overall test coverage")

