from datetime import datetime, date

class Forecast:
    def __init__(self, api_data):
        self.gust = int(api_data.G)
        self.wind_direction = api_data.D
        self.wind_speed = int(api_data.S)
        self.visibility = api_data.V
        self.temperature = int(api_data.T)
        self.rain = int(api_data.Pp)
        self.UV = int(api_data.U)
        self.humidity = int(api_data.H)
        self.time = int(api_data.id)/60 + BST_offset(date.today())

class Forecasts:
    #forecasts will be a list of 6 Forecast objects
    def __init__(self, api_data):
        dv = api_data.SiteRep.DV
        today = dv.dataDate.split("T")[0] #get the date but not the time from "YYYY-MM-DDTHH:MM:SSZ"
        todays_forecast = dv.Location.Period[0]
        if not todays_forecast.value.replace("Z","") == today:
            raise ValueError("Today's forecast not found in Met Office API data")
        self.get_forecasts(todays_forecast.Rep)
        self.assign_variables(self.forecasts)

    def get_forecasts(self, all_forecasts):
        self.forecasts = [Forecast(f) for f in all_forecasts]

    def assign_variables(self, forecasts):
        self.gusts = [f.gust for f in forecasts]
        self.wind_speed = [f.wind_speed for f in forecasts]
        self.visibilities = [f.visibility for f in forecasts]
        self.temperatures = [f.temperature for f in forecasts]
        self.rain = [f.rain for f in forecasts]
        self.uv = [f.UV for f in forecasts]
        self.humidity = [f.humidity for f in forecasts]

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
            BST_start = datetime(current_year,3,day,1)
        if datetime(current_year,10,day).weekday()==6:
            BST_end = datetime(current_year,10,day,1)

    if (input_date > BST_start) and (input_date < BST_end):
        return 1

    return 0