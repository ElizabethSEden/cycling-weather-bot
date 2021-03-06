#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy, json
from urllib.request import Request, urlopen
from types import SimpleNamespace as Namespace
from Forecast import Forecasts
from craft_message import *
from get_updates import write_updates
from pollution import get_pollution_alert
from weather_warning import get_weather_warning
from settings import *
from datetime import date

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#Get forecast from MetOffice
url = 'http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/'+MET_LOCATION_ID+'?res=3hourly&key='+MET_API_KEY
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urlopen(req) as web_forecast:
    data = web_forecast.read().decode()

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

try:
    weather_warning = get_weather_warning()
    if weather_warning is not None:
        updates.append(str(weather_warning))
except:
    api.send_direct_message(recipient_id=RECIPIENT_ID,text="Weather warnings broken on "+date.today().__str__())


if len(updates) == 0:
    updates.append("Grey day.")

alerts = fit_into_tweets(sort_by_time(updates))

for alert in alerts:
    print(alert)
    #api.update_status(alert)
    #print("Alert tweeted")