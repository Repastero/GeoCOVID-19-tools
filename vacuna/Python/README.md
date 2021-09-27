## Generar archivos CSV con las dosis de vacunas aplicadas semanalmente por departamento
- Copiar al directorio el archivo zip de *nomivac* o eliminarlo para que se descarge automaticamente.
- Opcional, modificar valores en script:
  - **PRINT_OUT_MORE_INFO**: *True* para informar en consola la cantidad de dosis aplicadas por depto.
- Correr script *get_nomivac_vaccines.py* desde consola.
  - Si todo funciona correctamente, la salida debe ser similar a:
```
Archivo 'datos_nomivac_covid19.zip' no encontrado
Iniciando descarga:
Tiempo de descarga: 5.12 minutos
Archivo CSV: datos_nomivac_covid19.csv
Tamaño: 7366 MB
Fecha de modificacion: 26/9/2021 19:55 hs
Iniciando lectura:
Tiempo de lectura: 6.31 minutos

Provincia: Santa Fe
Dosis tipo 1 aplicadas: 2385216
AstraZeneca, COVISHIELD, Cansino, Moderna, Pfizer, Sinopharm, Sputnik
0.3103, 0.0174, 0.0004, 0.0117, 0.006, 0.3028, 0.3514
Dosis tipo 2 aplicadas: 1841051
AstraZeneca, COVISHIELD, Moderna, Pfizer, Sinopharm, Sputnik
0.3311, 0.0, 0.1156, 0.0, 0.343, 0.2103

Provincia: Entre Ríos
Dosis tipo 1 aplicadas: 878152
AstraZeneca, COVISHIELD, Cansino, Moderna, Pfizer, Sinopharm, Sputnik
0.3042, 0.0194, 0.001, 0.0122, 0.0001, 0.329, 0.3341
Dosis tipo 2 aplicadas: 599471
AstraZeneca, COVISHIELD, Moderna, Pfizer, Sinopharm, Sputnik
0.3301, 0.0006, 0.0985, 0.0001, 0.357, 0.2137

Provincia: La Rioja
Dosis tipo 1 aplicadas: 264709
AstraZeneca, COVISHIELD, Cansino, Moderna, Pfizer, Sinopharm, Sputnik
0.28, 0.0267, 0.0017, 0.0325, 0.0032, 0.3117, 0.3442
Dosis tipo 2 aplicadas: 195258
AstraZeneca, COVISHIELD, Moderna, Pfizer, Sinopharm, Sputnik
0.307, 0.0005, 0.1141, 0.0, 0.3524, 0.226
```
- Se crea un directorio por provincia encontrada en *dataset.py* (ej: **Entre Ríos**, **Santa Fe**).
  - Los sub directorios se deben copiar al directorio **data** del projecto *GeoCOVID-19*.
- Fuente de URL de descarga:
  - http://datos.salud.gob.ar/dataset/vacunas-contra-covid19-dosis-aplicadas-en-la-republica-argentina

