#!/usr/bin/env python3

# runner.py

from lib.blockchain import Blockchain
from lib.client import Connection
import sys
import pprint

host = ''
port = 4444

def run():
    if sys.argv[1] == 'listener':
        conn = Connection(host, port)
        conn.start()
    else:
        conn = Connection(host, port, listener=False)
        conn.start()

if __name__ == '__main__':
    run()
