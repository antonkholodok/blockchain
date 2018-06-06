import hashlib
import json
from textwrap import dedent
from time import time
from urllib.parse import urlparse

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        
        # genesis block
        self.new_block(previous_hash=1, proof=100)

    def register_node(self, address):

        '''
        Adds new node to list of nodes.

        :param address: <str> Address of node (http://192.168.0.5:5000)
        :return: None
        '''

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url)

    def proof_of_work(self, last_proof):

        '''
        Simple PoW algorithm:
        - find number p' such that hash(pp') contains 4 leading zeros
        - p is previous proof, p' is new
        
        :param last_proof: <int>
        :return: <int>
        '''

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    def valid_proof(self, last_proof, proof):

        '''
        Proof validation:
        - hash(last_proof, proof) should contain 4 leading zeros

        :param last_proof: <int>
        :param proof: <int>
        :return: <bool> True if valid, Fails if not
        '''

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    def new_block(self, proof, previous_hash=None):
        
        '''
        Create a new Block in the Blockchain

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        '''

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block


    def new_transaction(self, sender, recipient, amount):
        
        '''
        Creates a new transaction to go into the next mined Block

        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        '''

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        
        '''
        Creates SHA-256 hash of a Block

        :param block: <dict> Block
        :return: <str>
        '''

        # we must make sure that the dictionary is ordered
        # or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]