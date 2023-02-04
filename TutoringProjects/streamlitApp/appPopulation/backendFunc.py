import requests, enum
import urllib.parse
from geopy.geocoders import Nominatim
from hashlib import shake_256
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import folium.plugins
folium.plugins.MarkerCluster()

from logging import Logger
import random

def UserTypecolors(userdata):
    if userdata['UserType'] == 'VipUser':
        return 'yellow'
    elif userdata['UserType'] == 'Frequent':
        return 'blue'
    elif userdata['UserType'] == 'FirstTime':
        return 'purple'
    elif userdata['UserType'] == 'NoAccount':
        return 'gray'
    
def CabTypecolors(Cabdata):
    if Cabdata['taxyType'] == 'RideShare':
        return 'green'
    elif Cabdata['taxyType'] == 'Utility':
        return 'orange'
    elif Cabdata['taxyType'] == 'Deluxe':
        return 'red'
    elif Cabdata['taxyType'] == 'Luxury':
        return 'aquamarine'    
    
    
def show_user(mapdata):
    locations = mapdata[['latitude', 'longitude']]
    locationlist = locations.values.tolist()
    map = folium.Map(location = [mapdata['latitude'].mean(), mapdata['longitude'].mean()], zoom_start = 3)

    marker_cluster = MarkerCluster().add_to(map)

    for point in range(0, len(locationlist)):
        
        folium.Marker(
            locationlist[point],
            popup=mapdata['User_name'][point]+' '+mapdata['UserType'][point]+' '+mapdata['User_cities'][point],
            
            icon=folium.Icon(color=mapdata["color"][point], icon_color='white', icon='cab', angle=0, prefix='fa')
            ).add_to(map)
        
    map

    return map #return folium_static(map)

def make_map(mapdata):
    locations = mapdata[['latitude', 'longitude']]
    locationlist = locations.values.tolist()
    map = folium.Map(location = [mapdata['latitude'].mean(), mapdata['longitude'].mean()], zoom_start = 3)

    marker_cluster = MarkerCluster().add_to(map)

    for point in range(0, len(locationlist)):
        
        folium.Marker(
            locationlist[point],
            popup=mapdata['Driver_name'][point]+' '+mapdata['taxyType'][point]+' '+mapdata['taxi_cities'][point],
            
            icon=folium.Icon(color=mapdata["color"][point], icon_color='white', icon='cab', angle=0, prefix='fa')
            ).add_to(map)
        
    map

    return map #return folium_static(map)


def random_phone_num_generator():
    first = str(random.randint(100, 999))
    second = str(random.randint(1, 888)).zfill(3)

    last = (str(random.randint(1, 9998)).zfill(4))
    while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
        last = (str(random.randint(1, 9998)).zfill(4))

    return '{}-{}-{}'.format(first, second, last)

def make_hashes(password):
	return shake_256(str.encode(password)).hexdigest(7)

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    
    return False



