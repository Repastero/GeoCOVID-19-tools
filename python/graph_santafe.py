# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
from statistics import median
from datetime import datetime
from math import ceil

RUNS_INDEX = 0 # fijo
SEED_INDEX = 1 # fijo
TICKS_INDEX = 2 # fijo

Y_AXIS_SCALE = 45
X_FIRST_DAY = 194 # Dia inicio simulacion

FIS_TILL_DEATH = 19 # Dias desde infeccion a muerte

START_DATE = datetime(2020,7,13) # Dia inicio simulacion (Lunes 13 de Julio 2020)

WEEKLY_DEATHS_FILE = 'weekly-deaths.csv'

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
deaths_list = []
last_deaths = 0
index = -1
with open(CSV_FILE, 'r') as fp:
    lines = fp.readlines()
    headers = eval(lines.pop(0)) # header
    #
    deaths_index = get_header_index(headers, 'Muertos')
    if deaths_index == -1:
        sys.exit("Error faltan valores 'Muertos'")
    #
    lines_len = len(lines)-1
    prev_seed, prev_tick = -1, -1
    for i, line in enumerate(lines):
        splited = line[:-1].split(',') # borrar /n
        try:
            seed = int(splited[SEED_INDEX]) # Seed
            tick = int(float(splited[TICKS_INDEX])) # Tick
            #   
            if prev_seed != seed: # nueva corrida
                prev_tick = -1
                deaths_list.append([])
                index += 1
                prev_seed = seed
            if prev_tick < tick: # nuevo dia
                prev_tick = tick
                
                deaths = int(float(splited[deaths_index])) # Muertos acumulados
                if not deaths_list[index]:
                    last_deaths = 0
                _ = deaths - last_deaths
                if deaths > last_deaths:
                    last_deaths = deaths
                deaths_list[index].append(_)
        except Exception as e:
            print(i, e)
if not deaths_list:
    sys.exit("Error faltan corridas")

# Descartar las corridas muy cortas
max_days = max([len(deaths) for deaths in deaths_list])
deaths_list[:] = [deaths for deaths in deaths_list if not len(deaths) < max_days]

# Calcular medianas
total_median_deaths = []
for i in range(max_days):
    median_deaths = []
    for j in range(len(deaths_list)):
        median_deaths.append(deaths_list[j][i])
    total_median_deaths.append(median(median_deaths))

# Pasar a semanas
total_median_deaths[:] = [sum(total_median_deaths[i:i+7]) for i in range(0, len(total_median_deaths) - 6, 7)]

# Leer muertes semanales
pmuc_deaths_list = []
with open(WEEKLY_DEATHS_FILE, 'r') as fp:
    for i,line in enumerate(fp.readlines()):
        splited = line[:-1].split(';') # borrar /n
        pmuc_deaths_list.append(int(splited[0]))

# Restar dias para calcular inicio infeccion
weeks_offset = ceil(FIS_TILL_DEATH / 7)
total_median_deaths[:-weeks_offset] = total_median_deaths[weeks_offset:]
pmuc_deaths_list[:-weeks_offset] = pmuc_deaths_list[weeks_offset:]
X_FIRST_DAY += FIS_TILL_DEATH - (7 * weeks_offset)

# Informar cantidad de muertos
print(f"Total muertos modelo: {sum(total_median_deaths):.2f} vs {sum(pmuc_deaths_list[:len(total_median_deaths)]):.2f}")

max_weeks = len(pmuc_deaths_list)
short_name = CSV_FILE[:-4]
out_file_name = f"sfe_{short_name}.png"
# Queda graficar nomas
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(16, 4))
plt.title(f"Fallecidos por semana - {FIS_TILL_DEATH} dias antes")
ax.plot(range(len(total_median_deaths)), total_median_deaths, 'r', label='Modelo') # en blanco camas pmuc
ax.plot(range(max_weeks), pmuc_deaths_list, 'w', label='SISA') # en blanco camas pmuc
plt.xticks(range(max_weeks), range(X_FIRST_DAY, X_FIRST_DAY + (max_weeks*7), 7))
plt.ylim([0, Y_AXIS_SCALE])
plt.xlim([0, max_weeks-1])
plt.grid(axis='both', color='grey', linestyle='--', linewidth=.5)
ax.legend()
fig.tight_layout()
# Guardar imagen
plt.savefig(out_file_name, bbox_inches='tight')
print(f"Grafica de casos con archivo: {CSV_FILE} > {out_file_name}")
