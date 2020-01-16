# pool-track

## 1. Why pool-track

Tax authorities and other administrations have been using drones to detect swimming pools in order to detect fraud, ilegal constructions and other annomalies. As drones requiere a considerable amount of time, investment and permissions, I tried to develop an alternative solution using satellite images, OpenCV (an artificial vision library) and Python.

## 2. Folders and main files in root

`api.py` contains the code for the API, which takes coordinates and executes an analysis of the area, showing the swimming pools found up to that moment

`src` contains all relevant functions in Python to connect to MongoDB, convert longitudes and latitudes into Web Mercator projections and the algorithms to detect and visualize swimming pools

`templates` includes the relevant front end html files

`static` the javascript and 

## 3. Logic behind

The workflow of the program is as follows.

1. Introduce top-left and right-bottom coordinates of a rectangle in a map. The program will scan this rectangle.

2. The program will calculate which tiles are within this coordinates and the center of each tile. To do so, it uses functions that convert latitude and longitude into Web Mercator projection coordinates.

    For each center, a request will be launched to Google Maps API, getting a squared image corresponding to each tile. To avoid double-spending in Goole API requests, a MongoDB atlas database is consulted, as it registers all request effectively made.

3. When images are downloaded, another function masks images and locates swimming pools by looking at the blue color HSV range. With the help of NumPy, determines if a photo contains a swimming pool by checking the average values of the pixels both in the whole image and in a 4x4 subdivision.

4. Once the processing images is ready, the coordinates of the swimming pools are uploaded to MongoDB Atlas, and a Folium map with a cluster visualization is updated to show the location of the found swimming pools.
