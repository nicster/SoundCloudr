# -*- coding: utf8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

from setuptools import setup

setup(
    name = "Soundcloudr",
    version = "1.1",
    description = "Listen to your Soundcloud feed and to your likes",
    url = '',
    author = "Nicolas Spycher",
    author_email = "nic.spycher@gmail.com",
    license = "WTFPL",
    zip_safe = True,
    install_requires = ("soundcloud"),
)
