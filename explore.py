import os
import eventful
import random
from flask import Flask, request, render_template, url_for, redirect, jsonify
from LastFMLoc import LastFMEvents
from SeatGeekLoc import SeatgeekEvents
from flask.ext.mongoengine import MongoEngine
from googlemaps import GoogleMaps
from ExploreAPI import *
from models import *
from keys import *

app = Flask(__name__)
app.debug = True
app.config["MONGODB_SETTINGS"] = {'DB': "explore_more"}
app.config["SECRET_KEY"] = SECRET

db = MongoEngine(app)

gmaps = GoogleMaps(GOOGLE)

api = eventful.API(EVENTFUL)

noEvents = False


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['location']
        return redirect(url_for("map", query=query))
    return render_template("index.html")


@app.route('/map/', methods=['GET', 'POST'])
def map():
    query = request.args.get('query')

    if request.method == 'POST':
        query = request.form['location']
        return redirect(url_for("map", query=query))

    return render_template("map.html", events=_populate_eventlist(query), query=query, flag=noEvents)


@app.route('/submit/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        title = request.form.get('event_title')
        address = request.form.get('event_address')
        time = request.form.get('event_time')
        lat, lon = gmaps.address_to_latlng(address)

        event = ExploreEvent(
            title=title,
            address=address,
            time=time,
            lat=lat,
            lon=lng)
        event.save()
        return redirect(url_for("map", query=address))


@app.route('/api/', methods=['GET', 'POST'])
def api_result():
    if request.method == 'GET':
        explore_api = ExploreApi()
        explore_api.search_events(request.args)
        resp = jsonify(explore_api.events_json)
        resp.status_code = 200
        return resp


def _populate_eventlist(query):
    events = []

    eventful_query = api.call("events/search", location=query, date="Today", page_size=25, sort_order="popularity")
    events.extend(get_eventful_events(eventful_query))

    last_fm = LastFMEvents(location=query)
    events.extend(last_fm.events)

    seatgeek = SeatgeekEvents(location=query)
    events.extend(seatgeek.events)

    events.extend(_find_explore_events(query))

    events = random.sample(events, len(events))

    return events


def get_eventful_events(events):
    eventList = []

    if events['total_items'] == 0:
        noEvents = True
        return eventList
    noEvents = False

    try:
        for event in events['events']['event']:
            eventSubList = [event['title'], event['venue_address'], event['longitude'], event['latitude'], event['url']]
            eventList.append(eventSubList)
    except TypeError:
        for event in events['events']:
            pass
    return eventList


def _find_explore_events(location):
    explore_api = ExploreApi()
    explore_api.search_events(location=location)
    return explore_api.events_list


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
