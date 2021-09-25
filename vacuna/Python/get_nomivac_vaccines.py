# -*- coding: utf-8 -*-

import os
import zipfile
import csv
from io import TextIOWrapper
from datetime import datetime
from timeit import default_timer as timer

from dataset import (JURISDICCION_NOMI, DEPTO_NOMI, DEPTO_REPAST, 
                    AGE_GROUP_EQUIV, AGE_GROUP_REPAST_COUNT, VACCINE_AG_COUNTER, DEPTO_REPAST_POP)

START_DATE = datetime(2020,12,28) # lunes 28 de diciembre (en realidad es el Martes 29)
START_DAY = 362 # indice primer dia (363 en realidad)

OUTPUT_HEADER = 'day,5-14,15-24,25-39,40-64,65+\n' # header csv de salida

PRINT_OUT_MORE_INFO = False

def get_date_day(value):
    min_days = -1
    date_format = '%Y-%m-%d' # isoformat
    try:
        _ = datetime.strptime(value[:10], date_format)
        min_days = (_ - START_DATE).days
    except:
        # error formato fecha
        pass
    if min_days >= 0:
        return min_days
    else:
        return -1

def get_date_week(value):
    _ = get_date_day(value)
    if _ >= 0:
        return _ // 7
    else:
        return -1

def show_progress(cur_p, max_p):
    _ = round(cur_p / max_p * 100)
    print(f'{_}%', end='\r')

def show_block_progress(block_num, block_size, total_size):
    show_progress(block_num * block_size, total_size)

def get_nomivac_file(zip_name='datos_nomivac_covid19.zip'):
    if not os.path.isfile(zip_name):
        import urllib.request
        print(f"Archivo '{zip_name}' no encontrado\nIniciando descarga:")
        url = 'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/datos_nomivac_covid19.zip'
        start_timer = timer()
        try:
            urllib.request.urlretrieve(url, zip_name, reporthook=show_block_progress)
        except Exception as e:
            print(e)
            exit('Error al descargar archivo nomivac!')
        print(f'Tiempo de descarga: {round((timer() - start_timer) / 60, 2)} minutos')
    else:
        print(f"Archivo '{zip_name}' encontrado")
    return zip_name

# Indices columnas
prov_id_index, depto_id_index, fecha_index, grupo_index, dosis_index, vacuna_index = 0,0,0,0,0,0
header_found = False
column_count = 15

step = 0x100000
progress_step = step
max_lines = -1 # para testeo
doses_dict = dict() # contador dosis
vaccines_counter = dict() # contador tipo vacunas

filehandle = get_nomivac_file()
zip_file_object = zipfile.ZipFile(filehandle, 'r')
file_info = zip_file_object.infolist()[0] # primer archivo

print(f'Archivo CSV: {file_info.filename}')
print(f'Tamaño: {file_info.file_size >> 20} MB')
_ = file_info.date_time
print(f'Fecha de modificacion: {_[2]}/{_[1]}/{_[0]} {_[3]}:{_[4]} hs')

print('Iniciando lectura:')
start_timer = timer()
with zip_file_object.open(file_info.filename, 'r') as csvfile:
    datareader = csv.reader(TextIOWrapper(csvfile, 'utf-8'))
    for i, row in enumerate(datareader):
        if not header_found:
            # Guardar indice columnas
            try:
                prov_id_index   = row.index('jurisdiccion_residencia_id')
                depto_id_index  = row.index('depto_residencia_id')
                fecha_index     = row.index('fecha_aplicacion')
                grupo_index     = row.index('grupo_etario')
                dosis_index     = row.index('orden_dosis')
                vacuna_index    = row.index('vacuna')
                header_found = True
            except:
                exit('Header erroneo!')
            column_count = len(row)
            show_progress(0, file_info.file_size)
        elif len(row) == column_count:
            # Sumar progreso, en base a bytes recorridos
            if i == progress_step:
                show_progress(csvfile.tell(), file_info.file_size)
                progress_step += step
                if i == max_lines: # para testeo
                    break
            # Suma dosis por: provincia -> depto -> dosis -> semana -> grupo etario
            if row[prov_id_index] in JURISDICCION_NOMI:
                province_id = row[prov_id_index]
                if row[depto_id_index] in DEPTO_NOMI[province_id]:
                    vac_week = get_date_week(row[fecha_index])
                    if vac_week != -1: # si fecha ok
                        depto = DEPTO_REPAST[province_id][DEPTO_NOMI[province_id][row[depto_id_index]]]
                        vaccine = row[vacuna_index]
                        if province_id not in doses_dict:
                            doses_dict[province_id] = dict()
                            vaccines_counter[province_id] = {vaccine : 0}
                        
                        if vaccine not in vaccines_counter[province_id]:
                            vaccines_counter[province_id][vaccine] = 1
                        else:
                            vaccines_counter[province_id][vaccine] += 1
                        
                        if depto not in doses_dict[province_id]:
                            doses_dict[province_id][depto] = [dict(), dict()] # asumo 2 dosis
                        vac_dose = int(row[dosis_index])-1 # indice tipo dosis
                        dose_counter = doses_dict[province_id][depto][vac_dose].get(vac_week)
                        if not dose_counter:
                            dose_counter = VACCINE_AG_COUNTER.copy()
                            doses_dict[province_id][depto][vac_dose][vac_week] = dose_counter
                        dose_counter[row[grupo_index]] += 1
print(f'Tiempo de lectura: {round((timer() - start_timer) / 60, 2)} minutos')

# Recorre provincias
for key_prov in doses_dict.keys():
    print(f'\nProvincia: {JURISDICCION_NOMI[key_prov]}')
    prov_doses_count = 0 # suma dosis por provincia
    # Recorre departamentos
    for key_depto, values_depto in doses_dict[key_prov].items():
        # Crea directorio de provincia / depto
        folder_path = f'{JURISDICCION_NOMI[key_prov]}/{key_depto}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        pop_perc = DEPTO_REPAST_POP[key_prov][key_depto]
        # Se fija si tiene varios municipios / comunas por depto, como Santa Fe
        if isinstance(pop_perc, dict):
            multiple_deptos = True
            pop_perc = sum(pop_perc.values())
        else:
            multiple_deptos = False
        
        # Recorre tipo dosis
        real_doses_count = []
        mod_doses_count = []
        for dose_idx in range(len(values_depto)):
            out_files = []
            if not multiple_deptos:
                # Crea solo un archivo csv por tipo dosis
                out_files.append(open(f'{folder_path}/dose{dose_idx}.csv', 'w', encoding='utf-8'))
                out_files[-1].write(OUTPUT_HEADER)
            else:
                # Crea una carpeta y archivos csv por municipio o conjunto de munis
                for town in DEPTO_REPAST_POP[key_prov][key_depto].keys():
                    town_folder_path = f'{folder_path}/{town}'
                    if not os.path.exists(town_folder_path):
                        os.makedirs(town_folder_path)
                    out_files.append(open(f'{town_folder_path}/dose{dose_idx}.csv', 'w', encoding='utf-8'))
                    out_files[-1].write(OUTPUT_HEADER)
            
            real_doses = 0
            mod_doses = 0
            out_remain = [0] * AGE_GROUP_REPAST_COUNT # para acumular el resto de vacunas entre semanas
            for key_week in sorted(values_depto[dose_idx].keys()):
                # Convierte a las franjas etarias usadas en el modelo
                out_values = [0] * AGE_GROUP_REPAST_COUNT
                for key_ag, value_doses in values_depto[dose_idx][key_week].items():
                    _ = AGE_GROUP_EQUIV[key_ag]
                    for i in range(AGE_GROUP_REPAST_COUNT):
                        out_values[i] += _[i] * value_doses
                
                # Modificar por % poblacion del depto
                for i in range(AGE_GROUP_REPAST_COUNT):
                    real_doses += int(out_values[i])
                    _ = out_values[i] * pop_perc + out_remain[i]
                    out_values[i] = round(_)
                    out_remain[i] = _ - out_values[i] # guardo el resto
                    mod_doses += out_values[i]
                
                if multiple_deptos:
                    # Divide la salida del depto, al conjunto de munis / comunas
                    out_town_values = [0] * AGE_GROUP_REPAST_COUNT # para acumular el resto de vacunas entre munis / comunas
                    for i, town_perc in enumerate(DEPTO_REPAST_POP[key_prov][key_depto].values()):
                        if i == len(DEPTO_REPAST_POP[key_prov][key_depto]) - 1:
                            # Si es el unico o el ultimo town, se guarda normalmente lo que queda
                            break
                        sub_pop_perc = town_perc / pop_perc # porcentaje para town
                        for j in range(AGE_GROUP_REPAST_COUNT):
                            out_town_values[j] = round(out_values[j] * sub_pop_perc)
                            out_values[j] -= out_town_values[j] # resto el total
                        doses = ','.join(str(val) for val in out_town_values)
                        out_files[i].write(f'{key_week * 7 + START_DAY},{doses}\n')
                # Escribe las dosis del unico depto o el ultimo town
                doses = ','.join(str(val) for val in out_values)
                out_files[-1].write(f'{key_week * 7 + START_DAY},{doses}\n')
            real_doses_count.append(real_doses)
            mod_doses_count.append(mod_doses)
            # Cerrar archivos csv
            for out_file in out_files:
                out_file.close()
        
        prov_doses_count += sum(real_doses_count)
        if PRINT_OUT_MORE_INFO:
            # Imprime cantidad dosis totales y modificadas por poblacion
            _ = ' + '.join(str(x) for x in real_doses_count)
            print(f'{key_depto} -> {_} = {sum(real_doses_count)}', end='')
            _ = ' + '.join(str(x) for x in mod_doses_count)
            print(f' | {_} = {sum(mod_doses_count)}')
    
    print(f'Dosis totales aplicadas: {prov_doses_count}')
    # Imprime tipos vacunas y proporcion
    total_doses = sum(vaccines_counter[key_prov].values())
    doses_types = []
    doses_perc = []
    initial_perc = 1
    for i, (type, doses) in enumerate(sorted(vaccines_counter[key_prov].items())):
        doses_types.append(type)
        if i < len(vaccines_counter[key_prov]) - 1:
            _ = round(doses / total_doses, 4)
            initial_perc -= _
        else:
            _ = round(initial_perc, 4)
        doses_perc.append(str(_))
    print(', '.join(doses_types))
    print(', '.join(doses_perc))
