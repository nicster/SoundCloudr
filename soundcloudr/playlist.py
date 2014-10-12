# -*- coding: utf8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import os
import urlparse

API_BASE = 'https://api.soundcloud.com'
HOME =  os.getenv('HOME')

class Playlist(object):
    def __init__(self, client, last_track):
        self.client = client
        self.last_track = last_track
        self.tracks = reversed(self.fetch_tracks())

    def fetch_tracks(self, tracks=None, cursor=None):
        if tracks is None:
            tracks = []
        data = self.client.get(
            '/me/activities/tracks/affiliated', cursor=cursor
        )

        for track in data.collection:
            tracks.append({
                'id': track['origin']['id'],
                'title': track['origin']['title'],
                'duration': track['origin']['duration'],
                'genre': track['origin']['genre'],
                'description': track['origin']['description'],
                'downloadable': track['origin']['downloadable'],
                'stream_url': track['origin']['stream_url'],
                'permalink_url': track['origin']['permalink_url']
            })
            if track['origin']['id'] == self.last_track:
                break
        else:
            self.fetch_tracks(tracks, self.extract_cursor(data.next_href))
        return tracks

    def extract_cursor(self, url):
        query = urlparse.urlparse(url).query
        params = urlparse.parse_qs(query)
        cursor = params['cursor'][0]
        return cursor

