#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy, urllib.request, json
from types import SimpleNamespace as Namespace
from Forecast import Forecasts
from craft_message import *
from get_updates import write_updates
from pollution import get_pollution_alert
from weather_warning import get_weather_warning
from settings import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#Get forecast from MetOffice
with urllib.request.urlopen('http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/'+MET_LOCATION_ID+'?res=3hourly&key='+MET_API_KEY) as url:
    data = url.read().decode()

#Turn into Forecasts object
data = data.replace("$","time") #Namespace can't handle a variable named $, so rename it to time
api_data = json.loads(data, object_hook=lambda d: Namespace(**d))

try:
    forecasts = Forecasts(api_data)
except AttributeError:
    with urllib.request.urlopen('http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/xml/' + MET_LOCATION_ID + '?res=3hourly&key=' + MET_API_KEY) as url:
        data = url.read().decode()
    forecasts = Forecasts(data, True)

updates = write_updates(forecasts.forecasts)

pollution_alert = get_pollution_alert()

if pollution_alert is not None:
    updates.append(pollution_alert)

weather_warning = get_weather_warning()

if weather_warning is not None:
    updates.append(str(weather_warning))

if len(updates) == 0:
    updates.append("An English day. No rain, but cloudy; not hot or cold; not windy or foggy; not humid or dry.")

alerts = fit_into_tweets(sort_by_time(updates))

for alert in alerts:
    print(alert)
    #api.update_status(alert)
    #print("Alert tweeted")