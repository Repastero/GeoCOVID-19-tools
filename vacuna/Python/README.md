## Generar archivos CSV con las dosis de vacunas aplicadas semanalmente por departamento
- Copiar al directorio el archivo zip de *nomivac* o eliminarlo para que se descarge automaticamente.
- Opcional, modificar valores en script:
  - **PRINT_OUT_MORE_INFO**: *True* para informar en consola la cantidad de dosis aplicadas por depto.
- Correr script *get_nomivac_vaccines.py* desde consola.
  - Si todo funciona correctamente, la salida debe ser similar a:
```
Archivo 'datos_nomivac_covid19.zip' no encontrado
Iniciando descarga:
Tiempo de descarga: 5.95 minutos
Archivo CSV: datos_nomivac_covid19.csv
Tamaño: 8645 MB
Fecha de modificacion: 27/10/2021 20:01 hs
Iniciando lectura:
Tiempo de lectura: 7.48 minutos

Provincia: Santa Fe
Dosis tipo 1 aplicadas: 2661321 | modificadas: 1978902
Dosis tipo 2 aplicadas: 2138335 | modificadas: 1589508

Provincia: La Rioja
Dosis tipo 1 aplicadas: 313756  | modificadas: 236221
Dosis tipo 2 aplicadas: 227580  | modificadas: 171452

Provincia: Entre Ríos
Dosis tipo 1 aplicadas: 967597  | modificadas: 671013
Dosis tipo 2 aplicadas: 718799  | modificadas: 495074
```
- Se crea un directorio por provincia encontrada en *dataset.py* (ej: **Entre Ríos**, **Santa Fe**).
  - Los sub directorios se deben copiar al directorio **data** del projecto *GeoCOVID-19*.
- Fuente de URL de descarga:
  - http://datos.salud.gob.ar/dataset/vacunas-contra-covid19-dosis-aplicadas-en-la-republica-argentina
