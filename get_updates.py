from forecast_update_builder import ForecastUpdateBuilder
from update_maker import UpdateMaker

def write_updates(forecasts):
    updates = ForecastUpdateBuilder(forecasts)
    updates.add(UpdateMaker("Very poor (<1km) visibility {}.", lambda f: f.visibility == "VP").make(updates.forecasts))
    updates.add_precipitation_update()
    updates.add_temperature_update()
    updates.add_wind_update()
    updates.add_humidity_update()
    updates.add_UV_update()
    updates.add_lovely_day()
    return updates.items