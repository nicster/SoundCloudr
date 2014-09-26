# -*- coding: utf8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import sys
import soundcloud

TOKEN = '1-97489-6257437-80f8de20636a16b3'

def help_():
    print 'This is the help page'

def exit_():
    sys.exit(1)

def listen_for_command():
    io = raw_input()
    parse_command(io)

def parse_command(command):
    commands[command]()

commands = {
    'help': help_,
    'exit': exit_
}

def main():
    print 'Please enter a command. For a list of available commands type help'
    while True:
        listen_for_command()

if __name__ == "__main__":
    main()
