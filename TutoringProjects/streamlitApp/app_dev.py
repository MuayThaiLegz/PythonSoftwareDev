import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu
#from db_functions import * 
import plotly.express as px 


import plotly.graph_objs as go        
        
import threading

#import util
import sys
#import yaml
#from cloud_tools import Subscriber
import boto3
from hashlib import sha256, shake_256
import hashlib, json, time, enum 

import AWSIoTPythonSDK

import botocore

from AWSIoTPythonSDK import MQTTLib
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import folium.plugins
folium.plugins.MarkerCluster()
import os
import gzip
from pathlib import Path
import csv
import s3fs
import pyarrow as pa
from pyarrow.json import read_json
import pyarrow.parquet as pq
import pygeohash
import jsonschema
from jsonschema.exceptions import ValidationError
from backendFunc import newTaxi,newUser ,CabTypecolors, make_map, get_geocode, get_nominatim_geocode
from logging import Logger
import requests, enum
import urllib.parse
from geopy.geocoders import Nominatim

def make_hashes_len(password, lenOfhash=int):
    	return shake_256(str.encode(password)).hexdigest(lenOfhash)
 
def create_driver_table():
    c.execute('CREATE TABLE IF NOT EXISTS TaxiData(driver_name TEXT, driver_email TEXT UNIQUE, driver_number NUMBER UNIQUE, taxy_Type TEXT, lat_point NUMBER,lon_point NUMBER ,taxy_id TEXT UNIQUE)')
    conn.commit()


def create_user_table():
    c.execute('CREATE TABLE IF NOT EXISTS UserData(newUserName TEXT, newUserEmail TEXT UNIQUE, newUserNumber NUMBER UNIQUE, newUserType TEXT, lat_point NUMBER,lon_point NUMBER ,newUserId TEXT UNIQUE)')
    conn.commit()


def add_driver_data(driver_name,driver_email,driver_number,taxy_Type,lat_point,lon_point ,taxy_id):
    c.execute('INSERT INTO TaxiData(driver_name,driver_email,driver_number,taxy_Type,lat_point,lon_point, taxy_id) VALUES (?,?,?,?,?,?,?)',(driver_name,driver_email,driver_number,taxy_Type,lat_point,lon_point,taxy_id))
    conn.commit()
    
def add_user_data(newUserName,newUserEmail, newUserNumber,newUserType ,lat_point,lon_point ,newUserId):
    c.execute('INSERT INTO UserData(newUserName,newUserEmail, newUserNumber,newUserType ,lat_point,lon_point ,newUserId) VALUES (?,?,?,?,?,?,?)',(newUserName,newUserEmail, newUserNumber,newUserType ,lat_point,lon_point ,newUserId))
    conn.commit()


def view_all_taxi():
    c.execute('SELECT * FROM TaxiData')
    data = c.fetchall()
    return data

def view_all_user():
    c.execute('SELECT * FROM UserData')
    data = c.fetchall()
    return data


def edit_driver_data(driver_email,driver_number,taxy_Type):
	c.execute("UPDATE TaxiData SET driver_email =?,driver_number=?,taxy_Type=? WHERE taxy_id=?",(driver_email,driver_number,taxy_Type))
	conn.commit()
	data = c.fetchall()
	return data

def edit_user_data(newUserEmail,newUserNumber,newUserType):
	c.execute("UPDATE UserData SET newUserEmail =?,newUserNumber=?,newUserType=? WHERE newUserId=?",(newUserEmail,newUserNumber,newUserType))
	conn.commit()
	data = c.fetchall()
	return data


def delete_taxy_data(taxy_id):
    c.execute('DELETE FROM TaxiData WHERE taxy_id="{}"'.format(taxy_id))
    
def delete_user_data(user_id):
    c.execute('DELETE FROM UserData WHERE user_id="{}"'.format(user_id))
    
    
from shapely import Point
from shapely.geometry import Polygon, CAP_STYLE
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

st.set_page_config(page_title="Taxi-Co Dashboard", page_icon=":taxi:", layout="wide")


import sqlite3
conn = sqlite3.connect("Taxy_coo.db")
c = conn.cursor()
#conn.close()

st.cache(suppress_st_warning=True)

def main(**state):
    
# ---- READ EXCEL ----

# Thoughts to consider:

# MAIN PAGE

# Collecting the User's Information on the Inflow/Outflow/Loans page

    menu = ['SignUp','UpdateAct']
    
    choice = option_menu(
        menu_title="Main Menu",
        options= menu,
        menu_icon = "cast",
        default_index = 0,
        orientation = "horizontal"
    )
    create_driver_table(); create_user_table();#create_bank_table()

    result = view_all_taxi()   
    clean_df = pd.DataFrame(result,columns=["driver_name", "driver_email","driver_number","taxy_Type", "lat_point","lon_point", "taxy_id"])
    #service_area = Polygon([(37.8287, -122.3555), (37.8044, 122.2712), (37.3387, 121.8853), (37.9780, 122.0311), (37.9101, 122.0652), (37.6688, 122.0810)])

    if choice == 'SignUp':
        country ="USA"
        
        Driver_opps = ['GivaRide', 'GetaRide'] # and?
        Driver_opps = st.sidebar.selectbox("Select: ", options=Driver_opps)
        
        if Driver_opps == "GivaRide":
            
            
            country ="USA"            
            name = st.sidebar.text_input("Add name")
            city = st.sidebar.text_input("Add city")
            email = st.sidebar.text_input("Add email")
            number = st.sidebar.text_input("Add number")
            taxy_Type = st.sidebar.selectbox("Taxy Category:",
                                        options=['Utility', 'Deluxe', 'Luxury', 'RideShare'])
            
            newTaxytest = newTaxi(name, email, number, taxy_Type,city)
            newTaxylatitude = newTaxytest.latitude
            newTaxylongitude = newTaxytest.longitude        
            
            # Check if a given location (taxi's location) is within the service area
            taxi_location = (newTaxylatitude, newTaxylongitude)
 
            #if service_area.contains(Point(taxi_location)):
             #   st.success("Taxi is within the service area.")    
            #else:
             #   st.error("Taxi is outside the service area.")
                
            
            TaxyDetails = pd.DataFrame(newTaxytest.Details)  
            pd.DataFrame(TaxyDetails)
        
            newTaxiDName = newTaxytest.Details.get('newTaxiDName')
            newTaxyDEmail = newTaxytest.Details.get('newTaxyDEmail')
            newTaxyDNumber = newTaxytest.Details.get('newTaxyDNumber')
            newTaxyType = newTaxytest.Details.get('newTaxyType')
            newTaxyId = newTaxytest.Details.get('newTaxyId')
            
            #newTaxyCity = newUsertest.Details.get('newTaxyCity')
            #newUserPoint = newUsertest.Details.get('newUserPoint')
            
            if st.sidebar.button('Add Taxy'):
                
                add_driver_data(newTaxiDName, newTaxyDEmail, 
                        driver_number = newTaxyDNumber,
                        taxy_Type = newTaxyType,
                        taxy_id = newTaxyId, lat_point=newTaxylatitude,
                        lon_point=newTaxylongitude)  
                
                st.sidebar.success("Added {} To fleet".format(newTaxyId))
                
                
                
                
        if Driver_opps == 'GetaRide':
            country ="USA"            
            Rider_name = st.sidebar.text_input("Add name")
            Rider_address = st.sidebar.text_input("Add address")
            Rider_email = st.sidebar.text_input("Add email")
            Rider_number = st.sidebar.text_input("Add number")
            Rider_Type = st.sidebar.selectbox("User Category:",
                                        options=['FirstTime', 'Frequent', 'VipUser', 'NoAccount'])

            newUsertest = newUser(Rider_name, Rider_email, Rider_number, Rider_Type, Rider_address)
            #latitude = newUsertest.latitude
            #longitude = newUsertest.longitude        
            
            
            # Check if a given location (taxi's location) is within the service area
            #taxi_location = (latitude, longitude)
 
            #if service_area.contains(Point(taxi_location)):
                                
             #   st.success("Taxi is within the service area.")
                
            #else:
                
             #   st.error("Taxi is outside the service area.")
                
            
            newUsertest.Details 
    
            
            newUserName = newUsertest.Details.get('newUserName')
            newUserEmail = newUsertest.Details.get('newUserEmail')
            newUserNumber = newUsertest.Details.get('newUserNumber')
            newUserType = newUsertest.Details.get('newUserType')
            newUserId = newUsertest.Details.get('newUserId')
            newUserAddress = newUsertest.Details.get('newUserAddress')
            
            long, long = get_geocode(newUserAddress)
            
            #newTaxyCity = newUsertest.Details.get('newTaxyCity')
            #newUserPoint = newUsertest.Details.get('newUserPoint')
            
            if st.sidebar.button('Complete Sign up'):
                
                add_user_data(newUserName, newUserEmail, 
                        driver_number = newUserNumber,
                        taxy_Type = newUserType,
                        taxy_id = newUserId, lat_point=long,
                        lon_point=long)  
                
                st.sidebar.success("Added {} To fleet".format(newTaxyId))
        
          #  view_result = view_all_data()   
           # view_resultdf = pd.DataFrame(view_result,columns=['driver_name',"driver_email","driver_number", "taxy_Type","latitude","longitude", "taxi_id"])
            #view_resultdf["color"] = view_resultdf.apply(CabTypecolors, axis=1)
            #view_resultdf_colorless = view_resultdf.drop(['color',"driver_email","driver_number","latitude","longitude"], axis=1)
            #view_resultdf_colorless

            #make_map(view_resultdf)


                
    if choice == 'UpdateAct':
            UpdateSec = list(clean_df['taxy_id'])
            tobeupSelection = st.sidebar.selectbox('Choose record to update', options = UpdateSec)
            rec = clean_df[clean_df['taxy_id'] == tobeupSelection]
            
            newTaxyId =  rec[['taxy_id']]
            
            New_email = st.sidebar.text_input("New driver email")
            
            if New_email == "":
                New_email =  rec['driver_email']
            
            New_number = st.sidebar.text_input("New driver number")
            if New_number == "":
                New_number =  rec['driver_number']
                
            New_taxy_Type = st.sidebar.text_input("Taxy Category:")
            if New_taxy_Type == '':
                New_taxy_Type =  rec['taxy_Type']
        
            if st.sidebar.button('Update Now'):
                edit_driver_data(New_email,New_number,New_taxy_Type, newTaxyId)   
                st.success("Updated")

                #st.success("Updated ::{} ::To {}".format(old_loanName,New_loan_name))
        
                
            #loan_type = st.sidebar.text_input("New Loan Category:")
            #loan = st.sidebar.number_input("New Loan Amount:", min_value = 0.00, step=1.,format= "%.2f",)
            #if loan == 0.00:
             #   loan = list(rec['Loan']).pop(-1)
                                
            rec

            
            
            #elif choice == "ToRide":
             #   pass
        
    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

main()