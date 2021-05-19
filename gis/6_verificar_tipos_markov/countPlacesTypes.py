# -*- coding: utf-8 -*-

from collections import Counter

INPUT_FILE = 'PopularPlaces.csv'
TYPES = []

MARKOV_FILE = 'places-markov.csv'
TYPES_MARKOV = []

if __name__ == '__main__':
    in_file = open(INPUT_FILE, encoding='utf-8')
    in_file.readline() # header
    for line in in_file.readlines():
        splited = line[:-1].split(',') # borrar /n
        if len(splited) < 6:
            continue
        type = splited[1] # type
        TYPES.append(type)
    in_file.close()
    
    in_file = open(MARKOV_FILE, encoding='utf-8')
    in_file.readline() # header
    for line in in_file.readlines():
        splited = line[:-1].split(',') # borrar /n
        type = splited[0] # type
        TYPES_MARKOV.append(type)
    in_file.close()
    
    sorted_full = Counter(TYPES)
    sorted_full_mc = sorted_full.most_common()
    print('Total', len(TYPES), 'Unicos', len(sorted_full))
    for i in range(len(sorted_full_mc)):
        if sorted_full_mc[i][0] not in TYPES_MARKOV:
            if '+' not in sorted_full_mc[i][0]:
                print(f'{sorted_full_mc[i][1]};{sorted_full_mc[i][0]}')
