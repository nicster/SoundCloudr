# -*- coding: utf8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import sys
import json
import pyglet

import requests

TOKEN = '1-97489-6257437-80f8de20636a16b3'
API_BASE = 'https://api.soundcloud.com'

class Playlist():
    def __init__(self):
        r = requests.get(
            API_BASE + '/me/activities/tracks/affiliated.json?oauth_token=' +
            TOKEN + '&limit=10&filter=streamable'
        )
        if not r.ok:
            r.raise_for_status()
        self.data = r.json()
        self.tracks = self.fetch_tracks(self.data)
        self.current_track = None

    def fetch_tracks(self, data):
        tracks = []
        tracks.append({'next_href': data['next_href']})

        for track in data['collection']:
            tracks.insert(0, {
                'id': track['origin']['id'],
                'duration': track['origin']['duration'],
                'genre': track['origin']['genre'],
                'description': track['origin']['description'],
                'downloadable': track['origin']['downloadable'],
                'stream_url': track['origin']['stream_url'],
                'permalink': track['origin']['permalink']
            })
        return tracks

    def play(self):
        self.current_track = self.tracks[0]
        stream_url = self.current_track['stream_url']
        r = requests.get(stream_url + '?oauth_token=' +
            TOKEN, stream=True)
        for line in r.iter_lines():
            if line:
                print line
        #print json.dumps(self.tracks, indent=2, sort_keys=True)

    def stop(self):
        self.current_track = None

    def get_current_track(self):
        if self.current_track is not None:
            return self.current_track
        else:
            print ("Nothing is playing right now. " +
                  "Go on and start playing some music!")

class Controller():

    def __init__(self):
        self.playlist = Playlist()

    def help_(self):
        print 'This is the help page'

    def exit_(self):
        sys.exit(1)

    def listen_for_command(self):
        io = raw_input()
        self.parse_command(io)

    def parse_command(self, command):
        commands = {
            'help': self.help_,
            'exit': self.exit_,
            'play': self.playlist.play,
            'current': self.playlist.get_current_track
        }
        commands[command]()

def main():
    controller = Controller()
    print 'Please enter a command. For a list of available commands type help'
    while True:
        print '>>',
        controller.listen_for_command()

if __name__ == "__main__":
    main()
