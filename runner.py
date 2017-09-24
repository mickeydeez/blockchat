#!/usr/bin/env python3

# runner.py

from lib.server import ChatServer
from argparse import ArgumentParser
import sys

def run():
    args = parse_args()
    if args.listener:
        conn = ChatServer()
    else:
        from lib.kclient import ClientApp
        conn = ClientApp(alias=sys.argv[1]).run()

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-l',
        '--listen',
        action='store_const',
        const=True,
        dest='listener',
        help="Specify to make this client the listener"
    )
    args, unknown = parser.parse_known_args()
    return args

if __name__ == '__main__':
    run()
