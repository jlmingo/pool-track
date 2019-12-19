from flask import Flask, render_template, request
import os
from src.m3_representation import update_map
from src.popfunctions import tiles_lister, download_tiles
from src.geofunctions import nTiles
from src.pre_process_img import poolDetect

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        c1 = request.form["top-l-coord"]
        c1 = [float(e) for e in c1.split(",")]
        c2 = request.form["bottom-r-coord"]
        c2 = [float(e) for e in c2.split(",")]
        print(c1,c2)
        submission=True
        n_tiles_analized = nTiles(c1, c2)
        gdf = tiles_lister(c1, c2)
        download_tiles(gdf)
        pools = poolDetect("./output/")
        n_pools = len(pools)
        update_map()
        iframe = "map.html"
        message = f"We found {n_pools} new pools looking in {n_tiles_analized} tiles! Check them out in the next section"
        return render_template('index-copy.html', iframe=iframe, message=message, submission=submission)
    
    else:
        iframe = 'map.html'
        message = None
        submission=False
        return render_template('index-copy.html', message=message, iframe=iframe, submission=submission)

@app.route('/map.html')
def map():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=False)