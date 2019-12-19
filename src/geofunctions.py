import numpy as np
import math

def coords_to_pixel(longitude, latitude, zoom=20):
    '''from longitude and latitude in degrees and zoom, returns equivalent in pixel coordinates'''
    x = (128/np.pi) * (2**zoom) * (np.radians(longitude) + np.pi)
    y = (128/np.pi) * (2**zoom) * (np.pi - np.log(np.tan(np.pi/4 + np.radians(latitude)/2)))
    return x, y

def pixel_to_coords(x,y,zoom=20):
    '''from pixel coordinates, returns longitude and latitude in degrees'''
    longitude = x / ((128/np.pi) * (2**zoom)) - np.pi
    latitude = 2 * np.arctan(np.exp(np.pi - y / (128 / np.pi*2**zoom))) - np.pi / 2
    return (np.degrees(longitude), np.degrees(latitude))

def bounds_coords(longitude, latitude, zoom=20, width=256, heigh=256):
    '''from longitude and latitude in degrees and zoom, returns left bottom and right top coords in pixel coordinates'''
    x = coords_to_pixel(longitude, latitude, zoom)[0]
    y = coords_to_pixel(longitude, latitude, zoom)[1]
    
    left = x - (width/2)
    right = x + (width/2)
    top = y - (heigh/2)
    bottom = y + (heigh/2)
    
    left_bottom_coords = pixel_to_coords(left, bottom, zoom)
    right_top_coords = pixel_to_coords(right, top, zoom)
    
    return [left_bottom_coords, right_top_coords]

def center_coords(longitude, latitude, zoom=20, width=256, heigh=256):
    '''from tile coords and zoom, returns center in degrees'''
    x = coords_to_pixel(longitude, latitude, zoom)[0]
    y = coords_to_pixel(longitude, latitude, zoom)[1]
    
    left = x - (width/2)
    right = x + (width/2)
    top = y - (heigh/2)
    bottom = y + (heigh/2)
    
    left_bottom_coords = pixel_to_coords(left, bottom, zoom)
    right_top_coords = pixel_to_coords(right, top, zoom)
    
    return [left_bottom_coords, right_top_coords]

def deg2num(lon_deg, lat_deg, zoom=20):
    '''from longitude and latitude in degrees and zoom, returns tile number'''
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return [xtile, ytile]

def num2deg(xtile, ytile, zoom=20):
    '''from tile number, returns its West-Nord coordinate. If input xtile+0.5 and ytile+0.5, returns its center'''
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return [lon_deg, lat_deg]


def nTiles(left_top_coord, right_bottom_coord):
    '''from coordinates, retrieves number of tiles each coord to be introduced as tuple as follows: (longitude, latitude)'''
    c1_tile = deg2num(left_top_coord[0], left_top_coord[1], zoom=20)
    c2_tile = deg2num(right_bottom_coord[0], right_bottom_coord[1], zoom=20)
    return ((c1_tile[0]-c2_tile[0])*(c1_tile[1]-c2_tile[1]))