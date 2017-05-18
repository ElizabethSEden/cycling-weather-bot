from datetime import date
import calendar


def get_time_index(update):
    if "today" in update:
        return 0
    elif "this morning" in update:
        return 1
    elif "this lunchtime" in update:
        return 2
    elif "this afternoon" in update:
        return 3
    elif "this evening" in update:
        return 4
    elif "tonight" in update:
        return 5
    else:
        return None


def sort_by_time(updates):
    timed_updates = {}
    for update in updates:
        timed_updates[update] = get_time_index(update)
    for update in sorted(timed_updates, key=timed_updates.get):
        yield update


def fit_into_tweets(updates):
    dayname = calendar.day_name[date.today().weekday()]
    alerts = []
    alert = dayname + ": "
    addToAlert = True
    i = 1
    for update in updates:
        if (len(alert) + len(update) < 140):
            alert += update + " "
            addToAlert = True
        else:
            alerts.append(alert.rstrip())
            i += 1
            alert = dayname + ": " + update + " "
    if addToAlert or len(alerts) < i:
        alerts.append(alert.rstrip())
    return alerts
