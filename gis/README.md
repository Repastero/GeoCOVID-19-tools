# GIS varios

## Descargar QGIS Standalone:
https://www.qgis.org/en/site/forusers/download.html

## Agregar XYZ Tile Layers:
Recomendado: Esri Imagery/Satellite<p>
https://www.spatialbias.com/2018/02/qgis-3.0-xyz-tile-layers/

## Descargar limites ciudad:
- Buscar en openstreetmap la ciudad y buscar la "realation". Ejemplo:<p>
https://www.openstreetmap.org/relation/7517633

- Descargar la relación con la siguiente página y script:<p>
http://overpass-turbo.eu/
```
[out:json][timeout:25];
(
  relation(7517633); // id relacion
);
out body;
>;
out skel qt;
```
- Presionar Run y despues Export (formato KML)

## Plugins útiles:
https://plugins.qgis.org/plugins/FreehandRasterGeoreferencer/<p>
https://plugins.qgis.org/plugins/latlontools/
