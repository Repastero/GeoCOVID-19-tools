# -*- coding: utf-8 -*-

import os
import math
import random
import shapefile
from shapely.geometry import Point, Polygon

INPUT_SHP_FILE = 'places_regions.shp'

METER_OFFSET_X = 0
METER_OFFSET_Y = 0

def create_region_shp():
    w = shapefile.Writer(INPUT_SHP_FILE, shapeType=5, encoding='utf8') # POLYGON
    w.field('id',   'N', size=8) # id - 8 digitos
    w.field('dist', 'N', size=4) # distancia en metros
    w.close()

def degrees_to_meters(lat, lon):
    x = (lon * 20037508.34) / 180
    y = math.log(math.tan(((90 + lat) * math.pi) / 360)) / (math.pi / 180)
    y = (y * 20037508.34) / 180
    return(x, y)

if not os.path.exists(INPUT_SHP_FILE):
    create_region_shp()
    exit("Nuevo shp creado")

polygon_file = shapefile.Reader(INPUT_SHP_FILE, encoding='utf8')
for polygon in polygon_file.shapeRecords():
    coords = polygon.shape.__geo_interface__['coordinates'][0]
    poly = Polygon(coords)
    
    if METER_OFFSET_X == 0:
        # Calcular distancia de 1 metro en grados
        _ = degrees_to_meters(poly.bounds[1], poly.bounds[0])
        lon_mts = (_[0] / poly.bounds[0]) # metros lon
        METER_OFFSET_X = 1 / lon_mts
        METER_OFFSET_Y = METER_OFFSET_X
    
    distance = polygon.record['dist']
    if not distance:
        print("Falta atributo dist!")
        continue
    
    out_file = open(f'{distance}.csv', 'w', encoding='utf-8')
    offset_x = METER_OFFSET_X * distance
    offset_y = METER_OFFSET_Y * distance
    first_line = True
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
                # Sumo un offset minimo a las coordenadas, por las dudas Google detecte scraping
                rnd_offset = random.randint(0,9) * (10 ** -8)
                output_y = start_y + rnd_offset
                output_x = start_x + rnd_offset
                if first_line:
                    # en la primer linea escribe el radio + 7% por sobreposicion
                    out_file.write(f'{output_y:.8f},{output_x:.8f},{distance*0.535}\n') # 8 decimales
                    first_line = False
                else:
                    out_file.write(f'{output_y:.8f},{output_x:.8f}\n') # 8 decimales
            start_y += offset_y
        start_x += offset_x
    out_file.close()
    
    print(f'Nuevo archivo: {out_file.name}')
polygon_file.close()
