# -*- coding: utf8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import os

import soundcloudr

def sqlite_url(name):
    return "sqlite:///" + os.path.join(
                                        soundcloudr.app.instance_path,
                                        name + ".sqlite"
                                      )

CLIENT_ID='eacabe21353f6c66901c66b1e8f9ae73'
CLIENT_SECRET='30965f87b5f0fb5468acbf56c85fdd9a'
SECRET_KEY = 'RX3{}7/&pheZU#GJ4mKVkjB7t24o@63FceK)kAdz;jQ?#7f4QL'
SQLALCHEMY_DATABASE_URI = sqlite_url("db")
