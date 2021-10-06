## Generar archivo con valores de temperatura media diarios
- ***SMN*** informa hasta 365 días previos a la fecha de ejecución (no inclusive).
- Modificar valores en script:
  - **PROVINCES_IDX**: *(opcional)* comentar / eliminar las provincias no deseadas.
  - **STATIONS_NAME**: *(opcional)* modificar centrales meteorológicas de cada provincia, en orden sur a norte.
    * Fuente: https://ssl.smn.gob.ar/dpd/zipopendata.php?dato=estaciones
  - **FORECAST_ENABLED**: obtiene los valores de temperatura media de los próximos 14 días.
  - **START_DATE**: día del primer valor (en formato DDMMYYYY).
  - **END_DATE**: día del ultimo valor (en formato DDMMYYYY), o nulo para infinito.
- Para poder obtener pronostico, instalar estas librerías individualmente o desde requirement:
```
pip install -U requests
pip install -U lxml
o
pip install -r requirements.txt
```
- Correr script desde consola.
  - Si todo funciona correctamente, la salida debe ser similar a:
```
Archivo SMN: registro_temperatura365d_smn.txt
Fecha fin: 05/10/2021
Fecha inicio: 01/01/2021

Leyendo pronostico de: GUALEGUAYCHU AERO
Ultima actualizacion: 21:42:56 05/10/2021
Leyendo pronostico de: PARANA AERO
Ultima actualizacion: 21:13:10 05/10/2021
Leyendo pronostico de: CONCORDIA AERO
Ultima actualizacion: 22:07:10 05/10/2021
> Archivo de salida: 2021-entreri.csv

Leyendo pronostico de: ROSARIO AERO
Ultima actualizacion: 22:04:42 05/10/2021
Leyendo pronostico de: SAUCE VIEJO AERO
Ultima actualizacion: 22:07:14 05/10/2021
Leyendo pronostico de: RECONQUISTA AERO
Ultima actualizacion: 22:07:16 05/10/2021
> Archivo de salida: 2021-santafe.csv

Leyendo pronostico de: CHEPES
Ultima actualizacion: 22:07:19 05/10/2021
Leyendo pronostico de: CHAMICAL AERO
Ultima actualizacion: 22:07:22 05/10/2021
Leyendo pronostico de: LA RIOJA AERO
Ultima actualizacion: 21:43:13 05/10/2021
> Archivo de salida: 2021-larioja.csv

```
- Fuente de URLs de descarga:
  - https://www.smn.gob.ar/descarga-de-datos

## Obtener valores de temperatura históricos (previos a 365 días)
- ***Ogimet*** permite consultar el clima de hasta 50 días previos a la fecha dada (inclusive).
- Obtener **ID** (INDICATIVO o IIiii) de estaciones meteorológicas deseadas:
  - https://www.ogimet.com/indicativos.phtml *(ingresar NOMBRE COMÚN)*
- Obtener hasta 50 registros de la estación, previos a la fecha dada:
  - https://www.ogimet.com/gsynres.phtml *(ingresar INDICATIVO)*
- Ejemplo: para consultar 50 días previos a 01/03/2020 en orden ascendente en Paraná:
  - https://www.ogimet.com/cgi-bin/gsynres?ord=DIR&ndays=50&ano=2020&mes=03&day=01&ind=87374
