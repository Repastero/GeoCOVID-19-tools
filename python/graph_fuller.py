# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
from statistics import median

RUNS_INDEX = 0 # fijo
SEED_INDEX = 1 # fijo
TICKS_INDEX = 2 # fijo

Y_AXIS_SCALE = 100 # para don Rufiner, mantener la escala

PMUC_BEDS_FILE = 'CamasUTI_ER_aprox.csv'

def get_header_index(headers, value):
    _ = -1
    try:
        _ = headers.index(value)
    except:
        print('Header erroneo')
    return _

# Chequear que existan el parametro archivo csv
if len(sys.argv) > 1:
    CSV_FILE = sys.argv[1]
else:
    sys.exit("Error falta 'CSV_FILE'")

# Leer camas
beds_list = []
deaths_list = []
last_deaths = 0
index = -1
with open(CSV_FILE, 'r') as fp:
    line = fp.readline() # header
    headers = eval(line)
    beds_index = get_header_index(headers, 'Camas')
    deaths_index = get_header_index(headers, 'Muertos')
    if beds_index > -1 and deaths_index > -1:
        runs = -1
        prev_seed, prev_tick = -1, -1
        for line in fp.readlines():
            splited = line[:-1].split(',') # borrar /n
            runs = int(splited[RUNS_INDEX]) # Runs
            seed = int(splited[SEED_INDEX]) # Seed
            tick = int(float(splited[TICKS_INDEX])) # Tick
            
            if prev_seed != seed: # nueva corrida
                prev_tick = -1
                beds_list.append([])
                index += 1
                if prev_seed != -1:
                    deaths_list.append(last_deaths)
                prev_seed = seed
            if prev_tick < tick: # nuevo dia
                prev_tick = tick
                beds = int(float(splited[beds_index])) # Camas
                beds_list[index].append(beds)
                last_deaths = int(float(splited[deaths_index])) # Muertos
        # falta el ultimo muerto
        if len(beds_list) > 0:
            deaths_list.append(last_deaths)
    else:
        sys.exit("Error faltan valores 'Camas' y/o 'Muertos'")

# Informar cantidad de muertos
print(f"Total muertos: {median(deaths_list):.2f}")

# Calcula cantidad de dias minimos
min_days = min([len(beds) for beds in beds_list])
print(f"Dias minimos: {min_days}")

# Calcular medianas
total_median_beds = []
for i in range(min_days):
    median_beds = []
    for j in range(index + 1):
        median_beds.append(beds_list[j][i])
    total_median_beds.append(median(median_beds))

# Leer camas PMUC
pmuc_beds_list = []
with open(PMUC_BEDS_FILE, 'r') as fp:
    for line in fp.readlines():
        splited = line[:-1].split(';') # borrar /n
        pmuc_beds_list.append(int(splited[0]))

short_name = CSV_FILE[:-4]
# Queda graficar nomas
plt.style.use('dark_background')
plt.figure(figsize=(16, 4))
plt.title(f"{short_name} x {index + 1}")
plt.plot(range(min_days), total_median_beds, 'r-o') # en azul camas sin modificar
plt.plot(range(len(pmuc_beds_list)), pmuc_beds_list, 'w') # en blanco camas pmuc
plt.xticks(range(0, min_days + 1, 10))
plt.yticks(range(0, int(max(total_median_beds)) + 10, 10))
plt.ylim([0, Y_AXIS_SCALE])
plt.xlim([0, min_days])
plt.grid(axis='both', color='grey', linestyle='--', linewidth=.5)

# Guardar imagen
plt.savefig(f"er_{short_name}.png", bbox_inches='tight')
