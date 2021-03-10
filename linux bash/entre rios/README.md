# Para simular todo Entre Rios
- Crear entorno virtual Python
- Copiar el script en python para graficar: graph_er.py
- Copiar el archivo con informacion diaria de camas en ER
- Cargar los tres modelos (pna, gchu y concord)
- El orden de los directorios por defecto es el siguiente:
```
launcher.sh
graph_er.py
CamasUTI_ER_aprox.csv
pna/ (modelo parana)
gchu/ (modelo gualeguaychu)
concord/ (modelo concordia)
~/python3-ve/ (entorno virtual Python)
MessageCenter.log4j.properties
```
- Modificar el archivo si se utilizan otros directorios
- Opcional: usar los archivos de parametros dados

## Para simular solo uno o dos modelos
- Eliminar de las lista los que no se van a utilizar
```
SCENARIO_FOLDERS=(pna gchu concord)
SCENARIO_NAMES=(parana gualeguaychu concordia)
```
