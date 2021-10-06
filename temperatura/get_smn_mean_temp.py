# -*- coding: utf-8 -*-

import os
import urllib.request
import zipfile
from time import sleep
from datetime import datetime, timedelta

INPUT_FILE_URL  = 'https://ssl.smn.gob.ar/dpd/zipopendata.php?dato=regtemp'

FORECAST_ENABLED    = True
FORECAST_URLS       = ['https://www.tiempo.com/{0}.htm', 'https://www.tiempo.com/argentina/{0}/proxima-semana'] # 7 + 7 dias de pronostico

START_DATE  = '01012021' # < a END_DATE
END_DATE    = None # > a START_DATE o None para tomar desde ultima fecha

# Indice de vectores de estaciones met. por provincias
PROVINCES_IDX = { # comentar / eliminar las no deseadas
    'entreri' : 0,
    'santafe' : 1,
    'larioja' : 2,
}
# Estaciones en orden de sur a norte
STATIONS_NAME = [
    ['GUALEGUAYCHU AERO', 'PARANA AERO', 'CONCORDIA AERO'],
    ['ROSARIO AERO', 'SAUCE VIEJO AERO', 'RECONQUISTA AERO'],
    ['CHEPES', 'CHAMICAL AERO', 'LA RIOJA AERO'], # o CHILECITO AERO
]
# Parametro para 'FORECAST_URLS', mismo orden que STATIONS_NAME
STATIONS_FORECAST_URL = [
    ['gualeguaychu', 'parana', 'concordia'],
    ['rosario', 'sauce-viejo', 'reconquista'],
    ['chepes', 'chamical', 'la-rioja_argentina-l16904'], # o chilecito
]

def read_smn_file():
    smn_file_lines = None
    try:
        filehandle, _ = urllib.request.urlretrieve(INPUT_FILE_URL)
        #filehandle = 'Registro_temperaturas-06102021.zip' # uso manual
        zip_file_object = zipfile.ZipFile(filehandle, 'r')
        file_info = zip_file_object.infolist()[0]
        print(f'Archivo SMN: {file_info.filename}')
        smn_file = zip_file_object.open(file_info.filename, 'r')
        # Leo todo el archivo en memoria por que solo contiene info. de 365 dias
        smn_file_lines = smn_file.read().decode('utf-8', 'ignore').splitlines()
        smn_file.close()
        zip_file_object.close()
        os.remove(zip_file_object.filename)
    except Exception as e:
        print('Error al descargar archivo smn', e, sep='\n')
    return smn_file_lines

def get_avg_temp(max, min):
    _ = (float(max) + float(min)) / 2
    _ += 0.001
    return round(_, 1)

def get_avg_temp_joined(val):
    temps = val.split()
    if len(temps) > 1:
        return get_avg_temp(temps[0], temps[1])
    else:
        return 404

def get_date(value, date_format='%Y-%m-%d%Z%I:%M:%S%z'):
    new_date = None
    try:
        new_date = datetime.strptime(value, date_format)
    except:
        pass
    return new_date

def get_forecast_values(req_session, station):
    temps_forecast = []
    try:
        for idx, url in enumerate(FORECAST_URLS):
            resp = req_session.get(url.format(station))
            tree = html.fromstring(resp.content)
            # La primer consulta se fija si la fecha pronosticada es la siguiente a la ultima registrada
            if idx == 0:
                date_list = tree.xpath('//meta[@property="og:updated_time"]/@content') # fecha actualizacion pronostico
                if date_list and END_DATE:
                    forecast_date = get_date(date_list[0]) # formato ISO
                    forecast_date = forecast_date.replace(tzinfo=None) - timedelta(hours=3) # paso a UTC-3
                    print('Ultima actualizacion:', forecast_date.strftime('%H:%M:%S %d/%m/%Y'))
                    last_date = get_date(END_DATE, '%d%m%Y') # formato smn
                    # Si hay mas de un dia de diferencia, se saltea el pronostico
                    _ = (forecast_date - last_date).days
                    if _ > 1:
                        print(f'Error: Pronostico {_} dias adelantado, ignorado')
                        break
            # Lee maximas y minimas pronosticadas, y calcula el promedio
            max_temps = tree.xpath('//span[@class="datos-dos-semanas"]//span[@class="maxima changeUnitT"]/@data')
            min_temps = tree.xpath('//span[@class="datos-dos-semanas"]//span[@class="minima changeUnitT"]/@data')
            _ = [get_avg_temp(max_temps[i].split('|')[0], min_temps[i].split('|')[0]) for i in range(len(max_temps))]
            temps_forecast.extend(_)
            sleep(0.5) # para demorar la proxima consulta
    except Exception as e:
        print('Error al intentar obtener pronostico:', e, sep='\n')
    return temps_forecast

# Verifica que existan las librerias para obtener pronostico
if FORECAST_ENABLED:
    try:
        from requests import Session
        from lxml import html, etree
    except ModuleNotFoundError as e:
        print(e)
        FORECAST_ENABLED = False

# Carga en una lista las lineas del archivo TXT de SMN
temp_lines = read_smn_file()
if not temp_lines:
    exit('No se obtuvo archivo con temperaturas')

# Listas con temperaturas por estaciones
output_dict = dict()
for prov_idx in PROVINCES_IDX.values():
    for st in STATIONS_NAME[prov_idx]:
        output_dict[st] = []

# Lee TXT linea por linea y guarda los valores de estaciones conocidas
station_name_col = -1
found_start = False
found_end   = False
for line in temp_lines:
    if station_name_col == -1:
        station_name_col = line.find('NOMBRE') # nombre estacion
    else:
        station_name = line[station_name_col:].rstrip()
        # Busca lista con temperaturas promedio de estacion
        temp_values = output_dict.get(station_name)
        if temp_values != None:
            temp_date = line[:8] # Fecha en formato %d%m%Y
            # Chequea si primer dia
            if not found_start:
                if not END_DATE or temp_date == END_DATE:
                    _ = get_date(temp_date, '%d%m%Y')
                    print('Fecha fin:', _.strftime('%d/%m/%Y'))
                    END_DATE = temp_date
                    found_start = True
                else:
                    # Sigue leyendo hasta encontrar fecha inicio
                    continue
            # Chequea si ultimo dia
            if not found_end:
                if temp_date == START_DATE:
                    _ = get_date(temp_date, '%d%m%Y')
                    print('Fecha inicio:', _.strftime('%d/%m/%Y'))
                    found_end = True
            else:
                # Si ya paso la fecha fin, deja de leer
                if temp_date != START_DATE:
                    break
            # Extrae TMAX TMIN y guarda promedio
            _ = get_avg_temp_joined(line[9:station_name_col-1])
            if _ != 404:
                temp_values.append(_)
            else: # Falta dato
                if not temp_values: # lista vacia, invento valor
                    temp_values.append(12.5)
                else: # copio anterior
                    temp_values.append(temp_values[-1])

# Por cada provincia, guarda el rchivo de salida con datos de sus 3 estaciones
request_session = None # para pronostico
print() # blank line
for prov_key, prov_idx in PROVINCES_IDX.items():
    temperatures = []
    min_days = 999
    for st_index, st_name in enumerate(STATIONS_NAME[prov_idx]):
        temps = output_dict.get(st_name)
        # Invertir y agregar pronostico
        temps.reverse() # vienen al revez
        if FORECAST_ENABLED:
            print('Leyendo pronostico de:', st_name)
            if not request_session:
                request_session = Session()
            _ = get_forecast_values(request_session, STATIONS_FORECAST_URL[prov_idx][st_index])
            temps.extend(_)
        # Guardo la cantidad minim de dias, para verificar
        if len(temps) < min_days:
            min_days = len(temps)
        # Guarda copia a lista de salida
        temperatures.append(temps)
    
    # Verificar que tenga muestras de las 3 estaciones
    if min_days == 0 or len(temperatures) < 3:
        print('No se obtuvieron todos los valores de temperaturas de:', prov_key)
        continue
    
    # Escrbir salida
    out_file = open(f'{END_DATE[-4:]}-{prov_key}.csv', 'w', encoding='utf-8')
    out_file.write('temp sur;temp centro;temp norte\n')
    for i in range(min_days):
        _ = ';'.join([str(temps[i]).rjust(4," ") for temps in temperatures])
        out_file.write(f'{_}\n')
    out_file.flush()
    out_file.close()
    print(f'> Archivo de salida: {out_file.name}', end='\n\n')
