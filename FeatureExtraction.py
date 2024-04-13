# importing required modules
import numpy as np
import pandas as pd
import os

# directories and file name
extractedText_folder = 'ExtractedText/'
extractedFeatures_folder = 'ExtractedFeatures/'

script_name = 'FeatureExtraction.py'
file_directory = __file__.replace(script_name, '')

## Config
#Create directory FeatureExtracted
os.makedirs(file_directory + extractedFeatures_folder, exist_ok=True)

languages = [
    'Spanish',
    'English',
    'German',
    'French'
]

columnsTitles = ['num_a', 'num_b', 'num_c', 'num_ç', 'num_d', 'num_e', 'num_f', 'num_g', 'num_h', 'num_i', 'num_j', 'num_k', 'num_l', 'num_m', 'num_n', 'num_ñ', 'num_o', 'num_p', 'num_q', 'num_r', 'num_s', 'num_t', 'num_u', 'num_v', 'num_w', 'num_x', 'num_y', 'num_z', 
                'num_sch', 'num_ch', 'num_sh', 'num_gn', 'num_esszett', 'num_ssh', 'num_ix', 'num_ll', 
                'num_triple_vowels', 'num_consonants', 'num_triple_vowels', 'num_triple_consonants', 'num_capital'
                 ]

def countTripleLetters(text, letters):
    count = 0
    for i in range(len(text) - 2):
        if text[i] in letters and text[i+1] in letters and text[i+2] in letters:
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

            num_vowels = num_a + num_e + num_i + num_o + num_u
            num_consonants = num_b + num_c + num_d + num_f + num_g + num_h + num_j + num_k + num_l + num_m + num_n + num_p + num_q + num_r + num_s + num_t + num_v + num_w + num_x + num_y + num_z
            num_triple_vowels = countTripleLetters(line.lower(), 'aeiou')
            num_triple_consonants = countTripleLetters(line.lower(), 'bcdfghjklmnpqrstvwxyz')
            num_capital = len(list(filter(lambda char: char.isupper(), line)))
            max_length_word = max(filter(lambda))




            line_feat_list = [num_a, num_b, num_c, num_ç, num_d, num_e, num_f, num_g, num_h, num_i, num_j, num_k, num_l, num_m, num_n, num_ñ, num_o, num_p, num_q, num_r, num_s, num_t, num_u, num_v, num_w, num_x, num_y, num_z, 
                              num_sch, num_ch, num_sh, num_gn, num_esszett, num_ssh, num_ix, num_ll,
                              num_triple_vowels, num_consonants, num_triple_vowels, num_triple_consonants, num_capital
                                ]
            all_obs_feat_list.append(line_feat_list)

        df = pd.DataFrame(all_obs_feat_list, columns = columnsTitles)
        df.to_csv(file_directory + extractedFeatures_folder + language + '.csv', sep=';', encoding='utf-8')




