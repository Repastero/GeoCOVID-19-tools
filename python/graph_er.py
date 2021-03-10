# -*- coding: utf-8 -*-

import sys
import os.path
import matplotlib.pyplot as plt
from statistics import median

# Modificador de acuerdo a los municipios no simulados
# (poblacion_depto / poblacion_ciudad) * (100 - (cant_municipios - 1)) / 100
TOWNS_MOD = {
'parana': 1.1794410622,
'concordia': 1.0384069687,
'gualeguaychu': 1.2116093171,
'uruguay': 1.2159112425,
'federacion': 1.8343801653,
'lapaz': 2.3849488531,
'colon': 2.3777733038,
'gualeguay': 1.1701390407,
'villaguay': 1.3429786067,
'diamante': 2.1866201706,
'nogoya': 1.547736056,
'victoria': 1.1007995729,
'federal': 1.3782114904,
'tala': 1.8141113459,
'sansalvador': 1.285898095,
'feliciano': 1.2228914267,
'ibicuy': 2.3907530612}

RUNS_INDEX = 0 # fijo
TICKS_INDEX = 1 # fijo

Y_AXIS_SCALE = 150 # para don Rufiner, mantener la escala

SCENARIO_NAMES = ['Parana', 'Gualeguaychu', 'Concordia'] # en orden
PMUC_BEDS_FILE = 'CamasUTI_ER_aprox.csv'

def get_header_index(headers, value):
    _ = -1
    try:
        _ = headers.index(value)
    except:
        print('Header erroneo')
    return _

# Chequear que existan el parametro ID
if len(sys.argv) > 1:
    JOB_ID = sys.argv[1]
else:
    sys.exit("Error falta 'SLURM_JOB_ID'")
SINK_FILES = [f'parana_{JOB_ID}.csv', f'gualeguaychu_{JOB_ID}.csv', f'concordia_{JOB_ID}.csv'] # en orden
PARAMS_FILES = [f'parana_param_{JOB_ID}.csv', f'gualeguaychu_param_{JOB_ID}.csv', f'concordia_param_{JOB_ID}.csv'] # en orden

# Chequear que existan los 6 archivos + archivo de camas
missing_files = []
for file_name in SINK_FILES + PARAMS_FILES + [PMUC_BEDS_FILE]:
    if not os.path.isfile(file_name):
        missing_files.append(file_name)
if missing_files:
    print("Error falta/n archivo/s:", ", ".join(missing_files))
    sys.exit()

# Leer cada PARAMS_FILES y SINK_FILES, y procesar en orden
full_median_beds = []
full_median_beds_mod = []
sim_max_days = -1
median_deaths_sum = 0
median_deaths_mod_sum = 0
for x in range(len(SCENARIO_NAMES)):
    param_file = PARAMS_FILES[x]
    sink_file = SINK_FILES[x]
    
    # Leer ciudades simuladas
    towns = []
    max_days = []
    with open(param_file, 'r') as fp:
        line = fp.readline() # header
        headers = eval(line)
        town_index = get_header_index(headers, 'nombreMunicipio')
        days_index = get_header_index(headers, 'diasSimulacion')
        if town_index > -1 and days_index > -1:
            for line in fp.readlines():
                splited = eval(line)
                towns.append(splited[town_index])
                max_days.append(splited[days_index])
        else:
            sys.exit("Error falta parametro 'nombreMunicipio' y/o 'diasSimulacion'")
    
    # Leer camas
    beds_list = [[[]]]
    deaths_list = []
    last_deaths = 0
    index = 0
    with open(sink_file, 'r') as fp:
        line = fp.readline() # header
        headers = eval(line)
        beds_index = get_header_index(headers, 'Camas')
        deaths_index = get_header_index(headers, 'Muertos')
        if beds_index > -1 and deaths_index > -1:
            runs = -1
            prev_run, prev_tick = -1, -1
            for line in fp.readlines():
                splited = line[:-1].split(',') # borrar /n
                prev_run = runs
                runs = int(float(splited[RUNS_INDEX])) # Runs
                ticks = int(float(splited[TICKS_INDEX])) # Ticks
                if prev_tick > ticks: # nueva corrida
                    # chequea si ya hay corridas de la misma ciudad
                    if len(beds_list) < runs:
                        beds_list.append([[]])
                    else:
                        beds_list[runs-1].append([])
                    # chequea si ya hay muertos de la misma ciudad
                    if len(deaths_list) >= prev_run:
                        deaths_list[prev_run-1].append(last_deaths)
                    else:
                        deaths_list.append([last_deaths])
                    #
                    index = len(beds_list[runs-1]) - 1
                prev_tick = ticks
                beds = int(float(splited[beds_index])) # Camas
                beds_list[runs-1][index].append(beds)
                last_deaths = int(float(splited[deaths_index])) # Muertos
            # falta el ultimo muerto
            if len(deaths_list) >= prev_run:
                deaths_list[prev_run-1].append(last_deaths)
            else:
                deaths_list.append([last_deaths])
            #
        else:
            sys.exit("Error faltan valores 'Camas' y/o 'Muertos'")
    
    # Calcular cantidad de muertos
    for i in range(len(deaths_list)):
        median_deaths = median(deaths_list[i])
        median_deaths_mod = median_deaths * TOWNS_MOD[towns[i]]
        median_deaths_sum += median_deaths
        median_deaths_mod_sum += median_deaths_mod
        print(f"{towns[i]} | Muertos: {median_deaths:.2f} | Muertos mod: {median_deaths_mod:.2f}")
    
    # Calcula cantidad de dias minimos
    if sim_max_days == -1: # supongo que el primer modelo simulado (parana) es el que mas dias tiene
        sim_max_days = max(max_days) + 1 # +1 por dia 0
    min_days = sim_max_days # ahora min es igual a max
    for i in range(len(beds_list)):
        for j in range(len(beds_list[i])):
            _ = len(beds_list[i][j])
            while _ < sim_max_days:
                beds_list[i][j].insert(0, 0)
                _ += 1
    
    # Calcular medianas hasta aca
    total_median_beds = []
    total_median_beds_mod = []
    for j in range(len(beds_list)):
        multipl = TOWNS_MOD[towns[j]]
        total_median_beds.append([])
        total_median_beds_mod.append([])
        for i in range(min_days):
            median_beds = []
            for beds in beds_list[j]:
                median_beds.append(beds[i])
            _ = median(median_beds)
            total_median_beds[j].append(_)
            total_median_beds_mod[j].append(_ * multipl)
    
    # Por ultimo sumar todos
    if not full_median_beds:
        full_median_beds = [0] * min_days
        full_median_beds_mod = [0] * min_days
    for i in range(min_days):
        bsum, bsum_mod = 0, 0
        for j in range(len(total_median_beds)):
            bsum += total_median_beds[j][i]
            bsum_mod += total_median_beds_mod[j][i]
        full_median_beds[i] += bsum
        full_median_beds_mod[i] += bsum_mod

print(f"Total muertos: {median_deaths_sum:.2f} | Total muertos mod: {median_deaths_mod_sum:.2f}")

# Leer camas PMUC
pmuc_beds_list = []
with open(PMUC_BEDS_FILE, 'r') as fp:
    for line in fp.readlines():
        splited = line[:-1].split(';') # borrar /n
        pmuc_beds_list.append(int(float(splited[0])))

# Queda graficar nomas
plt.style.use('dark_background')
plt.figure(figsize=(16, 4))
plt.title(f"Entre Rios x {index + 1}")
plt.plot(range(min_days), full_median_beds, 'b-o') # en azul camas sin modificar
plt.plot(range(min_days), full_median_beds_mod, 'r-o') # en rojo camas modificadas
plt.plot(range(len(pmuc_beds_list)), pmuc_beds_list, 'w') # en blanco camas pmuc
plt.xticks(range(0, min_days + 1, 10))
plt.yticks(range(0, int(max(full_median_beds_mod)) + 10, 10))
plt.ylim([0, Y_AXIS_SCALE])
plt.xlim([0, min_days])
plt.grid(axis='both', color='grey', linestyle='--', linewidth=.5)

# Guardar imagen
plt.savefig(f"entrerios_{JOB_ID}.png", bbox_inches='tight')
