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
from helper_functions import create_hash_dirs, taxi_search, get_nominatim_geocode,get_geocode,make_hashes, random_phone_num_generator , UserTypecolors, CabTypecolors, make_map

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
    st.write(confirmationId)
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


geolocator = Nominatim(user_agent="taxy_co")

users_location = (37.973525940217456, -122.05614932511963)


def createInitialUser(users_location):
    User_df = {'Username':[],'Userlocation':[],'Usernumber':[],
                            'Useremail':[],'Usertype':[],'Usercity':[]}

    # Distance in meters
    distance_in_meters = 80
    lats = []
    lons = []

    for u in [35, 50, 55, 65, 75]:
        User_df['Userlocation'].append(distance(meters=distance_in_meters).destination(point=users_location, bearing=u))

    nOfD = 5 
    for i in range(nOfD):
        User_df['Username'].append(names.get_full_name())
        User_df['Useremail'].append(f'{names.get_full_name().replace(" ", "")}@gmail.com')
        User_df['Usernumber'].append(random_phone_num_generator())
        User_df['Usercity'].append(random.choice(['Concord CA', 'Walnut Creek CA', 'Pleasant Hill CA', 'Martinez CA']))
        User_df['Usertype'].append(random.choice(['FirstTime', 'Frequent', 'VipUser', 'NoAccount']))

    for i in range(nOfD):
        lats.append(User_df.get(['Userlocation'][0])[i][0])

    for i in range(nOfD):
        lons.append(User_df.get(['Userlocation'][0])[i][1])

    User_df['lats'] = lats
    User_df['lons'] = lons
        
    User_dfpd = pd.DataFrame().from_dict(User_df)

    for i in range(nOfD):
        newUsertest = newUser(User_dfpd.loc[i]['Username'],
                              User_dfpd.loc[i]['Useremail'],
                              number = User_dfpd.loc[i]['Usernumber'],
                              user_Type = User_dfpd.loc[i]['Usertype'],
                              city = User_dfpd.loc[i]['Usercity'])
        
        add_user_data(newUsertest)  
        
    return User_dfpd


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

taxi_location = (37.973525940217456, -122.05614932511963)

def createInitialDrivers(taxi_location):

    driver_df = {'newTaxiDName':[],'newTaxyPoint':[],'newTaxyDNumber':[],
                            'newTaxyDEmail':[],'newTaxyType':[],'newTaxyCity':[]}

    distance_in_mlies = 80

    lats = []
    lons = []

    nOfD = 13
    for m in [0, 1, 5, 10, 15, 20, 22, 25, 35, 50, 55, 65, 75]:
        driver_df["newTaxyPoint"].append(distance(miles=distance_in_mlies).destination(point=taxi_location, bearing=m))


    for i in range(nOfD):
        lats.append(driver_df.get(['newTaxyPoint'][0])[i][0])

    for i in range(nOfD):
        lons.append(driver_df.get(['newTaxyPoint'][0])[i][1])
        

    for i in range(nOfD):
        driver_df['newTaxiDName'].append(names.get_full_name())
        driver_df['newTaxyDEmail'].append(f'{names.get_full_name().replace(" ", "")}@gmail.com')
        driver_df['newTaxyDNumber'].append(random_phone_num_generator())
        driver_df['newTaxyCity'].append(random.choice(['Concord CA', 'Walnut Creek CA', 'Pleasant Hill CA', 'Martinez CA']))
        driver_df['newTaxyType'].append(random.choice(['Utility', 'Deluxe', 'Luxury', 'RideShare']))


    driver_df['lats'] = lats
    driver_df['lons'] = lons



    driver_dfpd = pd.DataFrame().from_dict(driver_df)


    for i in range(nOfD):
        newDriverTest = newTaxi(
            driver_dfpd.loc[i]['newTaxiDName'],
            driver_dfpd.loc[i]['newTaxyDEmail'],
            number = driver_dfpd.loc[i]['newTaxyDNumber'],
            taxy_Type = driver_dfpd.loc[i]['newTaxyType'],
            city = driver_dfpd.loc[i]['newTaxyCity'])
        

        add_driver_data(newDriverTest)  
    
    return driver_dfpd
            
            
            
# Set up page title and description
st.set_page_config(page_title="Taxi App", page_icon=":taxi:", layout="wide")

st.cache(suppress_st_warning=True)

def main(**state):
    
    DriverData = Taxicodb.DriverCollection
    UserCollection = Taxicodb.UserCollection


    menu = ['Log in', 'Sign up', 'Add Points']
    
    choice = option_menu(
        menu_title="Main Menu",
        options= menu,
        menu_icon = "cast",
        default_index = 0,
        orientation = "horizontal"
    )
    
    if choice == "Add Points":
        Pointsmenu = ['Driver', 'Rider']
        PointsNav = st.selectbox("Choose From", options= Pointsmenu)
        if PointsNav == "Rider":
            if st.checkbox('Add Users'):
                InitialUsers = createInitialUser(users_location)
                st.dataframe(InitialUsers)

        elif PointsNav == "Driver":
            if st.checkbox('Add Driver'):
                InitialDrivers = createInitialDrivers(taxi_location)
                st.dataframe(InitialDrivers)

    if choice == "Sign up":
        
        signupmenu = ['Driver', 'Subscriber']
        
        signupNav = st.selectbox("Choose From", options= signupmenu)
        
        if signupNav == "Driver":
            name = st.text_input("Name")
            email = st.text_input("Email")
            number = st.text_input("Phone Number")
            city = st.text_input("City")
            TaxyType = st.selectbox("Choose From", options=['Utility', 'Deluxe', 'Luxury', 'RideShare'])

            if st.button('Add Driver'):
                newTaxiDriver = newTaxi(name, email, number, TaxyType, city)
                inserted_id = add_driver_data(newTaxiDriver)
                st.success(f"Driver added {inserted_id}")
        
        elif signupNav == "Subscriber":
            name = st.text_input("Name")
            email = st.text_input("Email")
            number = st.text_input("Phone Number")
            city = st.text_input("City")
            Usertype = st.selectbox("Choose From", options=['FirstTime', 'Frequent', 'VipUser', 'NoAccount'])
            
            if st.button("Add Subscriber"):
                new_user = newUser(name, email, number, Usertype, city)
                inserted_id = add_user_data(new_user)
                st.success(f"Subscriber added {inserted_id}")
                
        
    elif choice == "Log in":
        UserCollection_df, hashes_check, list_set_hashes = view_all_user()
        DriverCollection, hashes_check, list_set_hashes = view_all_driver()
        
        Loginmenu = ['Sign in to drive', 'Sign in to ride']
        
        LoginNav = st.selectbox("Choose From", options= Loginmenu)
        
        if LoginNav == 'Sign in to ride':
            name = st.text_input("Name")
            email = st.text_input("Email")
        
            if st.checkbox('Enter Rider Accounr'):
                
                user_check = UserCollection_df[UserCollection_df['newUserName'] == name].values
                user_checkTwo = UserCollection_df[UserCollection_df['newUserEmail'] == email].values
                
                if len(user_check) != 0 and len(user_checkTwo) != 0:
                                        
                    oppslist = ['Utility', 'Deluxe', 'Luxury', 'RideShare']
                    TaxySelection = st.selectbox("Choose From", options=oppslist)
                    selected_drivers = DriverCollection[DriverCollection['taxy_Type'] == str(TaxySelection)]
                    selected_drivers_slice = selected_drivers[['driver_name', 'driver_email', 'driver_number', 'taxy_id', 'geohash']]
                    st.dataframe(selected_drivers_slice)
                    if st.checkbox('Find Nearest Taxi of this type'):
                        make_map(DriverCollection)

                        taxi_search(37.976852, -122.033562, hashes_check, 0.0008, selected_drivers_slice)
                                                   
                    # Map Of Drivers
                    
                else:  
                    st.warning('No good')

        elif LoginNav == 'Sign in to drive':
            
                        
            name = st.text_input("Name")
            Number = st.text_input("Number")
            
            if st.checkbox('Enter Driver Account'):
                
                driver_check = DriverCollection[DriverCollection['driver_name'] == name].values
                driver_checkTwo = DriverCollection[DriverCollection['driver_number'] == Number].values
                
                if len(driver_check) != 0 and len(driver_checkTwo) != 0:
                    
                    DriverCollection[DriverCollection['driver_number'] == Number]
                    
                else:
                    st.warning('No good')

                        
                
            
        
main()