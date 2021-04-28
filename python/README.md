# Para crear entorno virtual Python
- En el home (cd) crear entorno en carpeta "python3-ve":
```
python3 -m venv --without-pip python3-ve
```
- Activar entorno e instalar pip:
```
source ~/python3-ve/bin/activate
wget https://bootstrap.pypa.io/get-pip.py -O - | python
```
- Descargar librerias individualmente o desde requirement:
```
pip install -U matplotlib
pip install -r requirements.txt
```
- Para salir del entorno:
```
deactivate
```

## Script graph_fuller.py (para todos los departamentos o no)
- Toma como parametro el nombre completo de archivo CSV que contiene los reportes de cada simulacion.
- Genera el archivo con grafica de camas con el nombre "er_(archivo csv)".png.
* Requiere el archivo csv con el numero de camas:
```
CamasUTI_ER_aprox.csv (cambiar en PMUC_BEDS_FILE)
```
- Si todo funciona correctamente, genera el archivo con grafica de UTIs.

## Script median_report.py
- Toma como parametro el nombre completo de archivo CSV que contiene los reportes de cada simulación.
- El archivo de reporte puede ser de cualquier tipo: contactos, contagios diarios, transporte público, etc.
- Genera un archivo de salida con la mediana de todos los valores del reporte dado.
* Requiere que el reporte contenga los valores de *random_seed* y *tick*.
- Ejemplo de uso en bash:
```
# Une todos los reportes de TP en un solo archivo
awk 'FNR==1 && NR!=1{next;}{print}' ./ReportTP*.csv >> "${SLURM_JOB_ID}-tp.csv"
# Pasa el nuevo archivo como parametro al script
python median_report.py "${SLURM_JOB_ID}-tp.csv"
```
- Si funciona correctamente, genera un archivo con el nombre de la entrada con el sufijo *-median*.
