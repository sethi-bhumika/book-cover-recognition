# book-cover-recognition

1. What does the program do?

The application is an implementation of a command line tool which recognizes and extracts metadata from book cover images. The path to a file or a directory is given as the -p or --path flag through the CLI, and the extracted fields, which include Title, Author names, ISBN number and Publisher Name, are written in an Excel workbook of the .xlsx format.

2. Description of the implementation

The information extraction works in two major components: OCR(optical character recognition using EasyOCR library(https://github.com/JaidedAI/EasyOCR)) and NER(named entity recognition using NLP library spaCy(https://spacy.io/)).

Through OCR, results are obtained in the form of bounding boxes containing text strings. This is passed to the information extractor, which uses the following heuristics to recognise fields:

- Title: This is selected as the text contained in the bounding box of the largest area and containing fewer than 100 characters. Note that the character limit assumption is necessary as boxes containing summary paragraphs etc. might have a larger area in combined images.

- ISBN Number: This is done in two ways to make the recognition system robust. First the keyword 'ISBN'(irrespective of case) is searched. If it is present, the number present right next to it is taken as the ISBN.
Secondly, in cases where only ISBN Barcode is present or the keyword could not be identified, the barcode data is used to find the ISBN, using pyzbar library.

- Author(s): For identification of authors, the entities labelled as 'PERSON' by the spaCy library are appended to a set. Set is used to avoid duplication due to the presence of the same name at multiple locations on the cover page.

- Publishers: Similar to the case of authors, the entities labelled as 'ORG' are considered to be publishers. However, it was observed in practice, that the spaCy model was ocassionaly labelling publisher names as people names. So, in addition, a dataset of already known publishers is used to fuzzy match with the OCR output strings to identify the publishing organization.

SOLID coding practices:
SOLID and DRY principles were kept in mind while designing the modules and the structure of the program.
- 1. Single Responsibility Principle: By limiting the functionality of the classes to singular responsibility.
- 2. Interface Segragation Principles: Coding to the interface has been extensibly used through the usage of abstract classes and methods and segregation is achieved by splitting into multiple independent parts.
- 3. Dependency Inversion Principle: In conjunction to increasing the scope of the application to pdf, epub files etc, an abstract inputConverter(converts specified format to image) has been created. The main function depends on this abstraction instead of individual converter functions for various filetypes(e.g. inputConverterPDF, inputConverterHTML etc.)
- 4. Open/Closed Principle: An example is the infoRecognizer class. It has the recognize function, which has no need to change to add for example, new features. The descendant class can have any additional methods. Thus it is close to modification but open to extension.
- 5. Liskov Substitution Principle: The custom exception class is inherited by the specific exception classes like pathException, fileTypeException etc., which can easily be replaced instead of the parent custom exception class.


3. To compile:
Create a virtual env to install the dependencies, example commands to do so are as follows:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

For running tests(test_file.py):
$ coverage run -m pytest -vv
$ coverage report

For running the program: (usage)
$ python main.py [-h|--help] -p|--path <file or directory path>
```
Note: 
There are warnings displayed about lack of CUDA in the absence of GPU. Further, the NLP performance might take some time on certain inputs due to the usage of GPU transform models on a CPU device.

4. Directory Structure:

```.
├── Books_Info.xlsx
├── images
│   ├── 1000splendidsuns.jpg
│   ├── barcode.jpeg
│   ├── cleancode1.jpeg
│   └── ex.jpeg
├── main.py
├── mdImages
│   ├── terminaloutput.png
│   ├── testcoverage.png
│   └── xloutput.png
├── publishers.txt
├── pytest.ini
├── README.md
├── requirements.txt
├── sample1.jpeg
├── sample.jpeg
├── test_dir
│   ├── eng.txt
│   ├── sample1.jpeg
│   ├── sample2.jpeg
│   └── sample3.jpeg
├── test_file.py
└── utils
    ├── argParser.py
    ├── exception.py
    ├── fileValidator.py
    ├── infoRecognizer.py
    ├── inputConverter.py
    ├── textExtractor.py
    └── writer.py
```


5. Screenshots:
![sample input image](./sample.jpeg "Input Image")
![excel output](./mdImages/xloutput.png "Writes output in .xlsx format")
![terminal output](./mdImages/terminaloutput.png "Terminal")
![test coverage 96%](./mdImages/testcoverage.png "Overall test coverage")

