import folium
from folium import Marker
from folium.plugins import MarkerCluster
import math
from src.connect_mongodb import connect
import pandas as pd

def embed_map(m, file_name):
    from IPython.display import IFrame
    m.save(file_name)
    return IFrame(file_name, width='100%', height='500px')

def update_map():

    m_1 = folium.Map(location=[40.415157, -3.689048], tiles='openstreetmap', zoom_start=10)

    y, x = connect("datamad1019", "swimming-pools")

    aggResult = x.find({})
    df2 = pd.DataFrame(list(aggResult))
    df2.head()

    mc = MarkerCluster()
    for idx, row in df2.iterrows():
        if not math.isnan(row['Location']["cordinates"][1]) and not math.isnan(row['Location']["cordinates"][0]):
            link =  '<a href='+f'{row["Google_link"]}'+'target="_blank">'+'Satellite View'+'</a>'
            mc.add_child(Marker([row['Location']["cordinates"][1], row['Location']["cordinates"][0]], popup=folium.Popup(link)))
    m_1.add_child(mc)

    embed_map(m_1, "./templates/map.html")

    return m_1