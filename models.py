import datetime
from flask import url_for
from explore import db


class ExploreEvent(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    address = db.StringField(max_length=255, required=True)
    time = db.StringField(max_length=255, required=True)
    lat = db.StringField(max_length=255, required=True)
    lon = db.StringField(max_length=255, required=True)
