# -*- coding: utf-8 -*-

import os
import zipfile
import csv
from io import TextIOWrapper
from datetime import datetime
from timeit import default_timer as timer

from dataset import (JURISDICCION_NOMI, DEPTO_NOMI, DEPTO_REPAST, 
                    AGE_GROUP_EQUIV, AGE_GROUP_REPAST_COUNT, VACCINE_AG_COUNTER, DEPTO_REPAST_POP,
                    VACCINE_ALIAS)

NOMIVAC_FILE_URL = 'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/datos_nomivac_covid19.zip'
NOMIVAC_FILE_NAME = 'datos_nomivac_covid19.zip'

START_DATE = datetime(2020,12,28) # lunes 28 de diciembre (en realidad es el Martes 29)
START_DAY = 362 # indice primer dia (363 en realidad)

SCHEDULE_FILE_NAME = 'vac-schedule.csv'
SCHEDULE_FILE_HEADER = 'day,dose,5-14,15-24,25-39,40-64,65+\n' # header csv de salida
VACTYPES_FILE_NAME = 'vac-types.csv'
VACTYPES_FILE_HEADER = 'type,dose,5-14,15-24,25-39,40-64,65+\n' # header csv de salida

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

def get_nomivac_file(zip_name=NOMIVAC_FILE_NAME):
    if not os.path.isfile(zip_name):
        import urllib.request
        print(f"Archivo '{zip_name}' no encontrado\nIniciando descarga:")
        start_timer = timer()
        try:
            urllib.request.urlretrieve(NOMIVAC_FILE_URL, zip_name, reporthook=show_block_progress)
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

step = 0x100000 # lineas
progress_step = step
max_lines = -1 # para testeo
doses_dict = dict() # contador dosis por grupo etario
vaccines_counter = dict() # contador tipo vacunas por grupo etario

filehandle = get_nomivac_file()
zip_file_object = zipfile.ZipFile(filehandle, 'r')
file_info = zip_file_object.infolist()[0] # primer archivo

print(f'Archivo CSV: {file_info.filename}')
print(f'Tamaño: {file_info.file_size >> 20} MB')
_ = file_info.date_time
print(f'Fecha de modificacion: {_[2]:02}/{_[1]:02}/{_[0]:04} {_[3]:02}:{_[4]:02} hs')

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
                        vac_dose = int(row[dosis_index])-1 # indice tipo dosis
                        vac_type = row[vacuna_index] # nombre tipo vacuna
                        if vac_type in VACCINE_ALIAS:
                            # Cambiar alias por nombre real
                            vac_type = VACCINE_ALIAS.get(vac_type)
                        if province_id not in doses_dict:
                            # Crear contadores para provincia
                            doses_dict[province_id] = dict()
                            vaccines_counter[province_id] = dict()
                        depto = DEPTO_REPAST[province_id][DEPTO_NOMI[province_id][row[depto_id_index]]]
                        if depto not in doses_dict[province_id]:
                            # Crear contador para departamento
                            doses_dict[province_id][depto] = [dict(), dict()] # asumo 2 dosis
                            vaccines_counter[province_id][depto] = [dict(), dict()] # asumo 2 dosis
                        # Sumar dosis aplicada
                        dose_counter = doses_dict[province_id][depto][vac_dose].get(vac_week)
                        if not dose_counter:
                            dose_counter = VACCINE_AG_COUNTER.copy()
                            doses_dict[province_id][depto][vac_dose][vac_week] = dose_counter
                        dose_counter[row[grupo_index]] += 1
                        # Sumar tipo de dosis aplicada
                        type_counter = vaccines_counter[province_id][depto][vac_dose].get(vac_type)
                        if not type_counter:
                            type_counter = VACCINE_AG_COUNTER.copy()
                            vaccines_counter[province_id][depto][vac_dose][vac_type] = type_counter
                        type_counter[row[grupo_index]] += 1
                        #
print(f'Tiempo de lectura: {round((timer() - start_timer) / 60, 2)} minutos')

# Recorre provincias
for key_prov in doses_dict.keys():
    print(f'\nProvincia: {JURISDICCION_NOMI[key_prov]}')
    prov_doses_count = []
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
        
        # Crear archivos de salida con programa vacunacion
        out_files = []
        if not multiple_deptos:
            # Crea solo un archivo csv por tipo dosis
            out_files.append(open(f'{folder_path}/{SCHEDULE_FILE_NAME}', 'w', encoding='utf-8'))
            out_files[-1].write(SCHEDULE_FILE_HEADER)
        else:
            # Crea una carpeta y archivos csv por municipio o conjunto de munis
            for town in DEPTO_REPAST_POP[key_prov][key_depto].keys():
                town_folder_path = f'{folder_path}/{town}'
                if not os.path.exists(town_folder_path):
                    os.makedirs(town_folder_path)
                out_files.append(open(f'{town_folder_path}/{SCHEDULE_FILE_NAME}', 'w', encoding='utf-8'))
                out_files[-1].write(SCHEDULE_FILE_HEADER)
        # Crear archivos de salida con tipos y porcentaje de vacunas
        types_out_file = open(f'{folder_path}/{VACTYPES_FILE_NAME}', 'w', encoding='utf-8')
        types_out_file.write(VACTYPES_FILE_HEADER)
        
        # Recorre tipo dosis
        real_doses_count = []
        mod_doses_count = []
        for dose_idx in range(len(values_depto)):
            real_doses = 0
            mod_doses = 0
            out_remain = [0] * AGE_GROUP_REPAST_COUNT # para acumular el resto de vacunas entre semanas
            doses_per_ag = [0] * AGE_GROUP_REPAST_COUNT # dosis por depto, por grupo etario (sin calcular poblacion)
            for key_week in sorted(values_depto[dose_idx].keys()):
                # Convierte a las franjas etarias usadas en el modelo
                out_values = [0] * AGE_GROUP_REPAST_COUNT
                for key_ag, value_doses in values_depto[dose_idx][key_week].items():
                    _ = AGE_GROUP_EQUIV[key_ag]
                    for i in range(AGE_GROUP_REPAST_COUNT):
                        out_values[i] += _[i] * value_doses
                
                # Modificar por % poblacion del depto
                for i in range(AGE_GROUP_REPAST_COUNT):
                    doses_per_ag[i] += out_values[i]
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
                        out_files[i].write(f'{key_week * 7 + START_DAY},{dose_idx},{doses}\n')
                # Escribe las dosis del unico depto o el ultimo town
                doses = ','.join(str(val) for val in out_values)
                out_files[-1].write(f'{key_week * 7 + START_DAY},{dose_idx},{doses}\n')
            real_doses_count.append(real_doses)
            mod_doses_count.append(mod_doses)
            
            # Imprime tipos vacunas y proporcion
            initial_perc = [1000] * AGE_GROUP_REPAST_COUNT
            # Calcula la proporcion de cada tipo de vacuna por franja etaria
            for x, (type, doses) in enumerate(sorted(vaccines_counter[key_prov][key_depto][dose_idx].items())):
                # Convierte a las franjas etarias usadas en el modelo
                out_values = [0] * AGE_GROUP_REPAST_COUNT
                for key_ag, value_doses in doses.items():
                    _ = AGE_GROUP_EQUIV[key_ag]
                    for i in range(AGE_GROUP_REPAST_COUNT):
                        out_values[i] += _[i] * value_doses # cantidad de dosis tipo para cada AG
                # Calcula los % y los pasa a enteros (sobre 1000)
                perc_string = []
                for i in range(AGE_GROUP_REPAST_COUNT):
                    if x < len(vaccines_counter[key_prov][key_depto][dose_idx]) - 1:
                        if doses_per_ag[i] > 0:
                            _ = int((out_values[i] / doses_per_ag[i]) * 1000)
                            initial_perc[i] -= _
                    else: # el % del ultimo tipo, es el resto del 100%
                        _ = initial_perc[i]
                    perc_string.append(str(_))
                doses_perc = ','.join(perc_string)
                types_out_file.write(f'{type},{dose_idx},{doses_perc}\n')
        
        # Cerrar archivos csv
        for out_file in out_files:
            out_file.close()
        types_out_file.close()
        
        if PRINT_OUT_MORE_INFO:
            # Imprime cantidad dosis aplicadas en depto - totales y modificadas por poblacion
            _ = ' + '.join(str(x) for x in real_doses_count)
            print(f'{key_depto} -> {_} = {sum(real_doses_count)}', end='')
            _ = ' + '.join(str(x) for x in mod_doses_count)
            print(f' | {_} = {sum(mod_doses_count)}')
        
        # Suma cantidad de dosis aplicadas en depto - totales y modificadas por poblacion
        for i in range(len(real_doses_count)):
            if i+1 > len(prov_doses_count):
                prov_doses_count.append([real_doses_count[i], mod_doses_count[i]])
            else:
                prov_doses_count[i][0] += real_doses_count[i]
                prov_doses_count[i][1] += mod_doses_count[i]
    
    # Imprime cantidad de dosis aplicadas por provincia
    for i in range(len(prov_doses_count)):
        print(f'Dosis tipo {i+1} aplicadas: {prov_doses_count[i][0]}\t| modificadas: {prov_doses_count[i][1]}')
