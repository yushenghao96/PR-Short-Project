# importing required modules
import numpy as np
import pandas as pd


VOWELS = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
CONSONANTS = {'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z',
              'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'}

## Config
# directories and file name
file_directory = 'C:/MUAR - 2/Reconeixement de formes i Machine Learning/NL/'
extractedText_folder = 'ExtractedText/'
extractedFeatures_folder = 'ExtractedFeatures/'

languages = [
    'Spanish',
    'English',
    'German',
    'French'
]

columnsTitles = ['num_a', 
                 'num_sch',
                 'num_3vowels'
                 ]

def countTripleVowels(text):
    vowels = 'aeiouAEIOU'
    count = 0
    for i in range(len(text) - 2):
        if text[i] in vowels and text[i+1] in vowels and text[i+2] in vowels:
            count += 1
    return count

def count_letters(text, letters):
    count = 0
    for char in text:
        if char in letters:
            count += 1
    return count

def count_vowels(text):
    return count_letters(text, VOWELS)

def count_consonants(text):
    return count_letters(text, CONSONANTS)

def calculate_vowel_consonant_ratio(text):
    vowel_count = count_vowels(text)
    consonant_count = count_consonants(text)
    if consonant_count == 0:
        return "No consonants found. Cannot calculate ratio."
    else:
        return vowel_count / consonant_count


for language in languages:
    with open(file_directory + extractedText_folder + language + '.txt', 'r') as file:
        lines = file.readlines()

    all_obs_feat_list = []
    for line in lines:

        num_a = line.count('a')
        #repetir con dem�s letras
        num_sch = line.count('sch')
        #repetir con dem�s conjuntos de letras
        num_triple_vowels = countTripleVowels(line)
        #reptir con consonantes
        #etc

        line_feat_list = [num_a,
                          num_sch,
                          num_triple_vowels
                            ]
        all_obs_feat_list.append(line_feat_list)

    df = pd.DataFrame(all_obs_feat_list, columns = columnsTitles)
    df.to_csv(file_directory + extractedFeatures_folder + language + '.csv', sep=';', encoding='utf-8')




