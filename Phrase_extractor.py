# importing required modules
from pypdf import PdfReader
import os
import re

## Config
# directories and file name
books_folder = 'Books/'
extractedText_folder = 'ExtractedText/'
script_name = 'Phrase_extractor.py'
file_directory = __file__.replace(script_name, '')

# assign language and book names
books = {
    'Spanish': 'J.R.R. Tolkien La Comunidad del anillo I.pdf',
    'English': 'harry-potter-book-collection-1-4.pdf',
    'German1': 'karl-marx-das-kapital-buch-1.pdf',
    'German2': 'Schloss, Das - Franz Kafka.pdf',
    'French1': 'Verne-Voyage_au_centre_de_la_Terre.pdf',
    'French2': 'Vol De Nuit - Antoine de Saint-Exupéry - PDF.pdf'
}

# Text cleaning
unwanted_charaters = ['\n', '-', 'El Señor de los anillos: La Comunidad del anillo'] # analizar si quitar '-'
number_spaces = 3 # number of repeated spaces to delete in the text

# CSV parameters
for book in books:
    if not os.path.exists(file_directory + extractedText_folder + book + '.txt'):
        #----------------------------------------------------------------------
        #--------------------------text extraction-----------------------------

        # creating a pdf reader object
        reader = PdfReader(file_directory + books_folder + books[book])

        # printing number of pages in pdf file
        pages = len(reader.pages)
        print(pages)

        # Looping every page
        i = 0
        text = ''
        while i < pages:
            # getting a specific page from the pdf file
            page_extract = reader.pages[i]

            # extracting text from page
            text_dummy = page_extract.extract_text()

            # cleaning the text from unwanted characters
            for character in unwanted_charaters:
                text_dummy = text_dummy.replace(character,'')

            # Removing space after dot
            text_dummy = text_dummy.replace('. ', '.')

            # Removing multiple space
            j = 1
            while j <= number_spaces:
                text_dummy = text_dummy.replace('  ', ' ')
                j += 1

            # append page
            text = text + text_dummy

            # iteration
            i += 1

        #----------------------------------------------------------------------
        #--------------------------------TXT-----------------------------------

        # init
        f = open(file_directory + extractedText_folder + book + '.txt', "w", encoding="utf-8")
        data_dict = {} # allocating dictionary to save csv
        text_list = text.split('.')
        for sentence in text_list:
            if '.' not in sentence and '*' not in sentence and len(sentence) > 25:
                if sentence.startswith(' '):
                    sentence = sentence[1:]
                sentence = re.sub(r'\d+', '', sentence)
                f.write(sentence + "\n")
        f.close()

