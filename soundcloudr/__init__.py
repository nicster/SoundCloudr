# -*- coding: utf8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import json

import flask
import soundcloud

import soundcloudr.playlist

app = flask.Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")

from soundcloudr.models import db
from soundcloudr.models import PlayPosition


@app.route("/")
def home():
    if 'access_token' in flask.session:
        return flask.render_template('home_loggedin.html')
    else:
        return flask.render_template('home.html')

@app.route("/login")
def login():
    return flask.redirect(flask.g.client.authorize_url())

@app.route("/logout")
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('home'))


@app.route('/authorize')
def authorize():
    access_token = flask.g.client.exchange_token(flask.request.args.get('code'))
    flask.session['access_token'] = access_token.access_token
    generate_client()
    flask.session['username'] = flask.g.client.get('/me').username
    return flask.redirect(flask.url_for('home'))

@app.route('/tracks')
def tracks():
    if 'access_token' not in flask.session:
        return flask.abort(401)
    else:
        user = PlayPosition.query.filter_by(user=flask.session['username']).first()
        if not user:
            user = PlayPosition(flask.session['username'])
            db.session.add(user)
            l_track = None
            user.track_id = l_track
            db.session.commit()
        else:
            l_track = user.first().track_id
    tracks = soundcloudr.playlist.Playlist(flask.g.client, l_track).tracks
    rv = flask.make_response(
        json.dumps([track['id'] for track in tracks
        if track['duration'] <= app.config['MAX_DURATION'] * 60 * 1000])
    )
    rv.headers['content-type'] = 'application/json'
    return rv

@app.route('/likes')
def likes():
    if 'access_token' not in flask.session:
        return flask.abort(401)
    else:
        number_of_likes = flask.g.client.get('/me').public_favorites_count
        likes = soundcloudr.playlist.Playlist(
            flask.g.client, None, number_of_likes
        ).likes
        rv = flask.make_response(
            json.dumps([track['id'] for track in likes
            if track['duration'] <= app.config['MAX_DURATION'] * 60 * 1000])
        )
        rv.headers['content-type'] = 'application/json'
        return rv

@app.route('/playposition', methods=['POST'])
def playposition():
    play_position = flask.request.form['last_played']
    user = PlayPosition.query.filter_by(user=flask.session['username']).first()
    if not user:
        user = PlayPosition(flask.session['username'])
        db.session.add(user)
    user.track_id = play_position
    db.session.commit()
    return 'OK'

@app.before_request
def generate_client():
    if 'access_token' in flask.session:
        token = flask.session['access_token']
        client = soundcloud.Client(client_id = app.config['CLIENT_ID'],
                               client_secret = app.config['CLIENT_SECRET'],
                               access_token = token,
                               redirect_uri = flask.url_for('authorize', _external=True))
        flask.g.client = client
    else:
        client = soundcloud.Client(client_id = app.config['CLIENT_ID'],
                               client_secret = app.config['CLIENT_SECRET'],
                               redirect_uri = flask.url_for('authorize', _external=True))
        flask.g.client = client
