import urllib2
import simplejson
from ExternalApiEvents import *


class SeatgeekEvents(ExternalApiEvents):

    def get_events(self, event_location, format="json"):
        event_location = event_location.replace(' ', '+')
        request_string = "http://api.seatgeek.com/2/events?venue.city={0}".format(event_location)
        self.json = self.send_request(request_string)
        self.events = self._build_event_list(self.json)

    def _build_event_list(self, json):
        loc_event = []
        try:
            for event in json['events']:
                event_items = []
                event_items.append(event['title'])
                event_items.append(event['venue']['name'])
                event_items.append(event['venue']['location']['lat'])
                event_items.append(event['venue']['location']['lon'])
                event_items.append(event['url'])
                event_items.append(event['venue']['address'] + ' ' + event['venue']['state'] + ' ' + event['venue']['postal_code'])
                event_items.append(event['performers'][0]['image'])
                loc_event.append(event_items)
        except KeyError:
            pass

        return loc_event
