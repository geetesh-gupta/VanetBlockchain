# associated medium post: https://medium.com/@ethervolution/ethereum-create-raw-json-rpc-requests-with-python-for-deploying-and-transacting-with-a-smart-7ceafd6790d9
import requests
import json
import web3  # Release 4.0.0-beta.8
import pprint
import time
from eth_utils.address import to_checksum_address, is_checksum_formatted_address, to_hex

# create persistent HTTP connection
session = requests.Session()
w3 = web3.Web3()
pp = pprint.PrettyPrinter(indent=2)

requestId = 0  # is automatically incremented at each request

URL = 'http://localhost:8501'  # url of my geth node
PATH_GENESIS = '/mnt/c/Users/gggui/Documents/VANET/VanetBlockChain/blockchain/genesis.json'
# smart contract path
PATH_SC_TRUFFLE = '/mnt/c/Users/gggui/Documents/VANET/VanetBlockChain/blockchain/python_code'

# extracting data from the genesis file
genesisFile = json.load(open(PATH_GENESIS))
CHAINID = genesisFile['config']['chainId']
PERIOD = genesisFile['config']['clique']['period']
GASLIMIT = int(genesisFile['gasLimit'], 0)

# compile your smart contract with truffle first
truffleFile = json.load(
    open(PATH_SC_TRUFFLE + '/build/contracts/AdditionContract.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# Don't share your private key !
# address funded in genesis file
myAddress = '0x4880AB43beA43Ae0E2A880Aa0ce3c44598130DD0'
myPrivateKey = '0x3890a1911cb0492ed38605c334456dc4fbe598b318fc918602fa38d748c93d31'


''' =========================== SOME FUNCTIONS ============================ '''
# see http://www.jsonrpc.org/specification
# and https://github.com/ethereum/wiki/wiki/JSON-RPC


def createJSONRPCRequestObject(_method, _params, _requestId):
    return {"jsonrpc": "2.0",
            "method": _method,
            # must be an array [value1, value2, ..., valueN]
            "params": _params,
            "id": _requestId}, _requestId+1


def postJSONRPCRequestObject(_HTTPEnpoint, _jsonRPCRequestObject):
    response = session.post(_HTTPEnpoint,
                            json=_jsonRPCRequestObject,
                            headers={'Content-type': 'application/json'})

    return response.json()


''' ======================= DEPLOY A SMART CONTRACT ======================= '''
# get your nonce
requestObject, requestId = createJSONRPCRequestObject(
    'eth_getTransactionCount', [myAddress, 'latest'], requestId)
responseObject = postJSONRPCRequestObject(URL, requestObject)
myNonce = w3.toInt(hexstr=responseObject['result'])
print('nonce of address {} is {}'.format(myAddress, myNonce))

# create your transaction
transaction_dict = {'from': myAddress,
                    'to': '',  # empty address for deploying a new contract
                    'chainId': CHAINID,
                    'gasPrice': 1,  # careful with gas price, gas price below the --gasprice option of Geth CLI will cause problems. I am running my node with --gasprice '1'
                    'gas': 2000000,  # rule of thumb / guess work
                    'nonce': myNonce,
                    'data': bytecode}  # no constrctor in my smart contract so bytecode is enough

# sign the transaction
signed_transaction_dict = w3.eth.account.signTransaction(
    transaction_dict, myPrivateKey)
params = [signed_transaction_dict.rawTransaction.hex()]

# send the transacton to your node
requestObject, requestId = createJSONRPCRequestObject(
    'eth_sendRawTransaction', params, requestId)
responseObject = postJSONRPCRequestObject(URL, requestObject)
try:
    transactionHash = responseObject['result']
    print('contract submission hash {}'.format(transactionHash))
    # wait for the transaction to be mined and get the address of the new contract
    while(True):
        requestObject, requestId = createJSONRPCRequestObject(
            'eth_getTransactionReceipt', [transactionHash], requestId)
        responseObject = postJSONRPCRequestObject(URL, requestObject)
        receipt = responseObject['result']
        if(receipt is not None):
            if(receipt['status'] == '0x1'):
                contractAddress = receipt['contractAddress']
                if not is_checksum_formatted_address(contractAddress):
                    contractAddress = to_checksum_address(contractAddress)
                print('newly deployed contract at address {}'.format(contractAddress))
            else:
                pp.pprint(responseObject)
                raise ValueError(
                    'transacation status is "0x0", failed to deploy contract. Check gas, gasPrice first')
            break
        time.sleep(PERIOD/10)

    ''' ================= SEND A TRANSACTION TO SMART CONTRACT  ================'''
    # get your nonce
    requestObject, requestId = createJSONRPCRequestObject(
        'eth_getTransactionCount', [myAddress, 'latest'], requestId)
    responseObject = postJSONRPCRequestObject(URL, requestObject)
    myNonce = w3.toInt(hexstr=responseObject['result'])
    print('nonce of address {} is {}'.format(myAddress, myNonce))

    # prepare the data field of the transaction
    # function selector and argument encoding
    # https://solidity.readthedocs.io/en/develop/abi-spec.html#function-selector-and-argument-encoding
    value1, value2 = 10, 32  # random numbers here
    function = 'add(uint256,uint256)'  # from smart contract
    methodId = w3.sha3(text=function)[0:4].hex()
    param1 = (value1).to_bytes(32, byteorder='big').hex()
    param2 = (value2).to_bytes(32, byteorder='big').hex()
    data = methodId + param1 + param2

    transaction_dict = {'from': myAddress,
                        'to': contractAddress,
                        'chainId': CHAINID,
                        # careful with gas price, gas price below the threshold defined in the node config will cause all sorts of issues (tx not bieng broadcasted for example)
                        'gasPrice': 1,
                        'gas': 2000000,  # rule of thumb / guess work
                        'nonce': myNonce,
                        'data': data}

    # sign the transaction
    signed_transaction_dict = w3.eth.account.signTransaction(
        transaction_dict, myPrivateKey)
    params = [signed_transaction_dict.rawTransaction.hex()]

    # send the transacton to your node
    print('executing {} with value {},{}'.format(function, value1, value2))
    requestObject, requestId = createJSONRPCRequestObject(
        'eth_sendRawTransaction', params, requestId)
    responseObject = postJSONRPCRequestObject(URL, requestObject)
    transactionHash = responseObject['result']
    print('transaction hash {}'.format(transactionHash))

    # wait for the transaction to be mined
    while(True):
        requestObject, requestId = createJSONRPCRequestObject(
            'eth_getTransactionReceipt', [transactionHash], requestId)
        responseObject = postJSONRPCRequestObject(URL, requestObject)
        receipt = responseObject['result']
        if(receipt is not None):
            if(receipt['status'] == '0x1'):
                print('transaction successfully mined')
            else:
                pp.pprint(responseObject)
                raise ValueError(
                    'transacation status is "0x0", failed to deploy contract. Check gas, gasPrice first')
            break
        time.sleep(PERIOD/10)

    ''' ============= READ YOUR SMART CONTRACT STATE USING GETTER  =============='''
    # we don't need a nonce since this does not create a transaction but only ask
    # our node to read it's local database

    # prepare the data field of the transaction
    # function selector and argument encoding
    # https://solidity.readthedocs.io/en/develop/abi-spec.html#function-selector-and-argument-encoding
    # state is declared as public in the smart contract. This creates a getter function
    methodId = w3.sha3(text='state()')[0:4].hex()
    data = methodId
    transaction_dict = {'from': myAddress,
                        'to': contractAddress,
                        'chainId': CHAINID,
                        'data': data}

    params = [transaction_dict, 'latest']
    requestObject, requestId = createJSONRPCRequestObject(
        'eth_call', params, requestId)
    responseObject = postJSONRPCRequestObject(URL, requestObject)
    try:
        state = w3.toInt(hexstr=responseObject['result'])
        print('using getter for public variables: result is {}'.format(state))
    except KeyError:
        print(responseObject['error'])

    ''' ============= READ YOUR SMART CONTRACT STATE GET FUNCTIONS  =============='''
    # we don't need a nonce since this does not create a transaction but only ask
    # our node to read it's local database

    # prepare the data field of the transaction
    # function selector and argument encoding
    # https://solidity.readthedocs.io/en/develop/abi-spec.html#function-selector-and-argument-encoding
    # state is declared as public in the smart contract. This creates a getter function
    methodId = w3.sha3(text='getState()')[0:4].hex()
    data = methodId
    transaction_dict = {'from': myAddress,
                        'to': contractAddress,
                        'chainId': CHAINID,
                        'data': data}

    params = [transaction_dict, 'latest']
    requestObject, requestId = createJSONRPCRequestObject(
        'eth_call', params, requestId)
    responseObject = postJSONRPCRequestObject(URL, requestObject)

    try:
        state = w3.toInt(hexstr=responseObject['result'])
        print('using getState() function: result is {}'.format(state))
    except KeyError:
        print(responseObject['error'])
        


except KeyError:
    print(responseObject['error'])


''' prints
nonce of address 0xF464A67CA59606f0fFE159092FF2F474d69FD675 is 4
contract submission hash 0x64fc8ce5cbb5cf822674b88b52563e89f9e98132691a4d838ebe091604215b25
newly deployed contract at address 0x7e99eaa36bedba49a7f0ea4096ab2717b40d3787
nonce of address 0xF464A67CA59606f0fFE159092FF2F474d69FD675 is 5
executing add(uint256,uint256) with value 10,32
transaction hash 0xcbe3883db957cf3b643567c078081343c0cbd1fdd669320d9de9d05125168926
transaction successfully mined
using getter for public variables: result is 42
using getState() function: result is 42
'''
