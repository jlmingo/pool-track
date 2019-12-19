import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob
from src.geofunctions import num2deg
from src.connect_mongodb import connect
import json
import os

def img_to_pool(preprocessed_image):
    img = cv2.imread(preprocessed_image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    l_blue = np.array([75,110,80])
    d_blue = np.array([100,255,255])
    mask = cv2.inRange(hsv_img, l_blue, d_blue)
    result = cv2.bitwise_and(img, img, mask=mask)
    return result

def is_pool(processed_image, path, tile, filename):
    grid = np.empty((4,4))
    print(np.mean(processed_image))
    print(path)
    for i in range(4):
        for j in range(4):
            grid[i,j] = np.mean(processed_image[64*i:64*i+64, 64*j:64*j+64])
    max_index = np.where(grid == np.amax(grid))
    max_index = np.resize(np.stack(max_index), (1,2))
    max_value = np.amax(grid)
    print(max_index)
    max_value_position = ((max_index[0,0]+1-0.5)/4, (max_index[0,1]+1-0.5)/4)
    tile_pool = [tile[0]+max_value_position[0], tile[1]+max_value_position[1]]
    coordinates = num2deg(tile_pool[0], tile_pool[1])
    detected_pool = {
        "Tile": tile,
        "Location": {
            "type": "Point",
            "cordinates": [coordinates[0], coordinates[1]]
        },
        "File_name": filename,
        "Google_link": f"https://www.google.es/maps/@{coordinates[1]},{coordinates[0]},53m/data=!3m1!1e3?hl=es"
    }
    return detected_pool if (np.mean(processed_image)>3 and max_value>20) else None

def poolDetect(path):
    database, coll = connect("datamad1019", "swimming-pools")
    images = glob.glob(path+"*.png")
    metadata = glob.glob(path+"*.txt")
    detected_pools = []
    for f in metadata:
        with open(f) as json_file:
            data = json.load(json_file)
        result = img_to_pool(os.path.join(path,data["name_file"]))
        if (is_pool(result, f, data["tile"], data["name_file"])):
            detected_pools.append(is_pool(result, f, data["tile"], data["name_file"]))
    tile_un = []
    tiles_in_coll = list(coll.find({}, {"Tile": 1, "_id":0}))
    for e in tiles_in_coll:
        tile_un.append(e["Tile"])
    for pool in detected_pools:
        if pool["Tile"] not in tile_un:
            coll.insert_one(pool)
    return detected_pools