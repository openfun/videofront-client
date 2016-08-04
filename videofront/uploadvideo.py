#!/usr/bin/env python
import argparse
import os
from time import sleep
import requests

from .client import Client


def main():
    parser = argparse.ArgumentParser(description='Upload a video file')
    parser.add_argument('--host', default=os.environ.get('VIDEOFRONT_HOST', 'http://127.0.0.1:8000'),
                        help='Videofront host')
    parser.add_argument('-t', '--token', help='Authentication token')
    parser.add_argument('-u', '--username', help='Authentication username')
    parser.add_argument('-p', '--password', help='Authentication password')
    parser.add_argument('video', help='Path to video file')

    args = parser.parse_args()
    video_path = args.video

    try:
        client = Client(args.host, token=args.token, username=args.username, password=args.password)
    except ValueError as e:
        raise argparse.ArgumentError(None, e.message)


    # Get upload url
    upload_url = client.post('videouploads/', data={'filename': os.path.basename(video_path)})

    # Upload the file
    method = upload_url['method'].lower()
    url = upload_url['url']
    video_id = upload_url['id']
    func = getattr(requests, method)
    _upload_response = func(url, data=open(video_path).read())

    # Monitor transcoding progress
    video = client.get('videos/' + video_id)
    title = video['title']
    video_id = video['id']
    print u"Video uploaded: id={} title='{}'".format(video_id, title)
    message = None
    status = None
    while status is None or status in ['processing', 'pending']:
        sleep(1) # don't flood the server
        video = client.get('videos/' + video_id)
        status_details = video['status_details']
        if status_details:
            status = status_details['status']
            new_message = "    {} {:.2f}%%".format(status, status_details['progress'])
        else:
            new_message = "    status unknown"
        if message != new_message:
            message = new_message
            print message


if __name__ == '__main__':
    main()
