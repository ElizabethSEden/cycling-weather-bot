from update_maker import UpdateMaker, PrecipitationUpdateMaker

class ForecastUpdateBuilder:
    def __init__(self, forecasts):
        self.items = []
        self.forecasts = list(f for f in forecasts if f.time >= 6)

    def add(self, text):
        if text:
            self.items.append(text)

    def add_first_matching(self, update_makers):
        for maker in update_makers:
            text = maker.make(self.forecasts)
            if text:
                self.add(text)
                return

    def add_wind_update(self):
        max_wind_speed = max(f.wind_speed for f in self.forecasts)
        self.add_first_matching([
            UpdateMaker("Gale {} - cars will veer on road - cycling not recommended.", lambda f: f.wind_speed >= 40),
            UpdateMaker("Strong winds ({1}mph) {0} - cycling will be hard.",           lambda f: f.wind_speed >= 30, args=[max_wind_speed]),
            UpdateMaker("Wind gusts over 25mph {} - they can knock you sideways.",     lambda f: f.gust >= 25),
            UpdateMaker("Wind speeds over 15mph {} - be ready for dust in your eyes.", lambda f: f.wind_speed >= 15)
        ])

    def add_UV_update(self):
        uv_index = max(f.UV for f in self.forecasts)
        self.add_first_matching([
            UpdateMaker("Very high UV ({1}) {0}  - avoid going out at midday.", lambda f: f.UV >= 8, args=[uv_index]),
            UpdateMaker("High UV ({1}) {0} - cover up.",                        lambda f: f.UV >= 6, args=[uv_index]),
            UpdateMaker("Moderate UV ({1}) {0} - take care if you're fair.",    lambda f: f.UV >= 4, args=[uv_index])
        ])

    def add_temperature_update(self):
        min_temp = min(f.temperature for f in self.forecasts)
        self.add_first_matching([
            UpdateMaker("It's going to feel freezing {}.", lambda f: f.temperature <= 0),
            UpdateMaker("It's going to feel cold ({1}°C) {0}.", lambda f: f.temperature < 5, args=[min_temp])
        ])

        max_temp = max(f.temperature for f in self.forecasts)
        self.add_first_matching([
            UpdateMaker("It's going to feel hot ({1}°C) {0}.", lambda f: f.temperature <= 0, args=[max_temp]),
            UpdateMaker("It's going to feel warm ({1}°C) {0}.", lambda f: f.temperature < 5, args=[max_temp])
        ])

    def add_humidity_update(self):
        max_dew_point = max(f.dew_point for f in self.forecasts if f.dew_point is not None)
        min_dew_point = min(f.dew_point for f in self.forecasts if f.dew_point is not None)
        self.add_first_matching([
            UpdateMaker("It's going to be oppressively humid {0}. (Dew point {1})", lambda f: f.dew_point is not None and f.dew_point >= 24, max_dew_point),
            UpdateMaker("It's going to be very humid {0}. (Dew point {1})", lambda f: f.dew_point is not None and f.dew_point >= 21, max_dew_point),
            UpdateMaker("It's going to be quite humid {0}. (Dew point {1})", lambda f: f.dew_point is not None and f.dew_point >= 18, max_dew_point),
            UpdateMaker("It's going to be uncomfortably dry {0}. (Dew point {1})", lambda f: f.dew_point is not None and f.dew_point <= -5, min_dew_point)
        ])

    # def add_rain_update(self):
    #     rain_update = ""
    #     definite_time = get_time([f for f in self.forecasts if f.rain > 80])
    #     if definite_time is not None:
    #         rain_update += ("It's going to rain {}. ".format(definite_time))
    #     if definite_time is None or not definite_time == "today":
    #         probable_time = get_time([f for f in self.forecasts if 50 < f.rain <= 80])
    #         if probable_time is not None:
    #             probable_time = get_at_other_times(definite_time is not None, probable_time)
    #             rain_update += ("It's probably going to rain {}. ".format(probable_time))
    #         if probable_time is None or not "today" in probable_time:
    #             time = get_time([f for f in self.forecasts if f.rain > 20])
    #             if time is not None:
    #                 time = get_at_other_times(definite_time is not None or probable_time is not None, time)
    #                 rain_update += ("It might rain {}. ".format(time))
    #     if not rain_update == "":
    #         self.add(rain_update.rstrip())

    def add_lovely_day(self):
        if all(f.weather_type == "sunny" or f.weather_type == "partly cloudy" for f in self.forecasts):
            self.add("Beautiful day for a bike ride")

    def add_fog_update(self):
        self.add_first_matching([
            UpdateMaker("It's going to be foggy {}.", lambda f: f.weather_type == "foggy"),
            UpdateMaker("It's going to be misty {}.", lambda f: f.weather_type == "misty"),
        ])

    def add_precipitation_update(self):
        self.add(PrecipitationUpdateMaker("{probability} sleet {time}{showers}.", lambda f: f.weather_type == "sleet").make(self.forecasts))
        self.add(PrecipitationUpdateMaker("{probability} hail {time}{showers2}.", lambda f: f.weather_type == "hail").make(self.forecasts))
        self.add(PrecipitationUpdateMaker("{probability}{intensity} snow{showers} {time}.", lambda f: "snow" in f.weather_type).make(self.forecasts))
        self.add(PrecipitationUpdateMaker("{probability} thunderstorm {showers}{time}.", lambda f: "thunder" in f.weather_type).make(self.forecasts))

        self.add_first_matching([
            PrecipitationUpdateMaker("{probability}{intensity} rain{showers} {time}.", lambda f: "rain" in f.weather_type),
            PrecipitationUpdateMaker("{probability} drizzle {time}.", lambda f: f.weather_type == "drizzle"),
        ])