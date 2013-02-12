from keys import LASTFM
from ExternalApiEvents import *


class LastFMEvents(ExternalApiEvents):

    def __init__(self, location=None):
        self.api_key = LASTFM
        self.json = {}
        self.events = []
        if location != None:
            self.get_events(location)

    def get_events(self, event_location, format="json"):
        event_location = event_location.replace(' ', '+')
        request_string = "http://ws.audioscrobbler.com/2.0/?method=geo.getevents&location={0}&api_key={1}&format={2}".format(event_location, self.api_key, format)
        self.json = self.send_request(request_string)
        self.events = self._build_event_list(self.json)

    def _build_event_list(self, json):
        loc_event = []
        try:
            for event in json['events']['event']:
                event_items = []
                event_items.append(event['title'])
                event_items.append(event['venue']['name'])
                event_items.append(event['venue']['location']['geo:point']['geo:lat'])
                event_items.append(event['venue']['location']['geo:point']['geo:long'])
                event_items.append(event['url'])
                event_items.append(event['venue']['location']['street'] + ', ' + event['venue']['location']['city'] + ', ' + event['venue']['location']['country'] + ' ' + event['venue']['location']['postalcode'])
                event_items.append(event['image'][2]["#text"])

                loc_event.append(event_items)
        except KeyError:
            pass

        return loc_event
