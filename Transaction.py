from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


class Transaction:

    # The initialisation function for a single transaction
    def __init__(self, supplier_puk, receiver_puk, item_id, timestamp, signature):
        self.supplier_puk = supplier_puk
        self.receiver_puk = receiver_puk
        self.item_id = item_id
        self.timestamp = timestamp
        self.signature = signature

    # This function is used for the verifying the signature of the transaction

    def verify_transaction(self):
        supplier_puk = RSA.import_key(self.supplier_puk.exportKey("DER"))

        message = str(self.supplier_puk.exportKey("PEM").decode('utf-8')) + \
            str(self.receiver_puk) + self.item_id + str(self.timestamp)
        hash_message = SHA256.new(message.encode('utf-8'))

        try:
            pkcs1_15.new(supplier_puk).verify(hash_message, self.signature)
            return True
        except (ValueError, TypeError):
            return False

    # Smart contract for checking if the input item code is avaiable on the blockchain & checking the previous owner of the consignment
    def check_item_code(self, blockchainObj):
        found_flag = False
        temp_blockchain = blockchainObj.blockchain[::-1]

        for block in temp_blockchain[:-1:]:
            for transaction in block.supply_data:
                if(transaction.item_id == self.item_id):
                    found_flag = True

        return found_flag

    # Smart contract for checking the previous owner of the commodity
    def check_previous_owner(self, blockchainObj):
        temp_blockchain = blockchainObj.blockchain[::-1]

        for block in temp_blockchain[:-1:]:
            for transaction in block.supply_data:
                if(transaction.item_id == self.item_id):
                    if(transaction.receiver_puk == self.supplier_puk.exportKey("PEM").decode('utf-8')):
                        return True
                    else:
                        return False

    # Smart contract for checking if the user is an authorised manufacturer
    def check_manufacturer_credentials(self, blockchainObj):
        for item in blockchainObj.manufacturers_list:
            if str(self.supplier_puk.exportKey("PEM").decode('utf-8')) == str(item.publickey().exportKey("PEM").decode('utf-8')):
                return True

        return False
