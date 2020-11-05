import hashlib as hasher
from PoWAlgo import generate_pow


class Block:

    # The initialisation function allows the setting up of a block
    def __init__(self, index, timestamp, supply_data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.supply_data = supply_data
        self.previous_hash = previous_hash
        self.proof_of_work = int(generate_pow())
        self.hash = self.hash_block()

    # The hashing function for the block using SHA 256
    def hash_block(self):
        sha = hasher.sha256()

        sha.update((str(self.index) +
                    str(self.timestamp) +
                    str(self.supply_data) +
                    str(self.previous_hash)).encode('utf-8'))

        return sha.hexdigest()
