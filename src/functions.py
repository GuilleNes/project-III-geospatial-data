import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd
import pymongo
import geopandas as gpd
from cartoframes.viz import Map, Layer, popup_element
import geopy

# We create a function to collect data from the offices column(country code, address, lat&long...).

def get_info(lista, df_, a, b):    
    append_data = []
    for i in range(len(lista)):
        try:           
            append_data.append(lista[i][0][b])             
        except:
            append_data.append("null")
    df_[a]= append_data
    return


# Dropping unnecesary columns

def drop_column(datfr, column):
    datfr = datfr.drop([column], axis = 1, inplace= True)
    return

# We delete some of the rows with missing data (the ones with more than one missing value)

def drop_nan(dfr):
    dfr.dropna(axis=0, inplace=True, thresh=7)
    dfr.reset_index(drop=True, inplace=True)
    return

# Mapping the values of City column to get to value_counts

def value_counts(df_,newcolumn, counting):
    df_[newcolumn] = df_[counting].map(df_[counting].value_counts())
    return

# Keeping only the columns with certain values

def keep_value(dfra, column, value):
    dfra = dfra[(dfra[column] >= value)]
    dfra.reset_index(drop=True, inplace=True)
    return dfra

#----------------------------------------------------

# Getting results from foursquare through the API


def get_results(query, location, limit, radius, token):
    ll = f"{location[0]}%2C{location[1]}"   
    url = f"https://api.foursquare.com/v3/places/search?query={query}&ll={ll}&limit={str(limit)}&radius={radius}"
    headers = {
        "accept": "application/json",
        "Authorization": token,
    }
    response = requests.get(url, headers=headers).json()
    return response


# We clean the results from the API keeping only the values that we need

def clean_results_first(df_, categ):
    new_list = []
    for i in df_["results"]:
            name = i["name"]
            address =  i["location"]["formatted_address"]
            lat = i["geocodes"]["main"]["latitude"]
            lon = i["geocodes"]["main"]["longitude"]
            neighborhood = i["location"]['neighborhood'][0]   
            new_list.append({"name":name,"category": categ,  "address": address, 'neighborhood': neighborhood, "lat":lat, "lon":lon})
    return pd.DataFrame(new_list)



def clean_results(df_, dfr, categ):
    new_list = []
    for i in df_["results"]:
        name = i["name"]
        address =  i["location"]["formatted_address"]
        lat = i["geocodes"]["main"]["latitude"]
        lon = i["geocodes"]["main"]["longitude"]
        neighborhood = i["location"]['neighborhood'][0]   
        new_list.append({"name":name, "category": categ, "address": address, 'neighborhood': neighborhood, "lat":lat, "lon":lon})
    df = pd.DataFrame(new_list)
    return pd.concat([dfr, df], axis=0).reset_index(drop= True)

# We add a row with the address of the new company

def add_company(dfr, address, neigh, lat, lon):
    new_row = pd.DataFrame({'name': "Company",'address': address,'neighborhood': neigh,'lat': lat,"lon": lon}, index =[0])
    return pd.concat([new_row, dfr]).reset_index(drop = True)


# Getting the distance from any point to the company office in meters

def calc_distance_SF(x):
    site_coords = (37.7871253, -122.4015358)
    place2_coords = (x.lat, x.lon)
    return (geopy.distance.geodesic(site_coords, place2_coords).km)*1000

# df_SF["Distance"] = df_SF.apply(fun.calc_distance_SF, axis = 1).round(2)



def calc_distance_SE(x):
    site_coords = (47.6251419,-122.3268577)
    place2_coords = (x.lat, x.lon)
    return (geopy.distance.geodesic(site_coords, place2_coords).km)*1000

# df_SE["Distance"] = df_SE.apply(fun.calc_distance_SE, axis = 1).round(2)

def calc_distance_CH(x):
    site_coords = (41.869276, -87.626694)
    place2_coords = (x.lat, x.lon)
    return (geopy.distance.geodesic(site_coords, place2_coords).km)*1000

# df_SE["Distance"] = df_SE.apply(fun.calc_distance_SE, axis = 1).round(2)



# We clean the results from the API keeping only the values that we need, only for London

def clean_results_first_lo(df_, categ):
    new_list = []
    for i in df_["results"]:
        name = i["name"]
        address =  i["location"]["formatted_address"]
        lat = i["geocodes"]["main"]["latitude"]
        lon = i["geocodes"]["main"]["longitude"]
        neighborhood = i["location"]['locality'][0]   
        new_list.append({"name":name,"category": categ,  "address": address, 'neighborhood': neighborhood, "lat":lat, "lon":lon})        
    return pd.DataFrame(new_list)


# We clean the results from the API keeping only the values that we need, only for London

def clean_results_lo(df_, dfr, categ):
    new_list = []
    for i in df_["results"]:
        name = i["name"]
        address =  i["location"]["formatted_address"]
        lat = i["geocodes"]["main"]["latitude"]
        lon = i["geocodes"]["main"]["longitude"]
        neighborhood = i["location"]['locality'][0]   
        new_list.append({"name":name, "category": categ, "address": address, 'neighborhood': neighborhood, "lat":lat, "lon":lon})
    df = pd.DataFrame(new_list)
    return pd.concat([dfr, df], axis=0).reset_index(drop= True)
