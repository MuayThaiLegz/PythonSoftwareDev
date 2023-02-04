#from cloud_tools import Subscriber
import boto3
from hashlib import shake_256
import json, time, enum, requests, names, random, sys, threading
from backendFunc import *
from geopy.geocoders import Nominatim
from geopy.distance import distance
from shapely.geometry import Point, Polygon
import pandas as pd

import sqlite3
conn = sqlite3.connect("users_population.db")
c = conn.cursor()
DB_CONN = None

if  DB_CONN == False:
    conn.close()

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



User_Type = enum.Enum('User_Type',
                  ['FirstTime', 'Frequent', 'VipUser', 'NoAccount'])

        
User_df = {'User_name':[],'User_locations':[],'User_num_generator':[],
                          'User_emails':[],'UserType':[],'User_cities':[]}

geolocator = Nominatim(user_agent="taxy_co")

class newUser :
          
    def __init__(self, name, email, number, user_Type, city):
        country='USA'
                 
        self.name = name
        self.type = user_Type
        self.email = email 
        self.number = number
        self.city = city
        
        self.newUserid = make_hashes((self.name+str( self.type)+(self.city+ country)))
        
        self.location = geolocator.geocode(self.city+','+ country)
        self.latitude = self.location.latitude
        self.longitude = self.location.longitude
        self.point = self.location.raw.get('display_name')
        

        
        self.Details = {
            
            'newUser_Name' : self.name,
            'newUser_Email' : self.email,
            'newUser_Number': self.number,
            'newUser_Type' : self.type,
            'newUser_Id': self.newUserid,
            'newUser_City': self.city,
            'newUser_Point': self.point
           } 
        
 
def createUses(nOfD = int):
    create_user_table()    
    geolocator = Nominatim(user_agent="taxy_co")

    
    users_location = (37.973525940217456, -122.05614932511963)

    # Distance in meters
    distance_in_meters = 80
    lats = []
    lons = []


    for u in [0, 1, 5, 10, 15, 20, 22, 25, 35, 50, 55, 65, 75]:
        User_df['User_locations'].append(distance(meters=distance_in_meters).destination(point=users_location, bearing=u))

        
    for i in range(nOfD):
        User_df['User_name'].append(names.get_full_name())
        User_df['User_emails'].append(f'{names.get_full_name().replace(" ", "")}@gmail.com')
        User_df['User_num_generator'].append(random_phone_num_generator())
        User_df['User_cities'].append(random.choice(['Concord CA', 'Walnut Creek CA', 'Pleasant Hill CA', 'Martinez CA']))
        User_df['UserType'].append(random.choice(['FirstTime', 'Frequent', 'VipUser', 'NoAccount']))



    for i in range(nOfD):
        lats.append(User_df.get(['User_locations'][0])[i][0])

    for i in range(nOfD):
        lons.append(User_df.get(['User_locations'][0])[i][1])

    User_df['lats'] = lats
    User_df['lons'] = lons
        
    User_dfpd = pd.DataFrame().from_dict(User_df)

    for i in range(nOfD):
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
    return User_dfpd