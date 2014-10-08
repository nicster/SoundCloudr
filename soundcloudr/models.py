# -*- coding: utf8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import flask.ext.sqlalchemy
from soundcloudr import app

db = flask.ext.sqlalchemy.SQLAlchemy(app)

class PlayPosition(db.Model):
    user = db.Column(db.String(255) , primary_key=True)
    track_id = db.Column(db.Integer)

    def __init__(self, user, track_id):
        self.user = user
        self.track = track_id

