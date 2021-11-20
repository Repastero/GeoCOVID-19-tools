# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from timeit import default_timer as timer

INPUT_FILE  = 'Copy of SISA 14-11-2021 sfe.csv'
OUTPUT_FILE = 'total-weekly-deaths.csv'

START_DATE = datetime(2020,7,13) # Lunes 13 de Julio

PROVI_FILTER = 'Santa Fe'
DEPTO_FILTER = None # ej: 'La Capital', 'Rosario', etc
LOCAL_FILTER = None # ej: 'SANTA FE', 'ROSARIO', etc

def get_date_day(value):
    """Puede cambiar el formato de fecha entre reportes"""
    if isinstance(value, str): # str -> formato iso
        date_format = '%Y-%m-%d'
        try:
            value = datetime.strptime(value[:10], date_format)
        except:
            return -1
    elif not isinstance(value, datetime): # int o float -> formato OLE
        try:
            value = (datetime(1899, 12, 30) + timedelta(days=value))
        except:
            return -1
    min_days = (value - START_DATE).days
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

def read_csv_file_lines():
    import csv
    print('Leyendo archivo CSV ...')
    with open(INPUT_FILE, errors='replace') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"') # o delimiter=','
        for row in spamreader:
            yield row

def read_xlsx_file_lines():
    import openpyxl
    print('Leyendo archivo XLSX ...')
    wb = openpyxl.load_workbook(INPUT_FILE, read_only=True, data_only=True, keep_links=False)
    sheet_obj = wb.active # primer hoja
    for row in sheet_obj.iter_rows(values_only=True):
        yield row
    wb.close()

weekly_deaths = [0]
duplicated = 0
header_found = False
nombres_fechas_naci_dict = dict()
if INPUT_FILE.lower().endswith('.csv'):
    get_next_row = read_csv_file_lines
else:
    get_next_row = read_xlsx_file_lines
start_timer = timer()
for row in get_next_row():
    if not header_found:
        # Guardar indice columnas
        try:
            nombre_idx      = row.index('NOMBRE')
            provi_resi_idx  = row.index('PROVINCIA_RESIDENCIA')
            depto_resi_idx  = row.index('DEPARTAMENTO_RESIDENCIA')
            local_resi_idx  = row.index('LOCALIDAD_RESIDENCIA')
            fecha_falle_idx = row.index('FECHA_FALLECIMIENTO')
            clasifica_idx   = row.index('CLASIFICACION')
            fecha_naci_idx  = row.index('FECHA_NACIMIENTO')
            header_found = True
        except:
            print(row)
            exit('Header erroneo!')
    else:
        # Filtrar por provincia, depto y/o localidad de residencia
        if PROVI_FILTER:
            if row[provi_resi_idx] != PROVI_FILTER:
                continue
        if DEPTO_FILTER:
            if row[depto_resi_idx] != DEPTO_FILTER:
                continue
        if LOCAL_FILTER:
            if row[local_resi_idx] != LOCAL_FILTER:
                continue
        # Filtra por clasificacion de caso
        clasifica = row[clasifica_idx]
        if clasifica and 'Caso confirmado' in clasifica:
            fecha_falle = row[fecha_falle_idx]
            if fecha_falle:
                week_idx = get_date_week(fecha_falle)
                if week_idx == -1:
                    continue
                nombre = row[nombre_idx]
                fecha_naci = row[fecha_naci_idx]
                # Chequea duplicados
                nombre_fechas_naci = nombres_fechas_naci_dict.get(nombre)
                if not nombre_fechas_naci:
                    nombres_fechas_naci_dict[nombre] = [fecha_naci] # fecha de nacimiento de fallecido
                else:
                    if fecha_naci not in nombre_fechas_naci:
                        nombre_fechas_naci.append(fecha_naci)
                    else:
                        duplicated += 1
                        continue
                # Suma muerte a la semana
                idx_diff = (week_idx + 1) - len(weekly_deaths)
                if idx_diff > 0: # expande cantidad de semanas
                    weekly_deaths.extend([0] * idx_diff)
                weekly_deaths[week_idx] += 1

print(f'Tiempo: {round((timer() - start_timer) / 60, 2)} minutos')
print(f'Duplicados: {duplicated}')
total_deaths = sum(weekly_deaths)
print(f'Total: {total_deaths}')
if total_deaths > 0:
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        for deaths in weekly_deaths:
            out_file.write(f'{deaths}\n')
