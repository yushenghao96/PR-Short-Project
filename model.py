# importing required modules
from pypdf import PdfReader
import pandas as pd


# directories and file name
extractedFeatures_folder = 'ExtractedFeatures/'
script_name = 'model.py'
file_directory = __file__.replace(script_name, '')

# config
languages = [
    'Spanish',
    'English',
    'German',
    'French']



df = pd.read_csv(file_directory + extractedFeatures_folder + 'English' + '.csv', delimiter=";", encoding='utf-8')
print(df)
