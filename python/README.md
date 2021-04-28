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

## Script graph_fuller.py (para Entre Rios completo)
- Toma como parametro el nombre completo de archivo CSV que contiene los reportes de cada simulacion.
- Genera el archivo con grafica de camas con el nombre "er_(archivo csv)".png.
* Requiere el archivo csv con el numero de camas:
```
CamasUTI_ER_aprox.csv (cambiar en PMUC_BEDS_FILE)
```
- Si todo funciona correctamente, genera el archivo con grafica de UTIs.
