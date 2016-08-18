import argparse
import os
from time import sleep

import requests

from .client import Client, HttpError

def get_auth_token():
    parser = argparse.ArgumentParser(description='Obtain an authentication token')
    add_auth_arguments(parser)
    _args, client = parse_args(parser)

    print("Authentication token: {}".format(client.token))

def upload_video():
    parser = argparse.ArgumentParser(description='Upload a video file')
    parser.add_argument('--playlist', help='Playlist ID to which the video should be added')
    parser.add_argument('video', help='Path to video file')
    add_auth_arguments(parser)
    args, client = parse_args(parser)
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


def delete_videos():
    parser = argparse.ArgumentParser(description='Delete a video')
    add_auth_arguments(parser)
    parser.add_argument('video_ids', nargs='+', help='Video IDs')
    args, client = parse_args(parser)

    for video_id in args.video_ids:
        try:
            response = client.delete('videos/' + video_id)
        except HttpError as e:
            print(u"Failed to delete video: id={} error={}".format(video_id, e.message))
        else:
            print(u"Video deleted: id={} status code={}".format(video_id, response.status_code))

def search_playlists():
    parser = argparse.ArgumentParser(description='Search playlists that have a given name')
    add_auth_arguments(parser)
    parser.add_argument('name', help='Playlist name')
    args, client = parse_args(parser)

    response = client.get('playlists', params={'name': args.name})
    playlists = response.json()
    print("{} results found".format(len(playlists)))
    for playlist in playlists:
        print("    id={} name='{}'".format(playlist['id'], playlist['name']))

def create_playlist():
    parser = argparse.ArgumentParser(description='Create a playlist')
    add_auth_arguments(parser)
    parser.add_argument('name', help='Playlist name')
    args, client = parse_args(parser)

    response = client.post('playlists/', data={'name': args.name})
    playlist = response.json()
    print(playlist)

def delete_playlists():
    parser = argparse.ArgumentParser(description='Create a playlist')
    add_auth_arguments(parser)
    parser.add_argument('playlist_ids', nargs='+', help='Playlist ID')
    args, client = parse_args(parser)

    for playlist_id in args.playlist_ids:
        client.delete('playlists/{}'.format(playlist_id))
        print("Deleted {}".format(playlist_id))

def add_auth_arguments(parser):
    """
    Add arguments for authenticating with the remote host.
    """
    parser.add_argument('--host', default=os.environ.get('VIDEOFRONT_HOST', 'http://127.0.0.1:8000'),
                        help='Videofront host. You may define the VIDEOFRONT_HOST environment variable instead.')
    parser.add_argument('-t', '--token',
                        help='Authentication token. You may define the VIDEOFRONT_TOKEN environment variable instead.')
    parser.add_argument('-u', '--username', help='Authentication username')
    parser.add_argument('-p', '--password', help='Authentication password')

def parse_args(parser):
    """
    Parse CLI arguments with authentication credentials.
    """
    args = parser.parse_args()

    try:
        client = Client(args.host, token=args.token, username=args.username, password=args.password)
    except ValueError as e:
        raise argparse.ArgumentError(None, e.message)

    return args, client
