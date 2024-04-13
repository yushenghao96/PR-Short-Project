# importing required modules
import numpy as np
import pandas as pd
import os


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


for language in languages:
    if not os.path.exists(file_directory + extractedFeatures_folder + language + '.csv'):
        with open(file_directory + extractedText_folder + language + '.txt', 'r') as file:
            lines = file.readlines()

        all_obs_feat_list = []
        for line in lines:

            num_a = line.lower().count('a')
            num_b = line.lower().count('b')
            num_c = line.lower().count('c')
            num_ç = line.lower().count('ç')
            num_d = line.lower().count('d')
            num_e = line.lower().count('e')
            num_f = line.lower().count('f')
            num_g = line.lower().count('g')
            num_h = line.lower().count('h')
            num_i = line.lower().count('i')
            num_j = line.lower().count('j')
            num_k = line.lower().count('k')
            num_l = line.lower().count('l')
            num_m = line.lower().count('m')
            num_n = line.lower().count('n')
            num_ñ = line.lower().count('ñ')
            num_o = line.lower().count('o')
            num_p = line.lower().count('p')
            num_q = line.lower().count('q')
            num_r = line.lower().count('r')
            num_s = line.lower().count('s')
            num_t = line.lower().count('t')
            num_u = line.lower().count('u')
            num_v = line.lower().count('v')
            num_w = line.lower().count('w')
            num_x = line.lower().count('x')
            num_y = line.lower().count('y')
            num_z = line.lower().count('z')
            num_sch = line.lower().count('sch')
            num_ch = line.lower().count('ch')
            num_sh = line.lower().count('sh')
            num_gn = line.lower().count('gn')
            num_esszett = line.lower().count('ß')
            num_ssh = line.lower().count('ss')
            num_ix = line.lower().count('ix')
            num_ll = line.lower().count('ll')
            #repetir con dem�s conjuntos de letras
            num_vowels = num_a + num_e + num_i + num_o + num_u
            num_consonants = num_b + num_c
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




