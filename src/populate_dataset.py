import geopandas as gpd
import requests
import os 
from dotenv import load_dotenv
import urllib
import urllib.request
import pandas as pd
from src.popfunctions import downloader

def main():
    #Reading geodataframe with Swimming Pools in Washington
    gdf = gpd.read_file("./input-ignore/Swimming_Pools_2015/Swimming_Pools_2015.shp")
    gdf['centroid'] = gdf['geometry'].centroid

    #Loading token for using in Google API
    load_dotenv()
    key = 'GOOGLETOKEN'
    value = os.getenv(key)

    for index, row in gdf.iterrows():
        y_coord= row.centroid.y #laatitude
        x_coord = row.centroid.x #longitude
        url = f"https://maps.googleapis.com/maps/api/staticmap?center={y_coord},{x_coord}&zoom=20&size=400x400&maptype=satellite&key={value}"
        downloader(url, index, "pool-")

    gdf["centroid_export"] = gdf.centroid.apply(lambda row: (row.x, row.y))
    df1 = pd.DataFrame(gdf.centroid_export)
    df1.to_csv("./output/centroids.csv")

if __name__ == "__main__":
    main()