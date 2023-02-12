import pymongo
import json, random, datetime, requests, time
from pymongo import  MongoClient
from hashlib import shake_256
import json, time, enum, requests, names, random, sys, threading
from geopy.geocoders import Nominatim
from geopy.distance import distance
from shapely.geometry import Point, Polygon
import sched
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu

from dotenv import load_dotenv, find_dotenv
import os, pprint
from pymongo import  MongoClient
from helper_functions import create_hash_dirs, taxi_search, get_nominatim_geocode,get_geocode,make_hashes, random_phone_num_generator , UserTypecolors, CabTypecolors

password =  os.environ.get("MONGODB_PWD")
geolocator = Nominatim(user_agent="taxy_co")
import pandas as pd
load_dotenv(find_dotenv())
connString = 'mongodb+srv://roy:foxyisfast@cluster0.s0fjifz.mongodb.net/?retryWrites=true&w=majority'

Mongo_client = MongoClient(connString)

Taxicodb =  Mongo_client.TaxiCo

UserData = Taxicodb.UserCollection
DriverData = Taxicodb.DriverCollection

import streamlit as st
import requests
User_df = {'Username':[],'Userlocation':[],'Usernumber':[],
                          'Useremail':[],'Usertype':[],'Usercity':[]}

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
            
            'newUserName' : self.name,
            'newUserEmail' : self.email,
            'newUserNumber': self.number,
            'newUserType' : self.type,
            'newUserId': self.newUserid,
            'newUser_City': self.city,
            'lat_point': self.latitude,
            'lon_point': self.longitude,
            'newUser_Point': self.point
           } 
                
def add_user_data(newUsertest):    
    UserCollection = Taxicodb.UserCollection

    UserData = ({
        'newUserName': newUsertest.name,
        'newUserEmail': newUsertest.email,
        'newUserNumber': newUsertest.number,
        'newUserType': newUsertest.type,
        'lat_point': newUsertest.latitude,
        'lon_point': newUsertest.longitude,
        'newUserId': newUsertest.newUserid
    })
    
    confirmationId = UserCollection.insert_one(UserData).inserted_id
    print(confirmationId)
    return confirmationId



def view_all_user():
    UserCollection = Taxicodb.UserCollection

    all_user =  list(UserCollection.find())
    UserCollection_df = pd.DataFrame().from_dict(all_user)#[6: :].drop(['name','type'], axis=1)


    UserCollection_df['UserTypeCats'] = UserCollection_df['newUserType'].factorize()[0]    
    UserCollection_df.rename(columns={'lat_point': "latitude", 'lon_point':'longitude'}, inplace=True)
    UserCollection_df["color"] = UserCollection_df.apply(UserTypecolors, axis=1)
    list_set_hashes, hashes =  create_hash_dirs(UserCollection_df)


    UserCollection_df['geohash'] = hashes
    hashes_check = UserCollection_df.geohash.to_list()
    return UserCollection_df, hashes_check, list_set_hashes

def edit_user_data(newUserName, newUserNumber, newUserType, newUserId):
    
    UserData = Taxicodb.UserCollection
    UserData.update_one(
        {"newUserId": newUserId},
        {"$set": {"newUserName": newUserName, "newUserNumber": newUserNumber, "newUserType": newUserType}}
    )
    
def delete_user_data(newUserId):
    
    UserData = Taxicodb.UserCollection
    UserData.delete_one({"newUserId": newUserId})

class newTaxi :
    
      
    def __init__(self, name, email, number, taxy_Type, city):
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
            'newTaxyPoint': self.point} 
        
def add_driver_data(driverobj):
    DriverCollection = Taxicodb.DriverCollection

    driver_data = {
        "driver_name": driverobj.name,
        "driver_email": driverobj.email,
        "driver_number": driverobj.number,
        "taxy_Type": driverobj.type,
        "lat_point": driverobj.latitude,
        "lon_point": driverobj.longitude,
        "taxy_id": driverobj.newTaxiid
    }
    
    
    confirmationId = DriverCollection.insert_one(driver_data).inserted_id
    print(confirmationId)
    return confirmationId


def view_all_driver():
    DriverCollection = Taxicodb.DriverCollection
    all_driversdf =  pd.DataFrame(list(DriverCollection.find()))
    
    all_driversdf['UserTypeCats'] = all_driversdf['taxy_Type'].factorize()[0]    
    all_driversdf.rename(columns={'lat_point': "latitude", 'lon_point':'longitude'}, inplace=True)
    all_driversdf["color"] = all_driversdf.apply(CabTypecolors, axis=1)
    list_set_hashes, hashes =  create_hash_dirs(all_driversdf)

    all_driversdf['geohash'] = hashes
    hashes_check = all_driversdf.geohash.to_list()
    
    return all_driversdf, hashes_check, list_set_hashes



def edit_driver_data(newDriverName, newDriverNumber, driver_email, taxy_id):
    
    DriverData = Taxicodb.DriverCollection
    DriverData.update_one(
        {"taxy_id": taxy_id},
        {"$set": {"driver_name": newDriverName, "driver_number": newDriverNumber,"driver_email": driver_email}}
    )
    
def delete_driver_data(taxy_id):
    
    DriverData = Taxicodb.DriverCollection
    DriverData.delete_one({"taxy_id": taxy_id})
            
# Set up page title and description
st.set_page_config(page_title="Taxi App", page_icon=":taxi:", layout="wide")

st.cache(suppress_st_warning=True)

def main(**state):
    DriverData = Taxicodb.DriverCollection
    UserCollection = Taxicodb.UserCollection


    menu = ["Customer", "Driver"]
    
    choice = option_menu(
        menu_title="Main Menu",
        options= menu,
        menu_icon = "cast",
        default_index = 0,
        orientation = "horizontal"
    )

    if choice == "Customer":
        
        UserCollection_df, hashes_check, list_set_hashes = view_all_user()
        CustomerMenu = ['Sign up', 'Log in']
        CustomerNav = st.selectbox("Choose From", options= CustomerMenu )
        if CustomerNav == "Log in":
            
            name = st.text_input("Name")
            email = st.text_input("Email")
            
            if st.button('Log into account'):
                st.dataframe(UserCollection_df[UserCollection_df['newUserName'] == name])
                st.dataframe(UserCollection_df[UserCollection_df['newUserEmail'] == email])
                     
        elif CustomerNav == "Sign up":

            name = st.text_input("Name")
            email = st.text_input("Email")
            number = st.text_input("Phone Number")
            city = st.text_input("City")
            Usertype = st.selectbox("Choose From", options=['FirstTime', 'Frequent', 'VipUser', 'NoAccount'])
            
            if st.button("Add User"):
                new_user = newUser(name, email, number, Usertype, city)
                inserted_id = add_user_data(new_user)
                st.success(f"User added {inserted_id}")
                
    if choice == "Driver":
        DriverCollection, hashes_check, list_set_hashes = view_all_driver()

        DriverMenu = ['Sign up', 'Log in']
        DriverrNav = st.selectbox("Choose From", options= DriverMenu )
        if DriverrNav == "Log in":
            name = st.text_input("Name")
            email = st.text_input("Email")
            number = st.text_input("Phone Number")
        
        elif DriverrNav == "Sign up":
                    
            name = st.text_input("Name")
            email = st.text_input("Email")
            number = st.text_input("Phone Number")
            city = st.text_input("City")

            TaxyType = st.selectbox("Choose From", options=['Utility', 'Deluxe', 'Luxury', 'RideShare'])

            if st.button('Add Driver'):
                newTaxiDriver = newTaxi(name, email, number, TaxyType, city)
                inserted_id = add_driver_data(newTaxiDriver)
                st.success(f"Driver added {inserted_id}")

        
main()