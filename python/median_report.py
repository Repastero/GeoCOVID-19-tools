# -*- coding: utf-8 -*-

import sys
from statistics import median

def get_header_index(headers, value):
    _ = -1
    try:
        _ = headers.index(value)
    except:
        print('Header erroneo:', value)
    return _

# Chequear que existan el parametro archivo csv
if len(sys.argv) > 1:
    CSV_FILE = sys.argv[1]
else:
    sys.exit("Error falta 'CSV_FILE'")

# Leer camas
values_list = []
last_deaths = 0
index = -1
headers = None
with open(CSV_FILE, 'r') as fp:
    lines = fp.readlines()
    headers = eval(lines.pop(0)) # header
    #
    run_index = get_header_index(headers, 'run')
    seed_index = get_header_index(headers, 'random_seed')
    tick_index = get_header_index(headers, 'tick')
    #
    skip_indexes = []
    if seed_index == -1 or tick_index == -1:
        sys.exit("Error faltan valores 'random_seed' y/o 'tick'")
    else:
        skip_indexes = [seed_index, tick_index]
        if run_index > -1:
            skip_indexes.insert(0, run_index)
    #
    prev_seed, prev_tick = -1, -1
    for line in lines:
        splited = line[:-1].split(',') # borrar /n
        try:
            #
            seed = int(splited[seed_index]) # Seed
            tick = int(float(splited[tick_index])) # Tick
            #
            if prev_seed != seed: # nueva corrida
                prev_tick = -1
                values_list.append([])
                index += 1
                prev_seed = seed
            if prev_tick < tick: # nuevo dia
                prev_tick = tick
                values_list[index].append([float(val) for idx, val in enumerate(splited) if idx not in skip_indexes])
        except Exception as e:
            print(e)
if not values_list:
    sys.exit("Error faltan corridas")

# Descartar los muy cortos
max_days = max([len(values) for values in values_list])
values_list[:] = [values for values in values_list if not len(values) < max_days]

# Calcular medianas
median_values = [[] for i in range(max_days)]
for i in range(len(values_list[0][0])): # valores
    for j in range(max_days): # dias
        values = []
        for k in range(len(values_list)): # corridas
            values.append(values_list[k][j][i])
        median_values[j].append(median(values)) # mismo valor i de todas las corridas en dia j

# Guardar csv de salida
out_file_name = f"{CSV_FILE[:-4]}-median.csv"
out_file = open(out_file_name, 'w', encoding='utf-8')
out_file.write(','.join(f'"{h}"' for i, h in enumerate(headers) if i not in skip_indexes)) # header
out_file.write('\n')
for values in median_values:
    out_file.write(','.join(format(x, ".2f") for x in values))
    out_file.write('\n')
out_file.flush()
out_file.close()
print(f"Mediana de archivo: {CSV_FILE} > {out_file_name}")
