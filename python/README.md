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

## Funcionamiento del script
- Toma como parametro el ID del trabajo Slurm (ej. 14500).
- Busca los archivos csv que contienen el ID dado:
```
parana_14500.csv
parana_param_14500.csv
gualeguaychu_14500.csv
gualeguaychu_param_14500.csv
concordia_14500.csv
concordia_param_14500.csv
```
- Tambien busca el archivo csv con el numero de camas:
```
CamasUTI_ER_aprox.csv (cambiar en PMUC_BEDS_FILE)
```
- Si todo funciona correctamente, genera el archivo con grafica de camas.
 
