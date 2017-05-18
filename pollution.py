#Southwark locations:
#Southwark
#Millwall f.c.
#rotherhithe youth hostel
#Crystal palace national sports centre

from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime

def get_pollution_alert():
    items = get_pollution_from_defra()
    pollution = get_Southwark_pollution_forecasts(items)
    for forecast in sorted(pollution, key=pollution.get, reverse=True):
        level = pollution[forecast]
        if 4 <= level <= 6:
            return "Moderate pollution today. Reduce pollution by not driving."
        elif 7 <= level <= 9:
            return "High pollution today. You may get sore eyes, cough or sore throat, especially if you cycle fast. Reduce pollution by not driving."
        elif level >= 10:
            return "Very high pollution today - it's going to be nasty out. Reduce pollution by not driving."
    return None

def get_Southwark_pollution_forecasts(items):
    today = datetime.now().strftime('%a')
    pollution = {}
    for forecast in items:
        if (forecast.find("title").string == "SOUTHWARK"
            or forecast.find("title").string == "MILLWALL F.C."
            or forecast.find("title").string == "ROTHERHITHE YOUTH HOSTEL"
            or forecast.find("title").string == "CRYSTAL PALACE NATIONAL SPORTS CENTRE"):
            description = forecast.find("description").string
            begin = description.find(today)
            pollution[description] = int(description[begin + 5: begin + 7].rstrip())
    return pollution


def get_pollution_from_defra():
    with urllib.request.urlopen('https://uk-air.defra.gov.uk/assets/rss/forecast.xml') as url:
        data = url.read().decode()
    soup = BeautifulSoup(data, "xml")
    items = soup.findAll("item")
    return items