#!/usr/bin/env python3
import requests
import json
import time
import datetime
from flask import Flask, render_template
from configparser import ConfigParser
import BKK_stop_ids

app = Flask(__name__)
config_object = ConfigParser()
config_object.read("config.ini")
bkk_config = config_object["BKK"]


def get_departures():
    stop_id = bkk_config["stopId"]
    if stop_id[:3] != "BKK":
        stop_id = "BKK_" + stop_id
    minutes_after = bkk_config["minutesAfter"]
    minutes_before = bkk_config["minutesBefore"]
    url = f"https://futar.bkk.hu/api/query/v1/ws/otp/api/where/arrivals-and-departures-for-stop.json?stopId={stop_id}&onlyDepartures=true&minutesBefore={minutes_before}&minutesAfter={minutes_after}"
    return requests.get(url)


def get_minute_count(timestamp):
    diff = timestamp - time.time()
    full = datetime.datetime.fromtimestamp(timestamp).strftime("%Y/%m/%d %H:%M")
    mins = datetime.datetime.fromtimestamp(diff).strftime("%M")
    return f"{mins} perc múlva ({full})"


def get_route_id(trip_id, json_data):
    data = json_data["data"]["references"]["trips"][trip_id]["routeId"]
    return data


def get_name(route_id, json_data):
    data = json_data["data"]["references"]["routes"][route_id]["description"]
    return data.replace("|", "<>")


def get_type(route_id, json_data):
    route_type = json_data["data"]["references"]["routes"][route_id]["type"]
    type_dict = {
        "TRAM": "villamos",
        "BUS": "bus",
        "SUBWAY": "metro",
        "TROLLEYBUS": "troli",
        "RAIL": "vonat",
        "FERRY": "komp",
    }
    return type_dict[route_type]


def get_number(route_id, json_data):
    data = json_data["data"]["references"]["routes"][route_id]["shortName"]
    return data


def get_json_data():
    error_form = {"data": {"entry": {"stopTimes": []}}}
    resp = get_departures()
    if resp.status_code != 200:
        return error_form
    json_data = json.loads(resp.text)
    if json_data["data"]["limitExceeded"]:
        return error_form
    return json_data


def get_route_data(route_id, json_data, starts, stop_times_dict):
    name = get_name(route_id, json_data)
    number = get_number(route_id, json_data)
    minutes = get_minute_count(starts["departureTime"])
    route_type = get_type(route_id, json_data)
    if "predictedDepartureTime" in starts:
        minutes = get_minute_count(starts["predictedDepartureTime"])
    route_name = number + " " + route_type + ": " + name
    if route_name in stop_times_dict.keys():
        stop_times_dict[route_name].append(minutes)
    else:
        stop_times_dict[route_name] = [minutes]


def get_data() -> dict:
    config_route_id = bkk_config["routeId"]
    max_number = int(bkk_config["maxNumberOfItems"], 10)
    json_data = get_json_data()
    stop_times_list = json_data["data"]["entry"]["stopTimes"]
    if not stop_times_list:
        return {"Hiba törént, kérem várjon!": []}
    stop_times_dict = {}
    for starts in stop_times_list:
        route_id = get_route_id(starts["tripId"], json_data)
        if len(config_route_id) != 0:
            if config_route_id == route_id:
                get_route_data(route_id, json_data, starts, stop_times_dict)
        else:
            get_route_data(route_id, json_data, starts, stop_times_dict)
    for key, value in stop_times_dict.items():
        stop_times_dict[key] = value[:max_number]
    return stop_times_dict


def get_stop_name():
    stop_id = bkk_config["stopId"]
    for i in BKK_stop_ids.stop_ids:
        if i["id"] in stop_id:
            return i["name"]
    return stop_id


@app.template_filter()
def datetimefilter(value, format="%Y/%m/%d %H:%M"):
    return value.strftime(format)


app.jinja_env.filters["datetimefilter"] = datetimefilter


@app.route("/")
def template_test():
    data = get_data()
    stop_name = get_stop_name()
    return render_template(
        "index.html",
        title=f"BKV figyelő - {stop_name}",
        current_time=datetime.datetime.now(),
        nest_list=data,
    )


if __name__ == "__main__":
    app.run()
