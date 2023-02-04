#from cloud_tools import Subscriber
import boto3
from hashlib import shake_256
import json, time, enum, requests, names, random, sys, threading

from geopy.geocoders import Nominatim
from geopy.distance import distance
from shapely.geometry import Point, Polygon
import pandas as pd
from backendFunc import *

import sqlite3
conn = sqlite3.connect("Taxie_population.db")
c = conn.cursor()
DB_CONN = None
if  DB_CONN == False:
    conn.close()

#conn.close()
def create_driver_table():
    c.execute('CREATE TABLE IF NOT EXISTS TaxiData(driver_name TEXT, driver_email TEXT UNIQUE, driver_number NUMBER UNIQUE, taxy_Type TEXT, lat_point NUMBER,lon_point NUMBER ,taxy_id TEXT UNIQUE)')
    conn.commit()


def add_driver_data(driver_name,driver_email,driver_number,taxy_Type,lat_point,lon_point ,taxy_id):
    c.execute('INSERT INTO TaxiData(driver_name,driver_email,driver_number,taxy_Type,lat_point,lon_point, taxy_id) VALUES (?,?,?,?,?,?,?)',(driver_name,driver_email,driver_number,taxy_Type,lat_point,lon_point,taxy_id))
    conn.commit()

def view_all_taxi():
    c.execute('SELECT * FROM TaxiData')
    data = c.fetchall()
    return data


def edit_driver_data(driver_email,driver_number,taxy_Type):
	c.execute("UPDATE TaxiData SET driver_email =?,driver_number=?,taxy_Type=? WHERE taxy_id=?",(driver_email,driver_number,taxy_Type))
	conn.commit()
	data = c.fetchall()
	return data

def delete_taxy_data(taxy_id):
    c.execute('DELETE FROM TaxiData WHERE taxy_id="{}"'.format(taxy_id))


taxyType = enum.Enum('taxyType',
                  ['Utility', 'Deluxe', 'Luxury', 'RideShare'])

driver_df = {'Driver_name':[],'taxi_locations':[],'phone_num_generator':[],
                          'Driver_emails':[],'taxyType':[],'taxi_cities':[]}

geolocator = Nominatim(user_agent="taxy_co")

address = '1226 Monument Blvd Concord CA'; city ="Concord"; country ="USA"

locGen = geolocator.geocode(city+','+ country)

class newTaxi :
    
      
    def __init__(self, name, email, number, taxy_Type, city, country):
        country ="USA"

        
        self.name = name
        self.type = taxy_Type
        self.email = email 
        self.number = number
        self.city = city
        
        
        self.newTaxiid = make_hashes((self.name+str(self.type)+(self.city+ country)))
        
        self.location = geolocator.geocode(self.city+','+ country)
        self.latitude = self.location.latitude
        self.longitude = self.location.longitude
        self.point = self.location.raw.get('display_name')
        
        
        
        self.Details = {
            
            'newTaxiDName' : self.name,
            'newTaxyDEmail' : self.email,
            'newTaxyDNumber': self.number,
            
            'newTaxyType' : self.type,
            'newTaxyId': self.newTaxiid,
            'newTaxyCity': self.city,
            'newUserPoint': self.point
            } 



def createDrivers(nOfD = int):    
    create_driver_table()

    geolocator = Nominatim(user_agent="taxy_co")

    address = '1226 Monument Blvd Concord CA'; city ="Concord"; country ="USA"

    locGen = geolocator.geocode(city+','+ country)

    taxi_location = (37.973525940217456, -122.05614932511963)

    distance_in_meters = 80

    lats = []
    lons = []
    
    for m in [0, 1, 5, 10, 15, 20, 22, 25, 35, 50, 55, 65, 75]:
        driver_df["taxi_locations"].append(distance(meters=distance_in_meters).destination(point=taxi_location, bearing=m))


    for i in range(nOfD):
        driver_df['Driver_name'].append(names.get_full_name())
        driver_df['Driver_emails'].append(f'{names.get_full_name().replace(" ", "")}@gmail.com')
        driver_df['phone_num_generator'].append(random_phone_num_generator())
        driver_df['taxi_cities'].append(random.choice(['Concord CA', 'Walnut Creek CA', 'Pleasant Hill CA', 'Martinez CA']))
        driver_df['taxyType'].append(random.choice(['Utility', 'Deluxe', 'Luxury', 'RideShare']))

    for i in range(nOfD):
            lats.append(driver_df.get(['taxi_locations'][0])[i][0])
    for i in range(nOfD):
        lons.append(driver_df.get(['taxi_locations'][0])[i][1])

    driver_df['lats'] = lats
    driver_df['lons'] = lons
    
    driver_dfpd = pd.DataFrame().from_dict(driver_df)

        

    for i in range(nOfD):
        newDriverTest = newTaxi(
            driver_dfpd.loc[i]['Driver_name'],
            driver_dfpd.loc[i]['Driver_emails'],
            number = driver_dfpd.loc[i]['phone_num_generator'],
            taxy_Type = driver_dfpd.loc[i]['taxyType'],
            city = driver_dfpd.loc[i]['taxi_cities'],
            country= 'USA')


        newTaxiDName = newDriverTest.Details.get('newTaxiDName')
        newTaxyDEmail = newDriverTest.Details.get('newTaxyDEmail')
        latitude = newDriverTest.latitude
        longitude = newDriverTest.longitude
        newTaxyDNumber = newDriverTest.Details.get('newTaxyDNumber')
        newTaxyType = newDriverTest.Details.get('newTaxyType')
        newTaxyId = newDriverTest.Details.get('newTaxyId')
        newTaxyCity = newDriverTest.Details.get('newTaxyCity')
        newTaxyId = newDriverTest.Details.get('newTaxyId')

        newTaxiDName = newDriverTest.Details.get('newTaxiDName')
        newUserPoint = newDriverTest.Details.get('newUserPoint')


        add_driver_data(newTaxiDName, newTaxyDEmail, 
                driver_number = newTaxyDNumber,  taxy_Type = newTaxyType,
                taxy_id = newTaxyId, lat_point=latitude, lon_point=longitude)  
        
    return driver_dfpd