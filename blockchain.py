from hashlib import sha256 # import sha256 from hashlib
from datetime import datetime # import datetime

now = datetime.now() # get the current time
time = now.strftime("%d/%m/%Y %H:%M:%S") # format the time

# Takes in any number of arguments and produces a sha256 hash as a result
def updatehash(*args):
    """
    Takes in any number of arguments and produces a sha256 hash as a result.

    Args:
    - args: Any number of arguments to be hashed.

    Returns:
    - The sha256 hash of the concatenated arguments.
    """
    hashing_text = ""
    h = sha256() # initialize sha256

    # loop through each argument and hash
    for arg in args:
        hashing_text += str(arg) # concatenate the argument

    h.update(hashing_text.encode('utf-8')) # update the hash
    return h.hexdigest() # return the hash

# The "node" of the blockchain. Points to the previous block by its unique hash in previous_hash.
class Block():
    """
    A class representing a block in the blockchain.
    Attributes:
    - number: The number of the block.
    - previous_hash: The hash of the previous block.
    - sender: The sender of the transaction.
    - recipient: The recipient of the transaction.
    - amount: The amount of the transaction.
    - nonce: The nonce value of the block.

    Methods:
    - hash: Returns the sha256 hash of the block's data.
    - __str__: Returns a string representation of the block's data.
    """
    def __init__(self, number=0, previous_hash="0"*64, sender=None, recipient=None, amount=None, nonce=0):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.number = number
        self.previous_hash = previous_hash
        self.nonce = nonce

    def hash(self):
        """
        Returns the sha256 hash of the block's data.

        Returns:
        - The sha256 hash of the block's data.
        """
        return updatehash(
            self.number,
            self.previous_hash,
            self.sender,
            self.recipient,
            self.amount,
            self.nonce
        )

    def __str__(self):
        """
        Returns a string representation of the block's data.

        Returns:
        - A string representation of the block's data.
        """
        return str("Block#: %s\nHash: %s\nPrevious: %s\nSender: %s\nRecipient: %s\nAmount: %s\nNonce: %s\n" % (
            self.number,
            self.hash(),
            self.previous_hash,
            self.sender,
            self.recipient,
            self.amount,
            self.nonce
        ))


# The "LinkedList" of the blocks - a chain of blocks.
class Blockchain():
    """
    A class representing a blockchain.

    Attributes:
    - difficulty: The number of zeros in front of each hash.
    - chain: A list representing the blocks in the blockchain.

    Methods:
    - __init__: Initializes a new blockchain.
    - add: Adds a new block to the chain.
    - remove: Removes a block from the chain.
    - mine: Finds the nonce of the block that satisfies the difficulty and adds it to the chain.
    - isValid: Checks if the blockchain is valid.
    """
    difficulty = 4

    def __init__(self):
        self.chain = []

    def add(self, block):
        """
        Adds a new block to the chain.

        Args:
        - block: The block to be added to the chain.
        """
        self.chain.append(block)

    def remove(self, block):
        """
        Removes a block from the chain.

        Args:
        - block: The block to be removed from the chain.
        """
        self.chain.remove(block)

    def mine(self, block):
        """
        Finds the nonce of the block that satisfies the difficulty and adds it to the chain.

        Args:
        - block: The block to be mined.
        """
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block)
                break
            else:
                block.nonce += 1

    def isValid(self):
        """
        Checks if the blockchain is valid.

        Returns:
        - True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i-1].hash()
            if _previous != _current or _current[:self.difficulty] != "0"*self.difficulty:
                return False

        return True
