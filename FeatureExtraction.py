# importing required modules
import numpy as np
import pandas as pd
import os
import math
import shutil
import statistics
import traceback

# directories and file name
extractedText_folder = 'ExtractedText/'
extractedFeatures_folder = 'ExtractedFeatures/'

script_name = 'FeatureExtraction.py'
file_directory = __file__.replace(script_name, '')

## Config
#Create directory FeatureExtracted
if os.path.exists(file_directory+extractedFeatures_folder):
    # Remove the folder
    shutil.rmtree(file_directory+extractedFeatures_folder)
    print(f"The folder {file_directory+extractedFeatures_folder} has been successfully removed.")
else:
    print(f"The folder {file_directory+extractedFeatures_folder} does not exist.")

os.makedirs(file_directory + extractedFeatures_folder, exist_ok=True)

# languages available
languages = [
    'Spanish',
    'English',
    'German1',
    'German2',
    'French1',
    'French2'
]

# columns of the csv
columnsTitles = ['num_a', 'num_b', 'num_c', 'num_ç', 'num_d', 'num_e', 'num_f', 'num_g', 'num_h', 'num_i', 'num_j', 'num_k', 'num_l', 'num_m', 'num_n', 'num_ñ', 'num_o', 'num_p', 'num_q', 'num_r', 'num_s', 'num_t', 'num_u', 'num_v', 'num_w', 'num_x', 'num_y', 'num_z', 
                'num_sch', 'num_ch', 'num_sh', 'num_gn', 'num_esszett', 'num_ssh', 'num_ix', 'num_ll', 'num_œ', 'num_à', 'num_á', 'num_â', 'num_ä', 'num_è', 'num_é', 'num_ê', 'num_ë', 'num_ì', 'num_í', 'num_î', 'num_ï', 'num_ò', 'num_ó', 'num_ô', 'num_ö', 'num_ù', 'num_ú', 'num_û', 'num_ü',
                 'num_consonants', 'num_vowels','num_triple_vowels','num_triple_consonants', 'num_capital','max_length_word', 'mean_length_words', 'diacritic_count', 'ratio_vowels_consonants', 'mean_vowel_per_word', 'phrase',
                 ]

# function to count three continuous of the same letter
def countTripleLetters(text, letters):
    count = 0
    for i in range(len(text) - 2):
        if text[i] in letters and text[i+1] in letters and text[i+2] in letters:
            count += 1
    return count

# function to calcualte shanon entropy
def shannon_entropy(num_vocals,num_consonants,summatory_letter_counts):

    probabilities = {}
    # Probability of each character
    total_chars = num_vocals + num_consonants
    # Accesss all items except 5 last ones

    for letter,count in summatory_letter_counts.items():
        probabilities[letter] = count /total_chars

    #Calculate entropy
    entropy = 0 
    for prob in probabilities.values():
        if prob != 0:  # Check if probability is not zero
            entropy -= prob * math.log2(prob)
    
    return entropy


# Parameters to track errors
error_list = []
line_number = -1
error_columns = ['line number', 'language', 'line', 'error'] # error columns

for language in languages:
    if not os.path.exists(file_directory + extractedFeatures_folder + language + '.csv'):
        with open(file_directory + extractedText_folder + language + '.txt', 'r', encoding='UTF-8') as file:
            lines = file.readlines()

        # feature list and counters
        all_obs_feat_list = []
        summatory_letter_counts = {
        'a': 0, 'b': 0, 'c': 0, 'ç': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0,
        'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'ñ': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0,
        's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0,
        'sch': 0, 'ch': 0, 'sh': 0, 'gn': 0, 'ß': 0, 'ss': 0, 'ix': 0, 'll': 0, 'œ': 0,
        'à': 0, 'á': 0, 'â': 0, 'ä': 0, 'è': 0, 'é': 0, 'ê': 0, 'ë': 0, 'ì': 0, 'í': 0,
        'î': 0, 'ï': 0, 'ò': 0, 'ó': 0, 'ô': 0, 'ö': 0, 'ù': 0, 'ú': 0, 'û': 0, 'ü': 0
        }
        line_letter_counts = {
        'a': 0, 'b': 0, 'c': 0, 'ç': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0,
        'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'ñ': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0,
        's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0,
        'sch': 0, 'ch': 0, 'sh': 0, 'gn': 0, 'ß': 0, 'ss': 0, 'ix': 0, 'll': 0, 'œ': 0,
        'à': 0, 'á': 0, 'â': 0, 'ä': 0, 'è': 0, 'é': 0, 'ê': 0, 'ë': 0, 'ì': 0, 'í': 0,
        'î': 0, 'ï': 0, 'ò': 0, 'ó': 0, 'ô': 0, 'ö': 0, 'ù': 0, 'ú': 0, 'û': 0, 'ü': 0
        }

        # Letters list to extract features
        vowels = {'a', 'e', 'i', 'o', 'u','à', 'á', 'â', 'ä', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ò', 'ó', 'ô', 'ö', 'ù', 'ú', 'û', 'ü'}
        diacritics = {'à', 'á', 'â', 'ä', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ò', 'ó', 'ô', 'ö', 'ù', 'ú', 'û', 'ü'}

        for line in lines:
            line_number+=1

            # Lowercase each line 
            line_lower = line.lower()
        
            # Iterate through each character 
            for char in line_letter_counts:
                num_char = line_lower.count(char)
                line_letter_counts[char] += num_char
            
            try:
                # Count vowels and consonants
                vowel_count = sum(line_letter_counts[vowel] for vowel in vowels)
                consonat_count = sum(line_letter_counts[letter] for letter in line_letter_counts) - vowel_count
                diacritic_count = sum(line_letter_counts[diacritic] for diacritic in diacritics)

                num_triple_vowels = countTripleLetters(line.lower(), 'aeiouàáâäéèêëìíîïòóôöùúûüœ')
                num_triple_consonants = countTripleLetters(line.lower(), 'bcdfghjklmnpqrstvwxyz')
                num_capital = len(list(filter(lambda char: char.isupper(), line)))
                max_length_word = max(map(len, line.split()))
                mean_length_words = statistics.mean(map(len, line.split()))
                ratio_vowels_consonants = vowel_count / consonat_count
                mean_vowel_per_word = vowel_count/len(line)
                
            except Exception as error:
                if __debug__:
                    print("Error in line number: " + str(line_number))
                    print("The line error is: " + line)
                    print("Error: " + str(error))
                    
                line_error = [line_number, language, line, str(error)]
                error_list.append(line_error)

                continue

            # Creation of array with column values
            line_feat_list = [value for value in line_letter_counts.values()]
            line_feat_list.append(vowel_count)
            line_feat_list.append(consonat_count)
            line_feat_list.append(num_triple_vowels)
            line_feat_list.append(num_triple_consonants)
            line_feat_list.append(num_capital)
            line_feat_list.append(max_length_word)
            line_feat_list.append(mean_length_words)
            line_feat_list.append(diacritic_count)
            line_feat_list.append(ratio_vowels_consonants)
            line_feat_list.append(mean_vowel_per_word)
            line_feat_list.append(line.replace(';', '|').replace('\n',""))
            all_obs_feat_list.append(line_feat_list)

            #Sum the values of line dict to summatory dict           
            for key in line_letter_counts.keys():
                summatory_letter_counts[key] += line_letter_counts[key]
            
            #Reset values of line dict
            for key in line_letter_counts.keys():
                line_letter_counts[key] = 0
        
        # Count vowels and consonants
        total_vowel = sum(summatory_letter_counts[vowel] for vowel in vowels)
        total_consonant = sum(summatory_letter_counts[letter] for letter in line_letter_counts) - total_vowel

        print(total_vowel)
        print(total_consonant)
        
        entropy = shannon_entropy(total_vowel,total_consonant,summatory_letter_counts)

        #Print all values from dict
        print('Language:',language)
        print('Entropy language ' + language + ': '+ str(entropy))
        print(summatory_letter_counts.items())


        df = pd.DataFrame(all_obs_feat_list, columns = columnsTitles)
        df.to_csv(file_directory + extractedFeatures_folder + language + '.csv', sep=';', encoding='utf-8')

# Saving errors
df = pd.DataFrame(error_list, columns = error_columns)
df.to_csv(file_directory + extractedFeatures_folder + "Errors" + '.csv', sep=';', encoding='utf-8')