#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy, urllib.request, json
from types import SimpleNamespace as Namespace
from Forecast import Forecasts
from craft_message import *
from get_updates import write_updates
from pollution import *

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
data = data.replace("$","id")
api_data = json.loads(data, object_hook=lambda d: Namespace(**d))
forecasts = Forecasts(api_data)

updates = write_updates(forecasts.forecasts)

pollution_alert = get_pollution_alert()

if pollution_alert is not None:
    updates.append(pollution_alert)

alerts = fit_into_tweets(sort_by_time(updates))

for alert in alerts:
    print(alert)
    api.update_status(alert)
    print("Alert tweeted")