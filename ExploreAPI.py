
from googlemaps import GoogleMaps
from models import *
from keys import *

gmaps = GoogleMaps(GOOGLE)


class ExploreApi(object):

    def __init__(self):
        self.events_json = []
        self.events_list = []

    def search_events(self, **kwargs):
        ''' queries allowed are keyword, location, radius and time'''
        keyword = None
        location = None
        time = None
        radius = 20
        if "keyword" in kwargs:
            keyword = kwargs["keyword"]
        if "location" in kwargs:
            location = kwargs["location"]
        if "radius" in kwargs:
            radius = kwargs["radius"]
        if "time" in kwargs:
            time = kwargs["time"]

        self._get_events(keyword, location, radius, time)

    def _get_events(self, keyword, location, radius, time):
        for item in ExploreEvent.objects:
            if self._event_in_radius(item, location, radius):
                if keyword != None and keyword in event.title:
                    self._add_entry(item)
                else:
                    self.add_entry(item)

    def _event_in_radius(self, item, location, radius):
        lat, lon = gmaps.address_to_latlng(location)
        try:
            if (abs(item.lat - lat) < radius) and (abs(item.lon - lon) < radius):
                return True
            else:
                return False
        except:
            return False

    def _add_entry(item):
        self.events_json.append(_create_json_entry(item))
        self.events_list.append(_create_list_entry(item))

    def _create_json_entry(self, item):
        event = {
            "title": item.title,
            "address": item.address,
            "lat": item.lat,
            "long": item.lon,
            "url": ''
        }
        return event

    def _create_list_entry(self, item):
        event = []
        for attr, value in item.__dict__.iteritems():
            event.append(value)
        event.append('')
        return event
