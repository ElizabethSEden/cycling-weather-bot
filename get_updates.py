def get_time(forecasts):

    if all(f.time<6 for f in forecasts):
        return None
    elif all(f.time <= 12 for f in forecasts):
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

def write_updates(forecasts):
    updates = []

    time = get_time([f for f in forecasts if f.visibility=="VP"])
    if time is not None:
        updates.append("Very poor (<1km) visibility {}.".format(time))

    get_rain_update(forecasts, updates)

    time = get_time([f for f in forecasts if f.humidity > 80])
    if time is not None:
        updates.append("Humid (>80%) {}.".format(time))

    get_temperature_update(forecasts, updates)

    get_UV_update(forecasts, updates)

    get_wind_update(forecasts, updates)

    return updates


def get_wind_update(forecasts, updates):
    time = get_time([f for f in forecasts if f.wind_speed >= 40])
    if time is not None:
        updates.append("Gale {} - cars will veer on road - cycling not recommended.".format(time))
    else:
        time = get_time([f for f in forecasts if f.wind_speed >= 30])
        if time is not None:
            windspeed = max(forecasts.wind_speed)
            updates.append("Strong winds ({}mph) {} - cycling will be hard.".format(windspeed, time))
        else:
            time = get_time([f for f in forecasts if f.gust >= 25])
            if time is not None:
                updates.append("Wind gusts over 25mph {} - they can knock you sideways.".format(time))
            else:
                time = get_time([f for f in forecasts if f.wind_speed >= 15])
                if time is not None:
                    updates.append("Wind speeds over 15mph {} - be ready for dust in your eyes.".format(time))


def get_UV_update(forecasts, updates):
    time = get_time([f for f in forecasts if f.UV >= 8])
    if time is not None:
        uv_index = max(f.UV for f in forecasts)
        updates.append("Very high UV ({}) {}  - avoid going out at midday.".format(uv_index, time))
    else:
        time = get_time([f for f in forecasts if f.UV >= 6])
        if time is not None:
            uv_index = max(f.UV for f in forecasts)
            updates.append("High UV ({}) {} - cover up.".format(uv_index, time))
        else:
            time = get_time([f for f in forecasts if f.UV >= 4])
            if time is not None:
                uv_index = max(f.UV for f in forecasts)
                updates.append("Moderate UV ({}) {} - take care if you're fair.".format(uv_index, time))


def get_temperature_update(forecasts, updates):
    time = get_time([f for f in forecasts if f.temperature <= 0])
    if time is not None:
        updates.append("It's going to feel freezing {}.".format(time))
    else:
        time = get_time([f for f in forecasts if f.temperature < 5])
        if time is not None:
            temperature = min(f.temperature for f in forecasts)
            updates.append("It's going to feel cold ({}°C) {}.".format(temperature, time))
    time = get_time([f for f in forecasts if f.temperature >= 25])
    if time is not None:
        temperature = max(f.temperature for f in forecasts)
        updates.append("It's going to feel hot ({}°C) {}.".format(time))
    else:
        time = get_time([f for f in forecasts if f.temperature > 18])
        if time is not None:
            temperature = max(f.temperature for f in forecasts)
            updates.append("It's going to feel warm ({}°C) {}.".format(temperature, time))


def get_rain_update(forecasts, updates):
    time = get_time([f for f in forecasts if f.rain > 80])
    if time is not None:
        updates.append("It's going to rain {}.".format(time))
    if time is None or not time == "today":
        time = get_time([f for f in forecasts if 50 < f.rain <= 80])
        if time is not None:
            updates.append("It's probably going to rain {}.".format(time))
        if time is None or not time == "today":
            time = get_time([f for f in forecasts if f.rain > 20])
            if time is not None:
                updates.append("It might rain {}.".format(time))
