import urllib2
import simplejson


class ExternalApiEvents(object):

    def __init__(self, location=None):
        self.json = {}
        self.events = []
        if location != None:
            self.get_events(location)

    def get_events(self, event_location, format="json"):
        event_location = event_location.replace(' ', '+')
        self.json = self.send_request()

    def send_request(self, string=None):
        if string != None:
            request_string = string
            request = urllib2.Request(request_string)
            opener = urllib2.build_opener()
            f = opener.open(request)
            json_result = simplejson.load(f)
            return json_result
