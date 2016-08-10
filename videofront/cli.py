import argparse
import os

from .client import Client

def add_auth_arguments(parser):
    """
    Add arguments for authenticating with the remote host.
    """
    parser.add_argument('--host', default=os.environ.get('VIDEOFRONT_HOST', 'http://127.0.0.1:8000'),
                        help='Videofront host')
    parser.add_argument('-t', '--token', help='Authentication token')
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
