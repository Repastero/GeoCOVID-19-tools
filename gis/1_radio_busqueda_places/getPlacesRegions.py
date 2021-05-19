# -*- coding: utf-8 -*-

import os
import shapefile
from shapely.geometry import Point, Polygon

INPUT_SHP_FILE = 'places_regions.shp'

# Distancia de metro en grados para este hemisferio (deberia calcularse)
# la otra es usar un CRS en metros y despues pasarlo a grados
METER_OFFSET_X = 0.000007
METER_OFFSET_Y = 0.000007

def create_region_shp():
    w = shapefile.Writer(INPUT_SHP_FILE, shapeType=5, encoding='utf8') # POLYGON
    w.field('id',   'N', size=8) # id - 8 digitos
    w.field('dist', 'N', size=4) # distancia en metros
    w.close()

if not os.path.exists(INPUT_SHP_FILE):
    create_region_shp()
    exit("Nuevo shp creado")

polygon_file = shapefile.Reader(INPUT_SHP_FILE, encoding='utf8')
for polygon in polygon_file.shapeRecords():
    coords = polygon.shape.__geo_interface__['coordinates'][0]
    poly = Polygon(coords)
    distance = polygon.record['dist']
    if not distance:
        print("Falta atributo dist!")
        continue
    
    # sumar 5% al diametro por sobreposicion
    out_file = open(f'{int(distance*1.05)}.csv', 'w', encoding='utf-8')
    
    offset_x = METER_OFFSET_X * distance
    offset_y = METER_OFFSET_Y * distance
    
    valid = False
    start_x = poly.bounds[0]
    while start_x < poly.bounds[2]:
        valid = not valid
        start_y = poly.bounds[1]
        if valid:
            start_y -= offset_y / 2
        while start_y < poly.bounds[3]:
            _ = Point(start_x, start_y)
            if poly.contains(_):
                out_file.write(f'{start_y},{start_x}\n')
            start_y += offset_y
        start_x += offset_x
    out_file.close()
    
    print(f'Nuevo archivo: {out_file.name}')
polygon_file.close()
