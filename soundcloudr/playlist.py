# -*- coding: utf8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import os
import re
import json

import requests

TOKEN = '1-97489-6257437-80f8de20636a16b3'
API_BASE = 'https://api.soundcloud.com'
HOME =  os.getenv('HOME')

class Playlist():
    def __init__(self):
        r = requests.get(
            API_BASE + '/me/activities/tracks/affiliated.json?oauth_token=' +
            TOKEN + '&filter=streamable'
        )
        if not r.ok:
            r.raise_for_status()
        self.data = r.json()
        json_data = open(HOME + "/Downloads/.last_listened.json")
        last = json.load(json_data)['id']
        self.tracks = self.fetch_tracks(self.data, last)
        self.current_track = None

    def fetch_tracks(self, data, last, flag = False, tracks = []):
        tracks.append({'next_href': data['next_href']})

        for track in data['collection']:
            if track['origin']['id'] == last:
                flag == True
                continue
            tracks.insert(0, {
                'id': track['origin']['id'],
                'title': track['origin']['title'],
                'duration': track['origin']['duration'],
                'genre': track['origin']['genre'],
                'description': track['origin']['description'],
                'downloadable': track['origin']['downloadable'],
                'stream_url': track['origin']['stream_url'],
                'permalink': track['origin']['permalink']
            })
        if flag == False:
            next_r = tracks.pop()
            url = re.split('affiliated', next_r['next_href'])
            request = (
                    API_BASE +
                    '/me/activities/tracks/affiliated.json?oauth_token=' +
                    TOKEN + '&' + url[1][1:]
                   )
            data = requests.get(request).json()
            self.fetch_tracks(data, last, tracks)



        return tracks

    def play(self):
        #print json.dumps(self.tracks, indent=2, sort_keys=True)
        while len(self.tracks)>0:
            self.current_track = self.tracks.pop(0)
        print ('You played all your unplayed tracks. If you want you can ' +
               "play your liked tracks with the 'play liked' command")

        '''stream_url = self.current_track['stream_url']
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

    def like(self):
        return 0

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
