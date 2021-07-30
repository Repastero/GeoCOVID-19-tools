## Generar archivo con valores de temperatura media diarios
- ***SMN*** informa hasta 365 días previos a la fecha de ejecución (no inclusive).
- Modificar valores en script:
  - **WEATHER_STATIONS**: lista de centrales meteorológicas en orden alfabético.
    * Fuente: https://ssl.smn.gob.ar/dpd/zipopendata.php?dato=estaciones
  - **REGIONS_STATIONS_IDX**: índices en orden sur-centro-norte de centrales.
  - **OUTPUT_FILE**: nombre archivo de salida.
  - **FORECAST**: suma de temperatura pronostico mínima y máxima de centrales sur a norte, o nulo para omitir.
  - **START_DATE**: día del primer valor (en formato DDMMYYYY).
  - **END_DATE**: día del ultimo valor (en formato DDMMYYYY), o nulo para infinito.
- Correr script desde consola.
  - Si todo funciona correctamente, la salida debe ser similar a:
```
END_DATE 28072021
START_DATE 01012021
Archivo de salida: 2021-smn-pna.csv
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
