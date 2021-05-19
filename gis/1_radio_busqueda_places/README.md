# Generar puntos de búsqueda de Places
1. Correr script ***getPlacesRegions.py*** para generar archivos shape vacíos: **places_regions**
2. Cargar layer con archivo shape en QGIS y setear CRS usada por Google: **WGS 84 - EPSG:4326**
3. Crear polígonos con un solo trazo según densidad de places y asignar atributo **dist**. Ejemplo:
   - 100 metros: Primer anillo, zona centrica.
   - 200 metros: Segundo anillo, zona media (?).
   - 300 metros: Tercer anillo, suburbios o periferias.
4. Guardar cambios en archivo shape.

![poligonos](https://i.imgur.com/5q01kfUl.jpg)

5. Volver a correr script ***getPlacesRegions.py*** para que genere archivos csv por cada polígono.
6. Para verificar, se pueden cargar los archivos csv en QGIS como layers.
7. Cambiar escala de Symbology a metros y el tamaño a distancia + 5% (el valor en nombre de archivo).
8. Si quedan espacios sin cubrir, se pueden agregar nuevos puntos o superponer un poco cada polígono.

![radios](https://i.imgur.com/MsCH5Ehl.jpg)
