import pygeohash
from pathlib import Path

import gzip
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
import os
import sys
import gzip
import json
from pathlib import Path
import csv
import pygeohash
import pymongo
import json, random, datetime, requests, time
from pymongo import  MongoClient
from hashlib import shake_256
import json, time, enum, requests, names, random, sys, threading
from geopy.geocoders import Nominatim
from geopy.distance import distance
from shapely.geometry import Point, Polygon
import sched
from dotenv import load_dotenv, find_dotenv
import os, pprint
from pymongo import  MongoClient
import numpy as np
import pandas as pd
geolocator = Nominatim(user_agent="taxy_co")

import streamlit as st
def create_hash_dirs(records):
    
    current_dir = Path(os.getcwd()).absolute()
    results_dir = current_dir.joinpath('results')
    results_dir.mkdir(parents=True, exist_ok=True)
    
    geoindex_dir = results_dir.joinpath('geoindex')
    
    geoindex_dir.mkdir(exist_ok=True, parents=True)
    
    hashes = []
    recs=len
    for i in range(len(records)):
        
        latitude = records.iloc[i]['latitude']
        
        longitude = records.iloc[i]['longitude']
        
        if latitude and longitude:
            
            encoded_lat_long = pygeohash.encode(latitude,longitude)
            
            hashes.append(encoded_lat_long)
                        
    hashes.sort()
            
    three_letter = sorted(list(set([entry[:3] for entry in hashes])))
    hash_index = {value: [] for value in three_letter}
    
    for key, values in hash_index.items():
        output_dir = geoindex_dir.joinpath(str(key[:1])).joinpath(str(key[:2]))
        output_dir.mkdir(exist_ok=True, parents=True)
        output_path = output_dir.joinpath('{}.jsonl.gz'.format(key))
        with gzip.open(output_path, 'w') as f:
            json_output = '\n'.join([json.dumps(value) for value in values])
            f.write(json_output.encode('utf-8'))
            
    return list(set(hashes)), hashes


def taxi_search(lat, lon, hashes_to_check, distance_in_km, df):
    distance_list = []
    closest_distance_list = []

    
    distance_in_m = distance_in_km*1000
    cord_hash = pygeohash.encode(lat, lon)    
    counter = 0
    for hash_ in hashes_to_check:        
        distance_list.append(pygeohash.geohash_approximate_distance(cord_hash,hash_))
        if pygeohash.geohash_approximate_distance(cord_hash,hash_) == min(distance_list):
            closest_hash = hash_
            closest_distance = pygeohash.geohash_approximate_distance(cord_hash,hash_)
            closest_distance_list.append(closest_distance)
    if min(distance_list) <= distance_in_m:
        
        for i in range(0, len(df)):
              
            if closest_hash == df['geohash'].iloc[i]:
                st.write('The closest is', df['driver_name'].iloc[i], 'at a distance of', closest_distance, 'miles.')
                counter += 1
            if counter >=1:
                break
    else:        
        print("No found in the distance specified.")
        
    return distance_list, closest_distance_list

def get_nominatim_geocode(address):
    try:
      location = geolocator.geocode(address)
      return location.raw['lat'], location.raw['lon']
    except Exception as e:
        return None, None
    
    
def get_geocode(address):
  lat,long = get_nominatim_geocode(address)
  return float(lat),float(long)

def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))


def make_hashes(password):
    	return shake_256(str.encode(password)).hexdigest(8)

def random_phone_num_generator():
  first = str(random.randint(100, 999))
  second = str(random.randint(1, 888)).zfill(3)

  last = (str(random.randint(1, 9998)).zfill(4))
  while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
    last = (str(random.randint(1, 9998)).zfill(4))

  return '{}-{}-{}'.format(first, second, last)


def UserTypecolors(userdata):
    if userdata['newUserType'] == 'VipUser':
        return 'yellow'
    elif userdata['newUserType'] == 'Frequent':
        return 'blue'
    elif userdata['newUserType'] == 'FirstTime':
        return 'purple'
    elif userdata['newUserType'] == 'NoAccount':
        return 'gray'
      
      
def CabTypecolors(Cabdata):
    if Cabdata['taxy_Type'] == 'RideShare':
        return 'green'
    elif Cabdata['taxy_Type'] == 'Utility':
        return 'orange'
    elif Cabdata['taxy_Type'] == 'Deluxe':
        return 'red'
    elif Cabdata['taxy_Type'] == 'Luxury':
        return 'aquamarine'    
    
def make_map(mapdata):
    locations = mapdata[['latitude', 'longitude']]
    locationlist = locations.values.tolist()
    map = folium.Map(location = [mapdata['latitude'].mean(), mapdata['longitude'].mean()], zoom_start = 12)

    marker_cluster = MarkerCluster().add_to(map)

    for point in range(len(mapdata['driver_name'])):
        
        folium.Marker(
            locationlist[point],
            popup=mapdata['driver_name'][point]+' '+mapdata['taxy_id'][point]+' '+mapdata['driver_number'][point],
            
            icon=folium.Icon(color=mapdata["color"][point], icon_color='white', icon='cab', angle=0, prefix='fa')
            ).add_to(map)
        
    marker_cluster

    return folium_static(map)


