#!/usr/bin/env python
import argparse
import os
from time import sleep
import requests

from . import cli


def main():
    parser = argparse.ArgumentParser(description='Upload a video file')
    parser.add_argument('--playlist', help='Playlist ID to which the video should be added')
    parser.add_argument('video', help='Path to video file')
    cli.add_auth_arguments(parser)
    args, client = cli.parse_args(parser)
    video_path = args.video

    # Get upload url
    data = {
        'filename': os.path.basename(video_path)
    }
    if args.playlist:
        data['playlist_id'] = args.playlist
    upload_url = client.post('videouploads/', data=data).json()

    # Upload the file
    method = upload_url['method'].lower()
    url = upload_url['url']
    video_id = upload_url['id']
    func = getattr(requests, method)
    _upload_response = func(url, data=open(video_path).read())

    # Monitor transcoding progress
    video = client.get('videos/' + video_id).json()
    title = video['title']
    video_id = video['id']
    print(u"Video uploaded: id={} title='{}'".format(video_id, title))
    message = None
    status = None
    while status is None or status in ['processing', 'pending']:
        sleep(1) # don't flood the server
        video = client.get('videos/' + video_id).json()
        status_details = video['status_details']
        if status_details:
            status = status_details['status']
            new_message = "    {} {:.2f}%".format(status, status_details['progress'])
        else:
            new_message = "    status unknown"
        if message != new_message:
            message = new_message
            print(message)

    for video_format in video['formats']:
        print("    {}: {}".format(video_format['name'], video_format['streaming_url']))


if __name__ == '__main__':
    main()
