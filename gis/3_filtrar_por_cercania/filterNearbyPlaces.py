# -*- coding: utf-8 -*-

"""
Script para filtrar los places obtenidos con el script anterior "nearbySearchPlaces.py".
Carga los datos de cada place, filtra la direccion y elimina (con suerte) los places repetidos.

La salida es un CSV con los datos basicos y con el formato para cargarlo en Google Maps.
"""

import json
import math
import Levenshtein

INPUT_FILE = 'nearby-places.txt' # JSON de entrada con los palces de Google
OUTPUT_FILE = 'PopularPlacesFull.csv' # CSV de salida para importar en Google Maps
FO_OUTPUT_FILE = 'PopularPlacesFull-FO.csv'

CSV_HEADER = 'Name,type,ratings,latitude,longitude,place_id\n' # Header que le gusta a Google Maps

ADDITIONAL_TYPES = ['store', 'administrative_area_level_1', 'administrative_area_level_2', 'administrative_area_level_3', 'administrative_area_level_4', 'administrative_area_level_5', 'archipelago', 'colloquial_area', 'continent', 'country', 'establishment', 'finance', 'floor', 'food', 'general_contractor', 'geocode', 'health', 'intersection', 'locality', 'natural_feature', 'neighborhood', 'place_of_worship', 'point_of_interest', 'political', 'post_box', 'postal_code', 'postal_code_prefix', 'postal_code_suffix', 'postal_town', 'premise', 'room', 'route', 'street_address', 'street_number', 'sublocality', 'sublocality_level_1', 'sublocality_level_2', 'sublocality_level_3', 'sublocality_level_4', 'sublocality_level_5', 'subpremise', 'town_square']
MAX_FACTOR = 10.0 ** 7 # Maxima cantidad de decimales en coordenadas

ids = []
names = []
types = []
ratings = []
lats = []
lngs = []

coords = [] # lat y lon en string
filtered_out = []

def load_file():
    with open(INPUT_FILE, encoding='utf-8') as f:
        results = json.load(f)
    
    for result in results:
        if not 'business_status' in result: # No es negocio
            continue
        #
        id   = result['place_id']
        name = result['name']
        #dire = clean_up_direcction(result['vicinity'])
        
        tags = [x for x in result['types'] if x not in ADDITIONAL_TYPES] # Saco los tipos que sobran
        if len(tags) == 1:
            typep = tags[0]
        elif len(tags) > 1:
            typep = f'{tags[0]}+{tags[1]}' # Si tiene 2 tags, los sumo
        else:
            typep = ''
        
        if 'user_ratings_total' in result:
            ratin = result['user_ratings_total']
        else:
            ratin = 0
        
        lat = math.trunc(result['geometry']['location']['lat'] * MAX_FACTOR) / MAX_FACTOR
        lng = math.trunc(result['geometry']['location']['lng'] * MAX_FACTOR) / MAX_FACTOR
        coords.append(f'{lat},{lng}')
        
        ids.append(id)
        names.append(name.replace(",", ";")) # Cambia comas por punto y coma (para csv)
        #direc.append(dire)
        types.append(typep)
        ratings.append(ratin)
        lats.append(lat)
        lngs.append(lng)

def save_file():
    out_file = open(OUTPUT_FILE, 'w', encoding='utf-8')
    out_file.write(CSV_HEADER)
    for i in range(len(ids)):
        out_file.write(f'{names[i]},{types[i]},{ratings[i]},{lats[i]},{lngs[i]},{ids[i]}\n') # Guardo los datos minimos
    out_file.close()

def save_filtered_out_file():
    out_file = open(FO_OUTPUT_FILE, 'w', encoding='utf-8')
    out_file.write(CSV_HEADER)
    for line in filtered_out:
        out_file.write(line)
    out_file.close()

def save_place_info(idx):
    filtered_out.append(f'{names[idx]},{types[idx]},{ratings[idx]},{lats[idx]},{lngs[idx]},{ids[idx]}\n')

def delete_item(index):
    try:
        del ids[index]
        del names[index]
        del types[index]
        del ratings[index]
        del lats[index]
        del lngs[index]
    except Exception as e:
        print(e)

def delete_items(indexes):
    indexes.sort(reverse = True)
    for i in indexes:
        delete_item(i)
    indexes.clear()

def filter_coord(coords):
    # Elimina los que tienen coordinadas repetidas
    print('Filtrando por sobreposicion:', len(ids), end = '')
    rep = list([i for i in range(len(coords)) if coords.count(coords[i]) > 2])
    # Dejar por las dudas los que tengan tipo o algo de rating
    rep[:] = [i for i in rep if not types[i] or ratings[i] < 3]
    
    # Exporta por las dudas los eliminados
    filtered_out.append('# COORD REPETIDA\n')
    [save_place_info(i) for i in rep]
    
    delete_items(rep)
    print(' >', len(ids))

def filter_close_by():
    def get_km_distance(lat_1, lng_1, lat_2, lng_2): 
        d_lat = math.radians(lat_2 - lat_1)
        d_lng = math.radians(lng_2 - lng_1)
        temp = (  
             math.sin(d_lat / 2) ** 2 
           + math.cos(lat_1) 
           * math.cos(lat_2) 
           * math.sin(d_lng / 2) ** 2
        )
        return 6373.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))
    
    # Filtrar nombres simulares y con locacion cercana
    print('Filtrando por cercania y nombre similar:', len(ids), end = '')
    del_index = []
    for i in range(len(ids)-1):
        if i in del_index:
            continue
        name_i = names[i]
        for j in range(i+1, len(ids)):
            if j in del_index:
                continue
            name_j = names[j]
            distance_kms = get_km_distance(lngs[i], lats[i], lngs[j], lats[j])
            if distance_kms < 0.1: # 100 metros
                sim_ratio = Levenshtein.ratio(name_i, name_j)
                if sim_ratio >= 0.7 or (sim_ratio >= 0.5 and distance_kms < 0.025): # calibrar ratio con los resultados
                    if types[i] and not types[j]:
                        del_index.append(j)
                        #print(name_i, "=>", name_j)
                    elif not types[i] and types[j]:
                        del_index.append(i)
                        #print(name_i, "<=", name_j)
                        break
                    elif ratings[i] > ratings[j]:
                        del_index.append(j)
                        #print(name_i, "=>", name_j)
                    elif ratings[i] < ratings[j]:
                        del_index.append(i)
                        #print(name_i, "<=", name_j)
                        break
    
    # Exporta por las dudas los eliminados
    filtered_out.append('# POSIBLES REPETIDOS\n')
    [save_place_info(i) for i in del_index]
    
    delete_items(del_index)
    print(' >', len(ids))
#
load_file()
full_count = len(ids)
filter_coord(coords)
coords.clear()
filter_close_by()
save_file()
save_filtered_out_file()

print('Total:', full_count)
print('Guardados:', len(ids))
