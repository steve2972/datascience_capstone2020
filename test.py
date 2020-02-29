#%%
# Exporatory Data Analysis
import pandas as pd
import numpy as np

# Url requests & parse
import urllib.request, requests
from bs4 import BeautifulSoup

# Data Visualization
import matplotlib.pyplot as plt
import folium

# File Management
import re, os, sys
import json
from pandas.io.json import json_normalize

def getLatLng(addr):
  url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+addr
  headers = {"Authorization": "KakaoAK 1dd987b2b0f2925d8b7ea121281310c8"}
  result = json.loads(str(requests.get(url,headers=headers).text))
  try:
    match_first = result['documents'][0]['address']
    return float(match_first['y']),float(match_first['x'])
  except IndexError:
    print("Not documented in API")
    return None

  

print(getLatLng("혜화동"))

# %%
df = pd.read_excel("Data/subwayStationNames.xlsx")
df.head()

# %%
df = df.drop(['연번', '한자', '중국어', '일본어'], axis=1)
df.head()


# %%
df.describe()

# %%
df.iloc[1]

# %%
df.iloc[0]['역명']

# %%
print(getLatLng('서울역'))

# %%
def getAddress(query, lat='37.5665', lng='126.9780', radius='20000'):
  url = 'https://dapi.kakao.com/v2/local/search/keyword.json?y={}&x={}&radius={}&query={}'.format(lat, lng, radius, query)
  headers = {"Authorization": "KakaoAK 1dd987b2b0f2925d8b7ea121281310c8"}
  result = json.loads(str(requests.get(url,headers=headers).text))
  return result

getAddress("강남역")

# %%
stations = []

for idx in df.index:
    name = (''.join(df['역명'][idx].split(' '))).split('(', 1)[0]
    if name[-1] != '역':
        name = name + '역'
    stations.append(name)

stations
# %%
def queryAddress(query, lat='37.5665', lng='126.9780', radius='20000'):
    # This function will return the locations with query within a radius of this.radius meters (default 20km)
    # Default coordinates centered in Seoul
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?y={}&x={}&radius={}&query={}'.format(lat, lng, radius, query)
    headers = {"Authorization": Kakao_appkey}
    result = json.loads(str(requests.get(url,headers=headers).text))
    try:
        return float(result['documents'][0]['x']), float(result['documents'][0]['y'])
    except IndexError:
        print("No such location within Seoul")
    
    return None

station_lat = []
station_lng = []

for station in stations:
    lat, lng = queryAddress(station)
    station_lat.append(lat)
    station_lng.append(lng)

df['Latitude'] = station_lat
df['Longitude'] = station_lng
df.head()

# %%

CLIENT_ID = 'RHLWHDGP2UUV5VAZOUNVEZOC3G5WQ00DPXYVYQIZIQ1BUY1G' # your Foursquare ID
CLIENT_SECRET = 'DAMEJ4SSMIYJ2UXOBS1I33K1DR0VG42RGQHTLBKKZSKPLRZZ' # your Foursquare Secret
VERSION = '20200228' # Foursquare API version

# %%
def get_categories(categories):
    return [(cat['name'], cat['id']) for cat in categories]
def format_address(location):
    address = ', '.join(location['formattedAddress'])
    address = address.replace(', Deutschland', '')
    address = address.replace(', Germany', '')
    return address
def get_venues_near_location(lat, lon, category, client_id, client_secret, radius=500, limit=100):
    version = '20200220'
    url = 'https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&v={}&ll={},{}&categoryId={}&radius={}&limit={}'.format(
        client_id, client_secret, version, lat, lon, category, radius, limit)
    try:
        results = requests.get(url).json()['response']['groups'][0]['items']
        venues = [(item['venue']['id'],
                   item['venue']['name'],
                   get_categories(item['venue']['categories']),
                   (item['venue']['location']['lat'], item['venue']['location']['lng']),
                   format_address(item['venue']['location']),
                   item['venue']['location']['distance']) for item in results]        
    except:
        venues = []
    return venues

# %%
LIMIT = 100
radius = 500
url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
    CLIENT_ID, 
    CLIENT_SECRET, 
    VERSION, 
    '37.554679', 
    '126.970607', 
    radius, 
    LIMIT)

url = 'https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&v={}&ll={},{}&categoryId={}&radius={}&limit={}'.format(
        CLIENT_ID, CLIENT_SECRET, VERSION, '37.554679', '126.970607',  '4d4b7105d754a06374d81259', radius, 100)
url # display URL

# %%
results = requests.get(url).json()
results

for item in results['response']['groups'][0]['items']:
    print(item['venue']['name'])
# %%
def get_categories(categories):
    return [(a['name'], a['id']) for a in categories]
def getNearbyVenues(lat, lon, category, radius, limit=100):
    url = 'https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&v={}&ll={},{}&categoryId={}&radius={}&limit={}'.format(
        CLIENT_ID, CLIENT_SECRET, VERSION, lat, lon, category, radius, limit)
    #url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
    #CLIENT_ID, CLIENT_SECRET, VERSION, lat, lon, radius, limit)
    results = requests.get(url).json()['response']['groups'][0]['items']
    venues = [(item['venue']['id'],
                item['venue']['name'],
                get_categories(item['venue']['categories']),
                (item['venue']['location']['lat'], item['venue']['location']['lng']),
                item['venue']['location']['formattedAddress'][0]) for item in results]        
    return venues
# %%
getNearbyVenues('37.554679', '126.970607',  '4d4b7105d754a06374d81259', 500)

# %%
