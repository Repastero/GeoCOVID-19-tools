## Generar archivos CSV con las dosis de vacunas aplicadas semanalmente por departamento
- Copiar al directorio el archivo zip de *nomivac* o eliminarlo para que se descarge automaticamente.
- Opcional, modificar valores en script:
  - **PRINT_OUT_MORE_INFO**: *True* para informar en consola la cantidad de dosis aplicadas por depto.
- Correr script *get_nomivac_vaccines.py* desde consola.
  - Si todo funciona correctamente, la salida debe ser similar a:
```
Archivo 'datos_nomivac_covid19.zip' no encontrado
Iniciando descarga:
Tiempo de descarga: 4.82 minutos
Archivo CSV: datos_nomivac_covid19.csv
Tamaño: 7330 MB
Fecha de modificacion: 25/9/2021 7:33 hs
Iniciando lectura:
Tiempo de lectura: 6.3 minutos

Provincia: Santa Fe
Dosis totales aplicadas: 4213298
AstraZeneca, COVISHIELD, Cansino, Moderna, Pfizer, Sinopharm, Sputnik
0.3198, 0.0098, 0.0002, 0.057, 0.0025, 0.3203, 0.2904

Provincia: Entre Ríos
Dosis totales aplicadas: 1471775
AstraZeneca, COVISHIELD, Cansino, Moderna, Pfizer, Sinopharm, Sputnik
0.3146, 0.0118, 0.0005, 0.047, 0.0001, 0.3406, 0.2854

Provincia: La Rioja
Dosis totales aplicadas: 457511
AstraZeneca, COVISHIELD, Cansino, Moderna, Pfizer, Sinopharm, Sputnik
0.2913, 0.0156, 0.0009, 0.0671, 0.0018, 0.3292, 0.2941
```
- Se crea un directorio por provincia encontrada en *dataset.py* (ej: **Entre Ríos**, **Santa Fe**).
  - Los sub directorios se deben copiar al directorio **data** del projecto *GeoCOVID-19*.
- Fuente de URL de descarga:
  - http://datos.salud.gob.ar/dataset/vacunas-contra-covid19-dosis-aplicadas-en-la-republica-argentina

