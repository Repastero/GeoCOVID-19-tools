# -*- coding: utf-8 -*-

"""
Script para buscar los places mas "prominentes" (pura mentira) de Google Places.

Para utilizar, asignar en "LOCATIONS" la lista de coordenadas del centro de los lugares a buscar,
y en "RADIUSES" el radio maximo donde se realiza la busqueda con respecto a las coordenadas (segun concentracion de places).
En "API_KEY" ponr la key que asigna Google por usuario.

En la version anterior filtraba la busqueda por tipo y en un radio mayor. Pero se obtienen mejores resultados sin filtrar.

La salida es un solo archivo JSON con todos los resultados, menos los repetidos.
"""

import json
import requests
import time

URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
API_KEY = 'API Google Cloud'
LOCATIONS = []
RADIUSES = []
LANGUAGE = 'es-419' # Spanish (Latin America)

INPUT_FILES = ['105.csv','210.csv','315.csv']
INPUT_RADIUSES = [53,105,158] # Cartesian

OUTPUT_FILE = 'nearby-places.txt'
PLACES_ID = set() # Para almacenar id de places

def load_coords():
    # coordenadas en grados como le gusta a Google
    for i, coor_file in enumerate(INPUT_FILES):
        with open(coor_file, 'r') as fp:
            for line in fp.readlines():
                LOCATIONS.append(line[:-2])
                RADIUSES.append(INPUT_RADIUSES[i])

def remove_duplicates(results):
    for i in reversed(range(len(results))):
        if results[i]['place_id'] not in PLACES_ID:
            PLACES_ID.add(results[i]['place_id'])
        else:
            del results[i]
    return results

load_coords()
print('Total coordenadas:', len(LOCATIONS))
total_results_count = 0
full_data = []
for i in range(len(LOCATIONS)):
    params = dict(
        location=LOCATIONS[i],
        radius=str(RADIUSES[i]),
        rankby='prominence',
        #type='establishment', # oviado (salvo en rankby='distance')
        key=API_KEY,
        language=LANGUAGE
    )
    resp = requests.get(URL, params=params)
    data = resp.json()
    if 'results' not in data:
        continue
    else:
        results_count = len(data['results'])
        results = remove_duplicates(data['results'])
        if len(results):
            full_data.extend(results)
        
        while 'next_page_token' in data:
            time.sleep(1) # 1 segundo de delay por las dudas
            params = dict(
                pagetoken=data['next_page_token'],
                key=API_KEY,
                language=LANGUAGE
            )
            resp = requests.get(URL, params=params)
            data = resp.json()
            results_count += len(data['results'])
            results = remove_duplicates(data['results'])
            if len(results):
                full_data.extend(results)
    
    total_results_count += results_count
    print('Results:', i, results_count)
print('Total:', total_results_count)
print('Duplicados:', total_results_count - len(full_data))

out_file = open(OUTPUT_FILE, 'a', encoding='utf-8')
json.dump(full_data, out_file, ensure_ascii=False, indent=4)
out_file.close()
full_data.clear()
