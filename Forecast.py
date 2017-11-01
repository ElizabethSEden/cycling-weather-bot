from datetime import datetime, date
from bs4 import BeautifulSoup

def get_weather(weather_code):
    # http://www.metoffice.gov.uk/datapoint/support/documentation/code-definitions
    #duplicates correspond to daytime and nighttime
    #(for which forecast websites use different pictures)
    weather_type = {
        1:  "sunny",
        2:  "partly cloudy",
        3:  "partly cloudy",
        #4 doesn't have a value in the spec
        5:  "mist",
        6:  "fog",
        7:  "cloudy",
        8:  "overcast",
        9:  "light rain shower",
        10:  "light rain shower",
        11:  "drizzle",
        12:  "light rain",
        13:  "heavy rain shower",
        14:  "heavy rain shower",
        15:  "heavy rain",
        16:  "sleet shower",
        17:  "sleet shower",
        18:  "sleet",
        19:  "hail shower",
        20:  "hail shower",
        21:  "hail",
        22:  "light snow shower",
        23:  "light snow shower",
        24:  "light snow",
        25:  "heavy snow shower",
        26:  "heavy snow shower",
        27:  "heavy snow",
        28:  "thunder shower",
        29:  "thunder shower",
        30:  "thunder",
    }
    if weather_code in weather_type.keys():
        return weather_type[weather_code]
    else:
        return ""

class Forecast:
    def __init__(self, api_data, is_xml=False):
        if is_xml:
            self.gust = int(api_data.get('G'))
            self.wind_direction = api_data.get('D')
            self.wind_speed = int(api_data.get('S'))
            self.visibility = api_data.get('V')
            self.temperature = int(api_data.get('F'))
            self.rain = int(api_data.get('Pp'))
            self.UV = int(api_data.get('U'))
            self.humidity = int(api_data.get('H'))
            self.time = int(api_data.contents[0]) / 60 + BST_offset(date.today())
            self.weather_type = get_weather(int(api_data.get('W')))
        else:
            self.gust = int(api_data.G)
            self.wind_direction = api_data.D
            self.wind_speed = int(api_data.S)
            self.visibility = api_data.V
            self.temperature = int(api_data.F)
            self.rain = int(api_data.Pp)
            self.UV = int(api_data.U)
            self.humidity = int(api_data.H)
            self.time = int(api_data.time)/60 + BST_offset(date.today())
            self.weather_type = get_weather(int(api_data.W))
        self.dew_point = self.get_dew_point()
        print(self.weather_type)
        print(self.dew_point)

    def get_dew_point(self):
        #This formula is only accurate above 50% humidity
        #For humidity below 50, temperature has to be over 35 for it to be sticky.
        #If temperature below 11, can be dry at humidity of 50.
        if self.humidity > 50:
            return self.temperature - (100 - self.humidity)/5
        return None

class Forecasts:
    #forecasts will be a list of 6 Forecast objects
    def __init__(self, api_data, is_xml=False):
        if is_xml:
            soup = BeautifulSoup(api_data, "xml")
            todays_forecast = soup.Period
            self.forecasts = [Forecast(f, True) for f in todays_forecast.find_all("Rep")]
        else:
            dv = api_data.SiteRep.DV
            today = dv.dataDate.split("T")[0] #get the date but not the time from "YYYY-MM-DDTHH:MM:SSZ"
            todays_forecast = dv.Location.Period[0]
            if not todays_forecast.value.replace("Z","") == today:
                raise ValueError("Today's forecast not found in Met Office API data")
            self.forecasts = [Forecast(f) for f in todays_forecast.Rep]

def BST_offset(input_date):
    if input_date.month in range(4,9):
        return 1
    if input_date.month in [11,12,1,2]:
        return 0
    # Find start and end dates for current year
    current_year = input_date.year

    #So for March and October
    for day in range(25,32): #Loop through days until you find Saturday
        if datetime(current_year,3,day).weekday()==6:
            BST_start = date(current_year,3,day)
        if datetime(current_year,10,day).weekday()==6:
            BST_end = date(current_year,10,day)

    if (input_date > BST_start) and (input_date < BST_end):
        return 1

    return 0
