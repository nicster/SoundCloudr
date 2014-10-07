# -*- coding: utf8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import sys

from blessings import Terminal

import soundcloudr.playlist

class Controller():

    def __init__(self):
        self.playlist = soundcloudr.playlist.Playlist()

    def help_(self):
        help_page = '''
        HELP PAGE:

        COMMANDS:
        play:       Play the newest tracks
        next:       Play the next track
        current:    Show the current track playing
        show:       Show available tracks
        like:       Like the current track playing
        stop:       Stop playing music
        exit:       Close the program
        '''
        print help_page

    def listen_for_command(self):
        io = raw_input()
        if io == 'exit':
            sys.exit(1)
        else:
            try:
                self.parse_command(io)
            except:
                print ('Please enter a valid command. ' +
                       'For further information type help')


    def parse_command(self, command):
        commands = {
            'help': self.help_,
            'play': self.playlist.play,
            'current': self.playlist.get_current_track,
            'next': self.playlist.next,
            'like': self.playlist.like,
            'stop': self.playlist.stop,
            'show': self.playlist.show
        }
        commands[command]()

def main():
    term = Terminal()
    controller = Controller()
    print 'Please enter a command. For a list of available commands type help'
    while True:
        print term.bright_red('>>'),
        controller.listen_for_command()

if __name__ == "__main__":
    main()
