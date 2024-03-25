# importing required modules
from pypdf import PdfReader
import pandas as pd


## Config
# directories and file name
file_directory = 'E:/Mega/Master/2023- 2024 2ro/Pattern recognition/'
file_name = 'J.R.R. Tolkien La Comunidad del anillo I.pdf' # file to extract text

extracted_text_file = 'extracted_text_file.txt' # file to save the text extracted
extracted_csv_file = 'Extracted data.csv'

# Text cleaning
unwanted_charaters = ['\n', '-'] # analizar si quitar '-'
number_spaces = 3 # number of repeated spaces to delete in the text

# CSV parameters




#----------------------------------------------------------------------
#--------------------------text extraction-----------------------------

# creating a pdf reader object
reader = PdfReader(file_directory+file_name)

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

# save in txt
f = open(file_directory + extracted_text_file, "w", encoding="utf-8")
f.write(text)
f.close()

#----------------------------------------------------------------------
#--------------------------------CSV-----------------------------------

# init
open(file_directory + extracted_csv_file, "w", encoding="utf-8").close() # clean csv
data_dict = {} # allocating dictionary to save csv
text_list = text.split('. ')

# this section for constructing csv table
#----------------------------------------------------------------------
# Add main column and data, phrases
data_dict['Phrase'] = text_list

#

#


#----------------------------------------------------------------------

# Create DataFrame and saving
df = pd.DataFrame(data_dict)
df.to_csv(file_directory + extracted_csv_file, sep=';', encoding='utf-8')