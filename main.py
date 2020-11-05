from BlockChain import BlockChain

if __name__ == "__main__":
    blockchain = BlockChain()

    # Generating keys for manufactures and other users
    number_manufacturers = int(input('\nEnter the number of manufacturers: '))
    blockchain.generate_manufacturer_keys(number_manufacturers)

    number_other_users = int(input('\nEnter the number of stakeholders: '))
    blockchain.generate_other_keys(number_other_users)

    # Inserting a genesis block into blockchain
    blockchain.add_block(blockchain.create_genesis_block())
    print('\n\nWelcome to the supply blockchain.')

    # Menu driven program for the supply blockchain
    while(1):
        print('\nThe following options are available to the user: ')
        print('1. View the blockchain. ')
        print('2. Enter a transaction. ')
        print('3. View the UTXO array. ')
        print('4. Mine a block. ')
        print('5. Verify the blockchain. ')
        print('6. Generate RSA keys. ')
        print('7. Track an item.')
        print('8. Exit.')

        choice = int(input('Enter your choice: '))

        if(choice == 1):
            blockchain.view_blockchain()
        elif(choice == 2):
            blockchain.make_transaction('', '', '')
        elif(choice == 3):
            blockchain.view_UTXO()
        elif(choice == 4):
            blockchain.mine_block()
        elif(choice == 5):
            blockchain.verify_blockchain()
        elif(choice == 6):
            number_manufacturers = int(
                input('\nEnter the number of manufacturers: '))
            blockchain.generate_manufacturer_keys(number_manufacturers)
            number_other_users = int(
                input('Enter the number of stakeholders: '))
            blockchain.generate_other_keys(number_other_users)
        elif(choice == 7):
            item_code = input('Enter the item code: ')
            blockchain.track_item(item_code)
        elif(choice == 8):
            break
        else:
            print('This is an invalid option.')
