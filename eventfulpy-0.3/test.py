import eventful

api = eventful.API('WDL5Mhk7MWmxX6BM')

events = api.call('events/search', location="San Diego", date="Today", page_size=25, sort_order="popularity")

for event in events['events']['event']:
    print "%s at %s" % (event['title'], event['start_time'])
    print "%s by %s" % (event['latitude'], event['longitude'])