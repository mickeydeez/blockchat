#!/usr/bin/env python3

# runner.py

from lib.client import Client
from argparse import ArgumentParser
import sys

def run():
    args = parse_args()
    if args.listener:
        conn = Client(args.name)
        conn.run()
    else:
        conn = Client(args.name, listener=False)
        conn.run()

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-n',
        '--name',
        action='store',
        dest='name',
        help='Alias to use for this client'
    )
    parser.add_argument(
        '-l',
        '--listen',
        action='store_const',
        const=True,
        dest='listener',
        help="Specify to make this client the listener"
    )
    args = parser.parse_args()
    if not args.name:
        parser.print_help()
        sys.exit(1)
    return args

if __name__ == '__main__':
    run()
