# -*- coding: utf-8 -*-

import os
import urllib.request
import zipfile

WEATHER_STATIONS = ['CONCORDIA AERO', 'GUALEGUAYCHU AERO', 'PARANA AERO'] # orden alfabetico - ER
#WEATHER_STATIONS = ['RECONQUISTA AERO', 'ROSARIO AERO', 'SAUCE VIEJO AERO'] # orden alfabetico - SF
REGIONS_STATIONS_IDX = [1,2,0] # indices en orden sur a norte
INPUT_FILE_URL = 'https://ssl.smn.gob.ar/dpd/zipopendata.php?dato=regtemp'
OUTPUT_FILE = '2021-smn-pna.csv'

# Valores de pronostico de sur a norte (sumar minima y maxima) o None para ovbiar
FORECAST = [
[24,27,33,30,32,26,15, 12,19,25,21,22,25,26],
[24,28,35,32,32,28,18, 13,18,24,21,26,26,25],
[23,31,37,38,36,32,20, 14,18,26,23,27,27,28]]

# < a END_DATE
START_DATE  = '01012021'
# > a START_DATE o None para tomar dsd ultima fecha
END_DATE    = None

def read_smn_file():
    smn_file_lines = None
    try:
        filehandle, _ = urllib.request.urlretrieve(INPUT_FILE_URL)
        #filehandle = 'Registro_temperaturas-19052021.zip' # uso manual
        zip_file_object = zipfile.ZipFile(filehandle, 'r')
        first_file = zip_file_object.namelist()[0]
        smn_file = zip_file_object.open(first_file)
        smn_file_lines = smn_file.readlines()
        smn_file.close()
        zip_file_object.close()
        os.remove(zip_file_object.filename)
    except Exception as e:
        print('Error al descargar archivo:', e)
    return smn_file_lines

def get_avg_temp(val):
    temps = val.split()
    if len(temps) > 1:
        _ = (float(temps[0]) + float(temps[1])) / 2
        _ += 0.001
        return round(_, 1)
    else:
        return 404

temp_lines = read_smn_file()
if not temp_lines:
    exit('No se obtuvo archivo con temperaturas')

temperatures = []
found_start = False
found_end   = False
for line in temp_lines:
    line = line.decode('utf8', 'ignore') # hace falta pq viene en bytes
    for i in range(len(WEATHER_STATIONS)):
        idx = line.find(WEATHER_STATIONS[i])
        if idx != -1:
            if not found_start:
                if not END_DATE or line[:8] == END_DATE:
                    print("END_DATE", line[:8])
                    found_start = True
                else:
                    break
            # Primera central
            if i == 0:
                temperatures.append([0]*len(WEATHER_STATIONS))
            # Extrae TMAX TMIN
            _ = get_avg_temp(line[9:idx-1])
            if _ != 404:
                temperatures[-1][i] = _
            else: # FALTA DATO!!!
                #print(line[:8], WEATHER_STATIONS[i])
                temperatures[-1][i] = temperatures[-2][i]
            # Chequea si primer valor de ultima central
            if line[:8] == START_DATE and i == len(WEATHER_STATIONS)-1:
                print("START_DATE", line[:8])
                found_end = True
    if found_end:
        break

if not temperatures:
    exit('No se obtuvieron valores de temperaturas')

# Invertir y agregar pronostico
temperatures.reverse() # vienen al revez
if FORECAST:
    for i in range(len(FORECAST[0])):
        _ = [0]*len(WEATHER_STATIONS)
        for j,idx in enumerate(REGIONS_STATIONS_IDX):
            _[idx] = FORECAST[j][i] / 2
        temperatures.append(_)

# Salida
out_file = open(OUTPUT_FILE, 'w', encoding='utf-8')
out_file.write('temp sur;temp centro;temp norte\n')
for temp in temperatures:
    _ = ';'.join([str(temp[idx]).rjust(4," ") for idx in REGIONS_STATIONS_IDX])
    out_file.write(f'{_}\n')
out_file.flush()
out_file.close()
print(f'Archivo de salida: {out_file.name}')
