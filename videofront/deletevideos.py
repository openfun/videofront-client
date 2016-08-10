#!/usr/bin/env python
import argparse

from . import cli
from .client import HttpError


def main():
    parser = argparse.ArgumentParser(description='Delete a video')
    cli.add_auth_arguments(parser)
    parser.add_argument('video_ids', nargs='+', help='Video IDs')
    args, client = cli.parse_args(parser)

    for video_id in args.video_ids:
        try:
            response = client.delete('videos/' + video_id)
        except HttpError as e:
            print(u"Failed to delete video: id={} error={}".format(video_id, e.message))
        else:
            print(u"Video deleted: id={} status code={}".format(video_id, response.status_code))

if __name__ == '__main__':
    main()
