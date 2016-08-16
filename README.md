# Videofront client

This is a client for Videofront

## Install

    pip install -e https://github.com/openfun/videofront-client.git@master#egg=videofront-client

## Usage

Obtain an authentication token:

    videofront-getauthtoken --host=http://videofront.myhost.com --username=myusername --password=mypassword

The remote host and authentication tokens may be stored in environment variables for shorter CLI:

    export VIDEOFRONT_HOST=http://videofront.myhost.com
    export VIDEOFRONT_TOKEN=myauthenticationtoken


Create a playlist:

    videofront-createplaylist myplaylistname

Search existing playlists:

    videofront-searchplaylists myplaylistname

Delete a playlist:

    videofront-deleteplaylists myplaylistname

Upload a video, optionally to a playlist:

    videofront-uploadvideo --playlist=playlist_id /path/to/my/video.mp4

Delete a video:

    videofront-deletevideo myvideoid
