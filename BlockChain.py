import time
import hashlib as hasher
import datetime as date
import random

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Signature import pkcs1_15

from Block import Block
from Transaction import Transaction


class BlockChain:

    def __init__(self):
        self.blockchain = []
        self.utxo_array = []
        self.manufacturers_list = []
        self.other_users_list = []
        self.global_index = 0
        self.pow_proof = int(0)

    # The function would verify all the blocks in the given blockchain

    def verify_blockchain(self):
        previous_block = self.blockchain[0]
        count = 1

        for block in self.blockchain[1:]:
            print('\nFor the block #' + str(count) + ': ')
            for transaction in block.supply_data:
                print('The item ID is ' + str(transaction.item_id) +
                      ' and the associated timestamp is ' + str(transaction.timestamp))

            if(str(previous_block.hash) == str(block.previous_hash)):
                print('The hash values have been verified.')

            sha = hasher.sha256()
            sha.update(str(int(block.proof_of_work)).encode('utf-8'))
            hash_value = sha.hexdigest()
            print('The PoW number is ' + str(block.proof_of_work) +
                  ' and the associated hash is ' + hash_value)

        print('------------------------------------------------------------------------------------------------------------------------')
        print('\n\n')


    # Function for generating manufacturer keys

    def generate_manufacturer_keys(self, number):
        for item in range(0, int(number)):
            self.manufacturers_list.append(
                RSA.generate(1024, Random.new().read))
        # print(self.manufacturers_list)
        print('\nThe manufacturer keys have been generated.')

    # Function for generating stakeholder keys

    def generate_other_keys(self, number):
        for item in range(0, int(number)):
            self.other_users_list.append(RSA.generate(1024, Random.new().read))
        # print(self.other_users_list)
        print('\nThe stakeholder keys have been generated.')

    # Function for tracking an item

    def track_item(self, item_code):
        not_found_flag = True

        for block in self.blockchain[1:]:
            for transaction in block.supply_data:
                if(item_code == transaction.item_id):
                    if(not_found_flag):
                        print('\nThe item (' + item_code +
                              ') has been found and the tracking details are: ')
                        not_found_flag = False

                    manufacturer_suppplier = False
                    manufacturer_receiver = False

                    supplier_count = 0
                    supplier_not_found_flag = True

                    for item in self.manufacturers_list:
                        supplier_count = supplier_count + 1

                        if str(transaction.supplier_puk.exportKey("PEM").decode('utf-8')) == str(item.publickey().exportKey("PEM").decode('utf-8')):
                            supplier_not_found_flag = False
                            manufacturer_suppplier = True
                            break

                    if(supplier_not_found_flag):
                        supplier_count = 0

                        for item in self.other_users_list:
                            supplier_count = supplier_count + 1

                            if str(transaction.supplier_puk.exportKey("PEM").decode('utf-8')) == str(item.publickey().exportKey("PEM").decode('utf-8')):
                                supplier_not_found_flag = False
                                break

                    receiver_count = 0
                    receiver_not_found_flag = True

                    for item in self.manufacturers_list:
                        receiver_count = receiver_count + 1

                        if str(transaction.receiver_puk) == str(item.publickey().exportKey("PEM").decode('utf-8')):
                            receiver_not_found_flag = False
                            manufacturer_receiver = True
                            break

                    if(receiver_not_found_flag):
                        receiver_count = 0

                        for item in self.other_users_list:
                            receiver_count = receiver_count + 1

                            if str(transaction.receiver_puk) == str(item.publickey().exportKey("PEM").decode('utf-8')):
                                receiver_not_found_flag = False
                                break

                    final_result = ""

                    if(manufacturer_suppplier):
                        final_result = final_result + "Manufacturer #" + \
                            str(supplier_count) + " transferred the asset to "
                    else:
                        final_result = final_result + "Stakeholder #" + \
                            str(supplier_count) + " transferred the asset to "

                    if(manufacturer_receiver):
                        final_result = final_result + "Manufacturer #" + \
                            str(receiver_count) + " at " + \
                            str(transaction.timestamp)
                    else:
                        final_result = final_result + "Stakeholder #" + \
                            str(receiver_count) + " at " + \
                            str(transaction.timestamp)

                    print(final_result)

        if(not_found_flag):
            print('\nThe item code was not found in the blockchain.')

    # This function is used for viewing all the blocks and the transactions in the blockchain

    def view_blockchain(self):
        print('\n\nThe list of blocks are: \n')
        for block in self.blockchain:
            print('\n------------------------------------------------------------------------------------------------------------------------')
            print(block.index)
            print(block.timestamp)
            print(block.supply_data)
            print(block.proof_of_work)
            print(block.hash)
            print(block.previous_hash)
        print('------------------------------------------------------------------------------------------------------------------------')
        print('\n\n')

    # This function is used to view all the Unspend Transaction Outputs

    def view_UTXO(self):
        print('\n\nThe list of UTXO are: \n')
        for transaction in self.utxo_array:
            print('\n------------------------------------------------------------------------------------------------------------------------')
            print(transaction.supplier_puk.exportKey("PEM").decode('utf-8'))
            print(transaction.receiver_puk)
            print(transaction.item_id)
            print(transaction.timestamp)
            print(transaction.signature)
        print('------------------------------------------------------------------------------------------------------------------------')
        print('\n\n')

    # This function is used to generate a transaction

    def make_transaction(self, supplier_key, receiver_key, item_id):

        # Selection functions for the keys and the item ID
        selection = input('\nSelect type of key (M/O) for supplier: ')
        if selection == 'M':
            index = int(input('There are a total of ' +
                              str(len(self.manufacturers_list)) + ' users. Enter your selection: ')) - 1
            supplier_key = self.manufacturers_list[index]

        elif selection == 'O':
            index = int(input('There are a total of ' +
                              str(len(self.other_users_list)) + ' users. Enter your selection: ')) - 1
            supplier_key = self.other_users_list[index]

        selection = input('\nSelect type of key (M/O) for receiver: ')
        if selection == 'M':
            index = int(input('There are a total of ' +
                              str(len(self.manufacturers_list)) + ' users. Enter your selection: ')) - 1
            receiver_key = self.manufacturers_list[index]

        elif selection == 'O':
            index = int(input('There are a total of ' +
                              str(len(self.other_users_list)) + ' users. Enter your selection: ')) - 1
            receiver_key = self.other_users_list[index]

        receiver_puk = receiver_key.publickey().exportKey("PEM").decode('utf-8')
        item_id = input('Enter the ID of the tracked item: ')

        # Acquiring the details for the transactions
        supplier_puk = supplier_key.publickey()
        timestamp = date.datetime.now()

        # Generating the message text and the signature
        message = str(supplier_puk.exportKey("PEM").decode('utf-8')) + \
            str(receiver_puk) + item_id + str(timestamp)
        hash_message = SHA256.new(message.encode('utf-8'))

        supplier_prk = RSA.import_key(supplier_key.exportKey("DER"))
        signature = pkcs1_15.new(supplier_prk).sign(hash_message)

        # Creating a new transaction
        new_transaction = Transaction(
            supplier_puk, receiver_puk, item_id, timestamp, signature)
        self.utxo_array.append(new_transaction)

    # The function for mining the block in the supply blockchain

    def mine_block(self):
        max_range = len(self.utxo_array)
        transaction_amount = random.randint(0, max_range)
        transaction_array = []

        print('\nThe number of selected transactions for the block is: ' +
              str(transaction_amount))

        if(transaction_amount):
            for index in range(0, transaction_amount):
                # All verifications for the transactions
                if(self.utxo_array[0].verify_transaction()):
                    print('\nThe sign verification for transaction #' +
                          str(index + 1) + ' was true!')
                    if(self.utxo_array[0].check_item_code(self)):
                        print(
                            'The item code has been found. Checking the previous owner details.')
                        if(self.utxo_array[0].check_previous_owner(self)):
                            print('Verification of previous owner has been done!')
                            transaction_array.append(self.utxo_array[0])
                        else:
                            print('Verification of previous owner has failed!')
                    else:
                        print(
                            'The item code was not found on blockchain. Checking for manufacturer credentials.')
                        if(self.utxo_array[0].check_manufacturer_credentials(self)):
                            print(
                                'The new item has been added under the manufacturer.')
                            transaction_array.append(self.utxo_array[0])
                        else:
                            print(
                                'The transaction key is not authorised as a manufacturer!')
                else:
                    print('The sign verification for transaction #' +
                          str(index + 1) + ' was false!')
                self.utxo_array.pop(0)

            if(len(transaction_array) != 0):
                new_block = Block(self.global_index, date.datetime.now(
                ), transaction_array, self.blockchain[self.global_index - 1].hash)
                self.global_index = self.global_index + 1
                self.blockchain.append(new_block)
            else:
                # Prevent addition of blocks with no transactions
                print(
                    'No transactions have been selected and therefore no block has been added!')

    def add_block(self, block):
        self.blockchain.append(block)

    # This function is used to create genesis block

    def create_genesis_block(self):
        self.global_index = self.global_index + 1
        print('\n\nThe genesis block is being created.')

        return Block(0, date.datetime.now(), "GENESIS BLOCK", "0")
