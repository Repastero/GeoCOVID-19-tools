# -*- coding: utf-8 -*-

import os
import shapefile
from shapely.geometry import Point, Polygon

OFFSET_X = 0.0004
OFFSET_Y = 0.0004

INPUT_SHP_FILE = 'sectorals.shp'
OUTPUT_SHP_FILE= 'parcels'

def create_sectorals_shp():
    w = shapefile.Writer(INPUT_SHP_FILE, shapeType=5, encoding='utf8') # POLYGON
    w.field('id',       'N', size=8) # id - 8 digitos
    w.field('sectoral', 'N', size=4) # numero de seccional - 4 digitos
    w.field('houses',   'N', size=6) # cantidad de hogares - 6 digitos
    w.close()

if not os.path.exists(INPUT_SHP_FILE):
    create_sectorals_shp()
    exit("Nuevo shp creado")

w = shapefile.Writer(OUTPUT_SHP_FILE, shapeType=1, encoding='utf8') # Point
w.field('id',  'N', size=8) # id - 8 digitos
w.field('sec', 'N', size=4) # numro de seccional - 4 digitos

id = 1
polygon_file = shapefile.Reader(INPUT_SHP_FILE, encoding='utf8')
for polygon in polygon_file.shapeRecords():
    coords = polygon.shape.__geo_interface__['coordinates'][0]
    poly = Polygon(coords)
    #
    sectoral_index = polygon.record['sectoral']
    max_houses = polygon.record['houses']
    houses = 0
    first_x = poly.bounds[0]
    start_y = poly.bounds[1]
    sw_offsets = False
    while houses < max_houses:
        while start_y < poly.bounds[3]:
            start_x = first_x
            while start_x < poly.bounds[2]:
                _ = Point(start_x, start_y)
                if poly.contains(_):
                    w.point(start_x, start_y) 
                    w.record(id, sectoral_index)
                    id += 1
                    houses += 1
                    if houses == max_houses:
                        start_y = poly.bounds[3]
                        break
                start_x += OFFSET_X
            start_y += OFFSET_Y
        start_y = poly.bounds[1]
        #
        if not sw_offsets:
            start_y += OFFSET_Y / 2
            sw_offsets = True
        else:
            first_x += OFFSET_X / 2
            sw_offsets = False

w.close()
