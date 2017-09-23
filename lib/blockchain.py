#!/usr/bin/env python3

# lib/blockchain.py

import hashlib
import json
import sys
import random

class InvalidTransaction(Exception):
    pass


class Blockchain(object):

    def __init__(self, name):
        self.id = name
        self.state = {"": ""}
        self.chain = [self._create_genesis_block()]

    def _create_genesis_block(self):
        genesis_blk_contents = {
                u'blockNumber': 0,
                u'parentHash': None,
                u'txnCount': 1,
                u'txns': self.state
                }
        genesis_hash = self._hash(msg=genesis_blk_contents)
        genesis_block = {
                u'hash': genesis_hash,
                u'contents': genesis_blk_contents
                } 
        genesis_block_str = json.dumps(genesis_block, sort_keys=True)
        return genesis_block

    def _hash(self, msg=""):
        if not isinstance(msg, str):
            msg = json.dumps(msg, sort_keys=True)
        if sys.version_info.major == 2:
            return unicode(hashlib.sha256(msg).hexdigest(), 'utf-8')
        else:
            return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

    def _make_txn(self, msg):
        return {self.id: "%s\n" % msg}

    def _update_state(self, txn):
        self.state.copy()
        for key in txn:
            if key in self.state.keys():
                self.state[key] += txn[key]
            else:
                self.state[key] = txn[key]

    def _is_valid_txn(self, txn):
        for key in txn.keys():
            if not isinstance(txn[key], str):
                return False
        return True

    def _append_block(self, block):
        self.chain.append(block)

    def _make_block(self, txn):
        parent = self.chain[-1]
        parent_hash = parent[u'hash']
        block_number = parent[u'contents'][u'blockNumber'] + 1
        block_contents = {
                u'blockNumber':block_number,
                u'parentHash':parent_hash,
                u'txnCount': 1,
                'txns':txn
                }
        block_hash = self._hash(block_contents)
        block = {u'hash':block_hash,u'contents':block_contents}
        return block

    def send_block(self, msg):
        txn = self._make_txn(msg)
        if self._is_valid_txn(txn):
            block = self._make_block(txn)
            self.chain.append(block)
            return block
        else:
            raise InvalidTransaction

    def recv_block(self, block):
        self.chain.append(block)
