# -*- coding: utf8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import os
import json
import random

import webbrowser

API_BASE = 'https://api.soundcloud.com'
HOME =  os.getenv('HOME')

class Playlist(object):
    def __init__(self, client):
        data = client.get(
                    '/me/activities/tracks/affiliated'
                )
        self.tracks = self.fetch_tracks(data, [])
        self.current_track = None

    def fetch_tracks(self, data, tracks):
        tracks.append({'next_href': data.next_href})

        for track in data.collection:
            tracks.insert(0, {
                'id': track['origin']['id'],
                'title': track['origin']['title'],
                'duration': track['origin']['duration'],
                'genre': track['origin']['genre'],
                'description': track['origin']['description'],
                'downloadable': track['origin']['downloadable'],
                'stream_url': track['origin']['stream_url'],
                'permalink_url': track['origin']['permalink_url']
            })
        return tracks

    def play(self):
        print len(self.tracks)
        #print json.dumps(self.tracks , indent=2, sort_keys=True)
        self.current_track = self.tracks.pop(0)
        '''print ('You played all your unplayed tracks. If you want you can ' +
               "play your liked tracks with the 'play liked' command")

        stream_url = self.current_track['stream_url']
        r = requests.get(stream_url + '?oauth_token=' +
            TOKEN, stream=True)
        for line in r.iter_lines():
            if line:
                print line'''

    def next(self):
        self.current_track = None
        self.play()

    def show(self):
        for track in self.tracks:
            print track['title']

    def open(self):
        webbrowser.open(self.current_track['permalink_url'])

    def play_liked(self):
        request = (
            API_BASE + '/me.json?oauth_token=' + TOKEN
        )
        data = self.api_request(request)
        number_of_likes = data['public_favorites_count']
        request = (
            API_BASE + '/me/favorites.json?oauth_token=' + TOKEN +
            '&limit=' + str(number_of_likes)
        )
        data = self.api_request(request)
        print json.dumps(data, indent=2, sort_keys=True)
        tracks = []
        for track in data:
            tracks.insert(0, {
                'id': track['id'],
                'title': track['title'],
                'duration': track['duration'],
                'genre': track['genre'],
                'description': track['description'],
                'downloadable': track['downloadable'],
                'permalink': track['permalink'],
                #'stream_url': track['stream_url']
            })
        print json.dumps(tracks, indent=2, sort_keys=True)
        next_track = random.randrange(1, number_of_likes)



    def stop(self):
        with open(
                  os.path.join(HOME + "/Downloads/",
                               ".last_listened.json"), "w"
                 ) as f:
            json.dump(self.current_track, f)
        self.current_track = None

    def get_current_track(self):
        if self.current_track is not None:
            print self.current_track['title']
        else:
            print ("Nothing is playing right now. " +
                  "Go on and start playing some music!")
