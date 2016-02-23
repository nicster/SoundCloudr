# -*- coding: utf8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import urlparse

import gevent
import gevent.pool


class Playlist(object):
    def __init__(self, client, last_track=None, number_of_likes=None):
        self.client = client
        self.last_track = last_track
        self.tracks = reversed(self.fetch_tracks())
        if number_of_likes is not None:
            self.likes = self.fetch_likes(number_of_likes)

    def fetch_tracks(self, tracks=None, cursor=None):
        if tracks is None:
            tracks = []
        data = self.client.get(
            '/me/activities/tracks/affiliated', cursor=cursor
        )

        for track in data.collection:
            if getattr(getattr(track, 'origin'), 'id') == self.last_track or len(tracks) >= 60:
                break
            tracks.append({
                'id': getattr(getattr(track, 'origin'), 'id'),
                'title': getattr(getattr(track, 'origin'), 'title'),
                'duration': getattr(getattr(track, 'origin'), 'duration'),
                'genre': getattr(getattr(track, 'origin'), 'genre'),
                'description': getattr(getattr(track, 'origin'), 'description'),
                'downloadable': getattr(getattr(track, 'origin'), 'downloadable'),
                'permalink_url': getattr(getattr(track, 'origin'), 'permalink_url')
            })
        else:
            self.fetch_tracks(tracks, self.extract_cursor(data.next_href))
        return tracks

    def fetch_likes(self, number_of_likes):
        likes = []
        pool = gevent.pool.Pool(10)

        for request in pool.imap(self.api_request, range(0, number_of_likes, 100)):
            for track in request:
                likes.append({
                    'id': track.id,
                    'title': track.title,
                    'duration': track.duration,
                    'genre': track.genre,
                    'description': track.description,
                    'downloadable': track.downloadable,
                    'permalink_url': track.permalink_url
                })
        return likes

    def api_request(self, offset):
        return self.client.get('/me/favorites', limit=100, offset=offset)

    def extract_cursor(self, url):
        query = urlparse.urlparse(url).query
        params = urlparse.parse_qs(query)
        cursor = params['cursor'][0]
        return cursor
