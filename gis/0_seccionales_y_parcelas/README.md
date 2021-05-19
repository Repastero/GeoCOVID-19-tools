# Generar ubicación de hogares según seccional
1. Correr script ***getSectoralParcels.py*** para generar archivos shape vacíos: **sectorals**
2. Cargar layer con archivo shape en QGIS y setear CRS: **WGS 84 - EPSG:4326**
3. Crear polígonos de un solo trazo, dividiendo en seccionales la parte habitada.
4. Setear en cada polígono el índice de seccional y la cantidad de hogares a crear.
5. Guardar cambios en el archivo shape.

![seccionales](https://i.imgur.com/y6QjdLQl.jpg)

6. Volver a correr script ***getSectoralParcels.py*** para crear nuevos archivos de parcelas.
7. Para verificar, se puede cargar un layer en QGIS con el nuevo shapefile **parcels**.
8. Para variar la separación entre hogares, modificar los atributos *OFFSET_X* y *OFFSET_Y*.

![parcelas](https://i.imgur.com/8KrGbcSl.jpg)
