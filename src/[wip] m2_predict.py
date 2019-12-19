import glob
import json
from connect_mongodb import connect
from pre-process-img import poolDetect

def main():
    database, coll = connect("datamad1019", "already_analyzed")
    metadata = glob.glob("../output/*.txt")
    
    tile_un = []
    for e in list(coll.find({}, {"tile": 1, "_id":0})):
        tile_un.append(e["tile"])
    
    images = []
    for m in metadata:
        with open(m) as json_file:
            data = json.load(json_file)
            if data["tile"] not in tile_un:
                images.append(data["name_file"])
    
    poolDetect()

if __name__ = "__main__":
    main()