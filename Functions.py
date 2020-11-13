import time
import math
from datetime import datetime
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import binascii
import ast


def curtime():
    """
    Returns current time in microsecond
    """
    from datetime import datetime
    dt = datetime.now()
    return dt.microsecond


def func_per_second(fn, timeframe=1, *args):
    """
    Runs a function every second

    Parameters:
    fn -> Function object
    """

    starttime = curtime()
    while True:
        fn(*args)
        time.sleep((1000.0 * timeframe - ((curtime() - starttime) %
                                          (1000.0 * timeframe))) / 1000)


def get_distance(x1, y1, x2, y2):
    """
    Returns distance two points
    """
    return math.sqrt(pow(abs(x1-x2), 2) + pow(abs(y1-y2), 2))


def get_dict_distance(pos_dict1, pos_dict2):
    """
    Returns distance two positions as dictionaries of format {'x': x_value, 'y': y_value}
    """
    return get_distance(pos_dict1['x'], pos_dict1['y'], pos_dict2['x'], pos_dict2['y'])


def check_within_range(x1, y1, range1, x2, y2):
    """
    Returns boolean whether (x2, y2) is in range of (x1, y1)
    """
    return pow(abs(x1-x2), 2) + pow(abs(y1-y2), 2) <= pow(range1, 2)


def check_dict_within_range(pos_dict1, range1, pos_dict2):
    """
    Returns boolean whether pos_dict2 is in range of pos_dict1
    where the two dictionaries are of format {'x': x_value, 'y': y_value}
    and represent positions
    """
    return check_within_range(pos_dict1['x'], pos_dict1['y'], range1, pos_dict2['x'], pos_dict2['y'])


def encrypt_data(data, key):
    cipher = PKCS1_OAEP.new(key)
    encrypted_data = cipher.encrypt(data.encode())
    return binascii.hexlify(encrypted_data).decode()


def decrypt_data(data, key):
    cipher = PKCS1_OAEP.new(key)
    decrypted_data = cipher.decrypt(
        eval(str(binascii.unhexlify(data.encode()))))
    return decrypted_data.decode()


def list_set_diff(lis, sett):
    return (list(list(set(lis)-sett)) + list(sett-set(lis)))


if __name__ == "__main__":
    # pri_key = RSA.generate(2048)
    # encrypted_data = encrypt_data("Hello", pri_key.publickey())
    # decrypted_data = decrypt_data(encrypted_data, pri_key)
    # print(encrypted_data)
    # print(decrypted_data)
    from Node import Node
    nodes = [Node(100, 100, 10, 10), Node(100, 100, 10, 10),
             Node(100, 100, 10, 10), Node(100, 100, 10, 10)]
    print(nodes)
    n_nodes = {nodes[0], nodes[1]}
    print(n_nodes)
    print(list_set_diff(nodes, n_nodes))
