from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
from settings import POLLUTION_LOCATIONS

def get_pollution_alert():
    items = get_pollution_from_defra()
    pollution = get_local_pollution_forecasts(items)
    for forecast in sorted(pollution, key=pollution.get, reverse=True):
        level = pollution[forecast]
        if 4 <= level <= 6:
            return "Moderate air pollution ({}) today. Reduce pollution by not driving.".format(level)
        elif 7 <= level <= 9:
            return "High air pollution ({}) today. You may get sore eyes, cough or sore throat, especially if you cycle fast. Reduce pollution by not driving.".format(level)
        elif level >= 10:
            return "Very high air pollution ({}) today - it's going to be nasty out. Reduce pollution by not driving.".format(level)
    return None

def get_local_pollution_forecasts(items):
    today = datetime.now().strftime('%a')
    pollution = {}
    for forecast in items:
        if (forecast.find("title").string in POLLUTION_LOCATIONS):
            description = forecast.find("description").string
            begin = description.find(today)
            pollution[description] = int(description[begin + 5: begin + 7].rstrip())
    return pollution


def get_pollution_from_defra():
    with urllib.request.urlopen('https://uk-air.defra.gov.uk/assets/rss/forecast.xml') as url:
        data = url.read().decode()
    soup = BeautifulSoup(data, "lxml-xml")
    items = soup.findAll("item")
    return items