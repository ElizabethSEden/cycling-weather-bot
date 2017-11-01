class UpdateMaker:
    def __init__(self, message, condition, args=[]):
        self.message = message
        self.condition = condition
        self.args = args

    def make(self, forecasts):
        matching = [f for f in forecasts if self.condition(f)]
        if matching:
            return self.format_message(matching)
        else:
            return None

    def format_message(self, matching_forecasts):
        return self.message.format(get_time(matching_forecasts), *self.args)

class PrecipitationUpdateMaker(UpdateMaker):
        def __init__(self, message, condition):
            super().__init__(message, condition)

        def format_message(self, matching_forecasts):
            return self.message.format_map({
                "time": get_time(matching_forecasts),
                "probability": get_precipitation_probability(matching_forecasts),
                "intensity": intensity(matching_forecasts),
                "showers": showers(matching_forecasts)
            })


def get_precipitation_probability(forecasts):
    precipitation_probability = max(f.rain for f in forecasts)
    if precipitation_probability >= 80:
        return "There's going to be"
    elif 50 < precipitation_probability < 80:
        return "There's probably going to be"
    elif precipitation_probability > 20:
        return "There might be"
    return None

def intensity(forecasts):
    if any("heavy" in f.weather_type for f in forecasts):
        return " heavy"
    elif all("light" in f.weather_type for f in forecasts):
        return " light"

def showers(forecasts):
    if all("shower" in f.weather_type for f in forecasts):
        return " showers"
    return ""

def get_time(forecasts):
    if len(forecasts) == 0:
        return None
    if all(f.time <= 12 for f in forecasts):
        return "this morning"
    elif all (12 <= f.time <= 14 for f in forecasts):
        return "this lunchtime"
    elif all(12 <= f.time <= 18 for f in forecasts):
        return "this afternoon"
    elif all(f.time >= 22 for f in forecasts):
        return "tonight"
    elif all(f.time >= 17 for f in forecasts):
        return "this evening"
    else:
        return "today"