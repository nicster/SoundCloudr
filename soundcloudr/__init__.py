# -*- coding: utf8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import flask
import soundcloud

import soundcloudr.playlist
from soundcloudr.models import db
#from soundcloudr.models import PlayPosition

app = flask.Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")

db.create_all()

#PlayPosition('Nic', 1234)

@app.route("/")
def home():
    if 'access_token' in flask.session:
        return flask.render_template('home_loggedin.html')
    return flask.render_template('home.html')

@app.route("/login")
def login():
    return flask.redirect(flask.g.client.authorize_url())

@app.route('/authorize')
def authorize():
    access_token = flask.g.client.exchange_token(flask.request.args.get('code'))
    flask.session['access_token'] = access_token.access_token
    return flask.redirect(flask.url_for('home'))

@app.route('/play')
def play():
    playlist = soundcloudr.playlist.Playlist(flask.g.client)
    next_track = playlist.tracks.pop(0)['permalink_url']
    print next_track
    embed_info = flask.g.client.get('/oembed', url=next_track)
    return flask.render_template('home.html', player = embed_info.html)

@app.before_request
def generate_client():
    token = flask.session['access_token']
    client = soundcloud.Client(client_id = app.config['CLIENT_ID'],
                           client_secret = app.config['CLIENT_SECRET'],
                           access_token = token,
                           redirect_uri = 'http://localhost:5000/authorize')
    flask.g.client = client
