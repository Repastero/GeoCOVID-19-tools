# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
from statistics import median

RUNS_INDEX = 0 # fijo
SEED_INDEX = 1 # fijo
TICKS_INDEX = 2 # fijo

Y_AXIS_SCALE = 100
X_FIRST_DAY = 182

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
    lines = fp.readlines()
    headers = eval(lines.pop(0)) # header
    #
    beds_index = get_header_index(headers, 'Camas')
    deaths_index = get_header_index(headers, 'Muertos')
    if beds_index == -1 or deaths_index == -1:
        sys.exit("Error faltan valores 'random_seed' y/o 'tick'")
    #
    lines_len = len(lines)-1
    runs = -1
    prev_seed, prev_tick = -1, -1
    for i, line in enumerate(lines):
        splited = line[:-1].split(',') # borrar /n
        try:
            runs = int(splited[RUNS_INDEX]) # Runs
            #
            seed = int(splited[SEED_INDEX]) # Seed
            tick = int(float(splited[TICKS_INDEX])) # Tick
            #   
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
                if i == lines_len: # falta el ultimo muerto
                    deaths_list.append(last_deaths)
        except Exception as e:
            print(e)
if not beds_list:
    sys.exit("Error faltan corridas")

# Informar cantidad de muertos
print(f"Total muertos: {median(deaths_list):.2f}")

# Descartar las corridas muy cortas
max_days = max([len(beds) for beds in beds_list])
beds_list[:] = [beds for beds in beds_list if not len(beds) < max_days]

# Calcular medianas
total_median_beds = []
for i in range(max_days):
    median_beds = []
    for j in range(len(beds_list)):
        median_beds.append(beds_list[j][i])
    total_median_beds.append(median(median_beds))

# Leer camas PMUC
pmuc_beds_list = []
with open(PMUC_BEDS_FILE, 'r') as fp:
    for line in fp.readlines():
        splited = line[:-1].split(';') # borrar /n
        pmuc_beds_list.append(int(splited[0]))

short_name = CSV_FILE[:-4]
out_file_name = f"er_{short_name}.png"
# Queda graficar nomas
plt.style.use('dark_background')
plt.figure(figsize=(16, 4))
plt.title(f"{short_name} x {len(beds_list)}")
plt.plot(range(max_days), total_median_beds, 'r') # 'r-o' en rojo camas sin modificar
plt.plot(range(len(pmuc_beds_list)), pmuc_beds_list, 'w') # en blanco camas pmuc
plt.xticks(range(0, max_days, 10), range(X_FIRST_DAY, X_FIRST_DAY + max_days, 10))
plt.yticks(range(0, int(max(total_median_beds)) + 10, 10))
plt.ylim([0, Y_AXIS_SCALE])
plt.xlim([0, max_days])
plt.grid(axis='both', color='grey', linestyle='--', linewidth=.5)
# Guardar imagen
plt.savefig(out_file_name, bbox_inches='tight')
print(f"Grafica de UTIs con archivo: {CSV_FILE} > {out_file_name}")
