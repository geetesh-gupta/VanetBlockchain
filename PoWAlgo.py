import time
import hashlib as hasher


# Algorithm for generating a proof-of-work (based on bitcoin PoW)
# The algorithm requires to find SHA256 of a natural number (string) such that has the first three positions as '000' and ends with '00'


def generate_pow():
    start_time = time.time()
    pow_proof = int(0)
    initial_start = pow_proof + 1

    while(1):
        sha = hasher.sha256()
        sha.update(str(initial_start).encode('utf-8'))
        hash_value = sha.hexdigest()
        initial_start = int(initial_start) + 1

        if(hash_value[0] == '0' and hash_value[1] == '0' and hash_value[2] == '0' and hash_value[-1] == '0' and hash_value[-2] == '0'):
            end_time = time.time()
            pow_proof = initial_start - 1
            print('\nThe required hash value is: ' + hash_value)
            print('The PoW number is: ' + str(pow_proof))
            print('The total time taken is: ' +
                  str((end_time - start_time)))

            break

    return pow_proof
