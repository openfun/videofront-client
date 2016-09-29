#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

def read(*paths):
    """ read files """
    with open(os.path.join(*paths), 'r') as filename:
        return filename.read()

setup(
    name="videofront-client",
    version="0.0.1",
    description="Videofront client library and CLI utilities",
    long_description=(read('README.md')),
    url="https://github.com/openfun/videofront-client",
    install_requires=[
        "requests[security]",
    ],
    license='AGPL',
    author="FUN-MOOC",
    author_email="admin@fun-mooc.fr",
    packages=['videofront'],
    entry_points={
        'console_scripts': [
            'videofront-getauthtoken=videofront.cli:get_auth_token',

            'videofront-searchplaylists=videofront.cli:search_playlists',
            'videofront-createplaylists=videofront.cli:create_playlist',
            'videofront-deleteplaylists=videofront.cli:delete_playlists',

            'videofront-uploadvideo=videofront.cli:upload_video',
            'videofront-deletevideos=videofront.cli:delete_videos',

            'videofront-uploadsubtitle=videofront.cli:upload_subtitle',
        ],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
