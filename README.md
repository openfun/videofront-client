# Videofront client

This is a client for Videofront

## Install

    pip install -e https://github.com/openfun/videofront-client.git@master#egg=videofront-client

## Usage

Upload a video:

    videofront-uploadvideo --host=http://videofront.myhost.com --token=mytoken /path/to/my/video.mp4

The remote host and authentication tokens may be stored in environment variables for shorter CLI:

    export VIDEOFRONT_HOST=http://videofront.myhost.com
    export VIDEOFRONT_TOKEN=myauthenticationtoken
