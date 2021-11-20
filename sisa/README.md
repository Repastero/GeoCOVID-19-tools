## Generar archivo CSV con la cantidad de fallecidos por semana, según reporte de SISA
- Clasificación de casos:
Por defecto se toman como válidos los casos confirmados por laboratorio y criterio "clínico-epidemiologico", de esta forma se obtiene un resultado comparable con otras fuentes.
A continuación se muestran todas las clasificaciones ordenadas por incidencia:
```
Caso confirmado por laboratorio - Fallecido
Caso Descartado
Caso confirmado por criterio clínico-epidemiologico - Fallecido
Caso sospechoso - Fallecido - Sin muestra
Caso sospechoso - Fallecido - Con muestra sin resultado concluyente
Caso con resultado negativo-no conclusivo - Fallecido
Caso sospechoso - Fallecido - Muestra no apta
Caso Invalidado Epidemiologicamente
Otro diagnostico
```
- Si el reporte de SISA está en formato xlsx, instalar librería openpyxl:
```
pip install -U openpyxl
```
- Modificar valores en script:
  - **INPUT_FILE**: ruta archivo de reporte csv o xlsx.
  - **OUTPUT_FILE**: ruta archivo de salida csv.
- Opcional, descartar casos de personas que:
  - **PROVI_FILTER**: residan fuera de la provincia.
  - **DEPTO_FILTER**: residan fuera del departamento.
  - **LOCAL_FILTER**: residan fuera de la localidad.
- Correr script *get_sisa_weekly_deaths.py* desde consola.
  - Se debe crear el archivo **OUTPUT_FILE** y mostrar un mensaje similar a:
```
Leyendo archivo CSV ...
Tiempo: 0.69 minutos
Duplicados: 9
Total: 8751
```