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

def CabTypecolors(Cabdata):
    print(Cabdata)
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
    map = folium.Map(location = [mapdata['latitude'].mean(), mapdata['longitude'].mean()], zoom_start = 3)
    marker_cluster = MarkerCluster().add_to(map)

    for point in range(0, len(locationlist)):
        folium.Marker(
            locationlist[point], popup=mapdata['taxi_id'][point]+' '+mapdata['taxy_Type'][point],
            icon=folium.Icon(color=mapdata["color"][point], icon_color='white', icon='taxi', angle=0, prefix='fa')
            ).add_to(map)

    return folium_static(map)

def make_hashes(password):
	return shake_256(str.encode(password)).hexdigest(77)


def make_hashes_len(password, lenOfhash=int):
	return shake_256(str.encode(password)).hexdigest(lenOfhash)

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    
    return False

geolocator = Nominatim(user_agent="taxy_co")
class newTaxi :
    
    
      
    def __init__(self, name, email, number, taxy_Type, city):
        country = 'USA'
        
        self.name = name
        self.type = taxy_Type
        self.email = email 
        self.number = number
        
        self.newTaxiid = make_hashes_len((name+str(taxy_Type)+(city+ country)), 5)
        
        self.location = geolocator.geocode(city+','+ country)
        self.latitude = self.location.latitude
        self.longitude = self.location.longitude
        self.city = self.location.raw.get('display_name')
        
        
        
        self.Details = {
            
            'newTaxiDName' : self.name,
            'newTaxyDEmail' : self.email,
            'newTaxyDNumber': self.number,
            
            'newTaxyType' : self.type,
            'newTaxyId': self.newTaxiid,
            'newTaxyCity': self.city,

            'newUserPoint': self.location.point
            } 
    