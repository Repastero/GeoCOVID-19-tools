# -*- coding: utf-8 -*-

import requests
import time
import Levenshtein

CSV_HEADER = 'Name,type,ratings,latitude,longitude,place_id\n' # Header que le gusta a Google Maps

INPUT_FILE = 'PopularPlacesFull.csv'
OUTPUT_FILE = 'PopularPlacesFull-.csv'

MIN_RATINGS = 0 # Cantidad minima de valoraciones necesarias (subir este valor para mayor concentracion de lugares)
MATCH_GMB_CATEGORIES = True # Si busca el type de category retornada (ahorra CPU en False)

URL_GMAPS = 'https://www.google.com/maps/search/'

types_found = {}
gcid = []
category = []

def get_google_maps_type(session, place_id, place_name, first_search=False):
    if not first_search:
        time.sleep(30) # 30 segundos minimo entre consulta
    params = dict(
        api=1,
        query=place_name,
        query_place_id=place_id,
        hl='en'
    )
    resp = session.get(URL_GMAPS, params=params)
    #print(resp.url)
    if resp.url.find('sorry') > -1: # error de Google
        print('Error Google')
        return 'sorry'
    #
    html_text = resp.text
    find_end = html_text.find('itemprop="description">')
    find_start = html_text.rfind('<meta content=', 0, find_end)

    description = html_text[find_start+len('<meta content=')+1:find_end-2]
    #print(place_name, '->', description)
    items_text = description.split('·')
    if len(items_text) == 2:
        return items_text[1].strip()
    elif len(items_text) > 2:
        return items_text[2].strip()
    return ''

def load_gmb_categories():
    with open('gmb_categories_us.txt') as fp:
        fp.readline() # header
        for line in fp.readlines():
            splited = line[:-1].split('\t') # borrar /n
            gcid.append(splited[0])
            category.append(splited[1])
#
first_search = True
skip_lines = 0
try:
    with open(OUTPUT_FILE, 'r') as f:
        skip_lines = sum(1 for _ in f)
except:
    pass

out_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
if skip_lines == 0:
    out_file.write(CSV_HEADER) # escribe header
else:
    print(f"Saltear {skip_lines} lineas")
    skip_lines -= 1

if MATCH_GMB_CATEGORIES:
    load_gmb_categories()

# Guardar datos basicos y en el formato CSV para luego importar en Google Maps
# Creo la session por si va a buscar los tipos de Google Maps
request_session = requests.Session()
request_session.headers.update({'Accept-Language': 'en-US'})

in_file = open(INPUT_FILE, encoding='utf-8')
in_file.readline() # header
for line in in_file.readlines():
    if skip_lines > 0:
        skip_lines -= 1
        continue
    #
    splited = line[:-1].split(',') # borrar /n
    if len(splited) < 6 or int(splited[2]) < MIN_RATINGS: # ratings
        continue
    #
    type = splited[1] # type
    if not type:
        idp = splited[5]
        name = splited[0] # no hace falta pasar comas a punto y coma
        type = get_google_maps_type(request_session, idp, name, first_search)
        first_search = False
        # Extra
        rating = splited[2]
        lat = splited[3]
        lng = splited[4]
        #
        if not type:
            pass # vacio
        elif type == 'sorry':
            break # error Google, detecto bot?
        elif MATCH_GMB_CATEGORIES:
            # Busca el mejor match para type
            _ = types_found.get(type)
            if _ is None:
                type_found = False
                for i in range(len(category)):
                    if Levenshtein.ratio(type, category[i]) >= 0.9:
                        type_found = True
                        types_found[type] = gcid[i]
                        type = gcid[i]
                        del category[i]
                        del gcid[i]
                        break
                if not type_found:
                    type += '***' # buscar *** para filtrar los tipos desconocidos
            else:
                type = _
        #
        out_file.write(f'{name},{type},{rating},{lat},{lng},{idp}\n')
        out_file.flush() # Por si muere el script, o correr con -u
    else:
        out_file.write(line)
out_file.flush()
out_file.close()
in_file.close()
