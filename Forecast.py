class Forecast:
    def __init__(self, api_data):
        self.gust = int(api_data.G)
        self.wind_direction = api_data.D
        self.wind_speed = int(api_data.S)
        self.visibility = api_data.V
        self.temperature = int(api_data.T)
        self.rain = int(api_data.Pp)
        self.UV = int(api_data.U)

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
        