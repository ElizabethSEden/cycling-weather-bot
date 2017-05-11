#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy, urllib.request, json
from types import SimpleNamespace as Namespace
from Forecast import Forecasts

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 
CONSUMER_SECRET = 
ACCESS_KEY = 
ACCESS_SECRET = 

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#Get forecast from MetOffice
MET_API_KEY = #Your MetOffice DataPoint developer key
LOCATION_ID = #Go to http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/xml/sitelist?key=MET_API_KEY to see a list of sites with their ids

with urllib.request.urlopen('http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/'+LOCATION_ID+'?res=3hourly&key='+MET_API_KEY) as url:
    data = url.read().decode()

#Turn into Forecasts object
api_data = json.loads(data, object_hook=lambda d: Namespace(**d))
forecasts = Forecasts(api_data)

#api.update_status
#Tweet relevant bits
if "VP" in forecasts.visibilities:
    api.update_status("Very poor (<1km) visibility today.")

if any(uv>=8 for uv in forecasts.uv):
    uv_index = max(forecasts.uv)
    api.update_status("Very high UV today ({}). Avoid going out at midday.".format(uv_index))
elif any(uv>=6 for uv in forecasts.uv):
    uv_index = max(forecasts.uv)
    api.update_status("High UV today ({}). Cover up.".format(uv_index))
elif any(uv>=3 for uv in forecasts.uv):
    uv_index = max(forecasts.uv)
    api.update_status("Moderate UV today ({}). Take care if you're fair.".format(uv_index))
    
if any(pp>80 for pp in forecasts.rain):
    api.update_status("It's going to rain today.")
elif any(pp>60 for pp in forecasts.rain):
    api.update_status("It's probably going to rain today.")
elif any(pp>20 for pp in forecasts.rain):
    api.update_status("It might rain today.")

if any(t<0 for t in forecasts.temperatures):
    api.update_status("It's going to feel freezing today.")
elif any(t<5 for t in forecasts.temperatures):
    temperature = min(forecasts.temperatures)
    api.update_status("It's going to feel cold ({}°C) today.".format(temperature))

if any(t>25 for t in forecasts.temperatures):
    api.update_status("It's going to feel hot today.")
elif any(t>20 for t in forecasts.temperatures):
    api.update_status("It's going to feel warm today.")

if any(speed>40 for speed in forecasts.wind_speed):
    api.update_status("Gale today. Cars will veer on road. Cycling not recommended.")
elif any(speed>30 for speed in forecasts.wind_speed):
    windspeed = max(forecasts.wind_speed)
    api.update_status("Strong winds ({}mph) today. Cycling will be hard.".format(windspeed))
elif any(gust>20 for gust in forecasts.gusts):
    api.update_status("Wind gusts over 20mph today. They will knock you sideways.")
elif any(speed>15 for speed in forecasts.wind_speed):
    api.update_status("Wind speeds over 15mph today. Be ready for dust in your eyes.")