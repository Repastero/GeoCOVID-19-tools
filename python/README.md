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