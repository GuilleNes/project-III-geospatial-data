import requests
from dotenv import load_dotenv
import pandas as pd
import geopandas as gpd
import geopy
from folium import  Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster

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

# Getting subsets from our different cities

def do_subset(dfr, city):
    return  dfr.loc[dfr['City'] == city]


#---------------------------------------------------- Foursquare API

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

# And we use this function only for the airports

def get_results_airport(query, location, limit, radius, token):
    ll = f"{location[0]}%2C{location[1]}"   
    url =f'https://api.foursquare.com/v3/places/search?query={query}&ll={ll}&radius={radius}&categories=19040&limit={str(limit)}'      
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

def calc_distance_LO(x):
    site_coords = (51.505024, -0.080416)
    place2_coords = (x.lat, x.lon)
    return (geopy.distance.geodesic(site_coords, place2_coords).km)*1000

# df_SE["Distance"] = df_SE.apply(fun.calc_distance_SE, axis = 1).round(2)

def calc_distance_CA(x):
    site_coords = (42.3731956,-71.1198561)
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
        new_list.append({"name":name,"category": categ,  "address": address, 'neighborhood': "Null", "lat":lat, "lon":lon})        
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


# ------------------------------------------------------------------------------------------------- Ponderations

# Getting the values for wheighting our cities

def get_df(dfr):
    index = pd.Index(['Airport','Basketball arena','Club','Coffee','Pet hairdresser',"Preschool","Vegan restaurant"], name = "Category")
    dfr = pd.DataFrame({'Weight':[0.2,0.1,0.15,0.15,0.05,0.2,0.15]}, index=index)
    return
# df_CA = pd.read_csv("../Data/df_CA.csv")
# df_CA = df_CA.iloc[1:]

def get_weight(dfr, df1):

    mean_distance = df1.groupby("category").mean("Distance").drop(["lat", "lon"], axis = 1)
    dfr = pd.concat([dfr, mean_distance], axis=1)
    dfr = dfr.rename({'Distance': 'Mean'}, axis=1)

    max_distance = df1.groupby("category").max("Distance").drop(["lat", "lon"], axis = 1)
    dfr = pd.concat([dfr, max_distance], axis=1)
    dfr = dfr.rename({'Distance': 'Max'}, axis=1)

    min_distance = df1.groupby("category").min("Distance").drop(["lat", "lon"], axis = 1)
    dfr = pd.concat([dfr, min_distance], axis=1)
    dfr = dfr.rename({'Distance': 'Min'}, axis=1)
    return dfr


def final_result(dfr, city):
    if dfr['Mean'].isnull().values.any():
        dfr = dfr.fillna(3000)
        dfr['Final Result'] = round(dfr["Mean"]/dfr["Radius"] * dfr["Weight factor"], 2)
        

    else:
        dfr['Final Result'] = round(dfr["Mean"]/dfr["Radius"] * dfr["Weight factor"], 2)

    final_r = dfr["Final Result"].sum().round(2)
    
    return f"The final result for {city} is {final_r}"



#------------------------------------------------------------------------- Mapping functions



def mapping_results(df, map):

    for index, row in df.iterrows():
        
        #1. MARKER without icon
        district = {"location": [row["lat"], row["lon"]], "tooltip": row["name"]}
        
        #2. Icon
        if row["category"] == "Coffee":        
            icon = Icon (
                color="white",
                opacity = 0.6,
                prefix = "fa",
                icon="coffee",
                icon_color = "black"
            )
        elif row["category"] == "Preschool":
            icon = Icon (
                color="pink",
                opacity = 0.6,
                prefix = "fa",
                icon="graduation-cap",
                icon_color = "yellow"
            )
        elif row["category"] == "Club":
            icon = Icon (
                color="darkpurple",
                opacity = 0.6,
                prefix = "fa",
                icon="glass",
                icon_color = "white"
            )
        elif row["category"] == "Vegan restaurant":
            icon = Icon (
                color="green",
                opacity = 0.6,
                prefix = "fa",
                icon="cutlery",
                icon_color = "white"
            )
        elif row["category"] == "Basketball arena":
            icon = Icon (
                color="orange",
                opacity = 0.6,
                prefix = "fa",
                icon="futbol-o",
                icon_color = "white"
            )
        elif row["category"] == "Airport":
            icon = Icon (
                color="blue",
                opacity = 0.6,
                prefix = "fa",
                icon="plane",
                icon_color = "white"
                
            )
        elif row["category"] == "Pet hairdresser":
            icon = Icon (
                color="red",
                opacity = 0.6,
                prefix = "fa",
                icon="scissors",
                icon_color = "white"
                
            )
        else:
            row["category"] == "Company",
            icon = Icon (
            color="black",
            opacity = 0.9,
            prefix = "fa",
            icon = "briefcase",
            icon_color = "white",
            icon_size=(30, 30)
            )
                
        #3. Marker
        marker = Marker(**district, icon = icon, radius = 2)
        
        #4. Add the Marker
        marker.add_to(map)
    return

def mapping_companies(subset, map):
    for index, row in subset.iterrows():
    
        #1. MARKER without icon
        district = {"location": [row["Lat"], row["Long"]], "tooltip": row["name"]}
        
        #2. Icon       
        icon = Icon (
        color="white",
        opacity = 0.6,
        prefix = "fa",
        icon="building",
        icon_color = "black"
            )

                
        #3. Marker
        marker = Marker(**district, icon = icon, radius = 2)
        
        #4. Add the Marker
        marker.add_to(map)
  
    return






