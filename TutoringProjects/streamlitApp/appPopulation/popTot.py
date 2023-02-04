#from cloud_tools import Subscriber
import boto3
from hashlib import shake_256
import json, time, enum, requests, names, random, sys, threading
from backendFunc import *
from geopy.geocoders import Nominatim
from geopy.distance import distance
from shapely.geometry import Point, Polygon
from backendFunc import *
import pandas as pd

import sqlite3
conn = sqlite3.connect("users_population.db")
c = conn.cursor()
#conn.close()

def make_hashes_len(password, lenOfhash=int):
    	return shake_256(str.encode(password)).hexdigest(lenOfhash)

def create_user_table():
    c.execute('CREATE TABLE IF NOT EXISTS UserData(newUserName TEXT, newUserEmail TEXT UNIQUE, newUserNumber NUMBER UNIQUE, newUserType TEXT, lat_point NUMBER,lon_point NUMBER ,newUserId TEXT UNIQUE)')
    conn.commit()
    
def add_user_data(newUserName,newUserEmail, newUserNumber,newUserType ,lat_point,lon_point ,newUserId):
    c.execute('INSERT INTO UserData(newUserName,newUserEmail, newUserNumber,newUserType ,lat_point,lon_point ,newUserId) VALUES (?,?,?,?,?,?,?)',(newUserName,newUserEmail, newUserNumber,newUserType ,lat_point,lon_point ,newUserId))
    conn.commit()

def view_all_user():
    c.execute('SELECT * FROM UserData')
    data = c.fetchall()
    return data

def edit_user_data(newUserEmail,newUserNumber,newUserType):
    c.execute("UPDATE UserData SET newUserEmail =?,newUserNumber=?,newUserType=? WHERE newUserId=?",(newUserEmail,newUserNumber,newUserType))
    conn.commit()
    data = c.fetchall()
    return data

def delete_user_data(user_id):
    c.execute('DELETE FROM UserData WHERE user_id="{}"'.format(user_id))


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

driver_df = {'Driver_name':[],'taxi_locations':[],'phone_num_generator':[],
                          'Driver_emails':[],'taxyType':[],'taxi_cities':[]}

User_df = {'User_name':[],'User_locations':[],'User_num_generator':[],
                          'User_emails':[],'UserType':[],'User_cities':[]}

def createUses():    
    
    create_user_table(); geolocator = Nominatim(user_agent="taxy_co")
    users_location = (3.7387, 12.3555)
    # Distance in meters
    distance_in_meters = 50
    lats = []
    lons = []

    for u in [3, 5, 10, 15, 20, 22, 25, 30, 35, 40]:
        User_df['User_locations'].append(distance(meters=distance_in_meters).destination(point=users_location, bearing=u))

    for i in range(10):
        User_df['User_name'].append(names.get_full_name())
        User_df['User_emails'].append(f'{names.get_full_name().replace(" ", "")}@gmail.com')
        User_df['User_num_generator'].append(random_phone_num_generator())
        User_df['User_cities'].append(random.choice(['Concord CA', 'Walnut Creek CA', 'Pleasant Hill CA', 'Martinez CA']))
        User_df['UserType'].append(random.choice(['FirstTime', 'Frequent', 'VipUser', 'NoAccount']))

    for i in range(10):
        lats.append(User_df.get(['User_locations'][0])[i][0])

    for i in range(10):
        lons.append(User_df.get(['User_locations'][0])[i][1])
        
    User_df['lats'] = lats
    User_df['lons'] = lons
        
    User_dfpd = pd.DataFrame().from_dict(User_df)

    for i in range(10):
        newUsertest = newUser(
            User_dfpd.loc[i]['User_name'],
            User_dfpd.loc[i]['User_emails'],
            number = User_dfpd.loc[i]['User_num_generator'],
            user_Type = User_dfpd.loc[i]['UserType'],
            city = User_dfpd.loc[i]['User_cities']
            )

        newUser_Name = newUsertest.Details.get('newUser_Name')
        newUser_Email = newUsertest.Details.get('newUser_Email')
        latitude = newUsertest.latitude
        longitude = newUsertest.longitude
        newUser_Number = newUsertest.Details.get('newUser_Number')
        newUser_Type = newUsertest.Details.get('newUser_Type')
        newUserId = newUsertest.Details.get('newUser_Id')
        newUser_City = newUsertest.Details.get('newUser_City')
        
        newUser_Point = newUsertest.Details.get('newUser_Point')


        add_user_data(newUser_Name, newUser_Email, 
                newUserNumber = newUser_Number,  newUserType = newUser_Type,
                lat_point=latitude, lon_point=longitude, newUserId = newUserId)  

driver_df = {'Driver_name':[],'taxi_locations':[],'phone_num_generator':[],
                          'Driver_emails':[],'taxyType':[],'taxi_cities':[]}

            
def createDrivers():    
    
    driver_df = {'Driver_name':[],'taxi_locations':[],'phone_num_generator':[],
                          'Driver_emails':[],'taxyType':[],'taxi_cities':[]}

    User_df = {'User_name':[],'User_locations':[],'User_num_generator':[],
                          'User_emails':[],'UserType':[],'User_cities':[]}
    create_driver_table()

    geolocator = Nominatim(user_agent="taxy_co")

    address = '1226 Monument Blvd Concord CA'; city ="Concord"; country ="USA"

    locGen = geolocator.geocode(city+','+ country)

    taxi_location = (37.7387, 121.3555)

    distance_in_meters = 50

    lats = []
    lons = []


    for m in [0, 1, 5, 10, 15, 20, 22, 25, 35, 50]:
        driver_df["taxi_locations"].append(distance(meters=distance_in_meters).destination(point=taxi_location, bearing=m))


    for i in range(10):
        driver_df['Driver_name'].append(names.get_full_name())
        driver_df['Driver_emails'].append(f'{names.get_full_name().replace(" ", "")}@gmail.com')
        driver_df['phone_num_generator'].append(random_phone_num_generator())
        driver_df['taxi_cities'].append(random.choice(['Concord CA', 'Walnut Creek CA', 'Pleasant Hill CA', 'Martinez CA']))
        driver_df['taxyType'].append(random.choice(['Utility', 'Deluxe', 'Luxury', 'RideShare']))




    for i in range(10):
        lats.append(driver_df.get(['taxi_locations'][0])[i][0])
    for i in range(10):
        lons.append(driver_df.get(['taxi_locations'][0])[i][1])

    driver_df['lats'] = lats
    driver_df['lons'] = lons

    driver_dfpd = pd.DataFrame().from_dict(driver_df)

        

    for i in range(10):
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
