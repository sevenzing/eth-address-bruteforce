import re
from web3 import Web3
from tqdm import tqdm
import os
import argparse

get_account = Web3().eth.account.from_key


def privToAddress(priv) -> str:
    return get_account(priv).address.lower()[2:]


def bruteforce(pattern, n=1000):
    for _ in tqdm(range(n)):
        key = os.urandom(32)
        address = privToAddress(key)
        if re.match(pattern,address):
            return address, key.hex()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'pattern',
        help='prefix for eth address',
    )
    parser.add_argument(
        '-n', '--number', type=int, default=16**6,
        help='amount of iterations. default is 16^6',
    )
    parser.add_argument(
        '-o', '--output', default='keys',
        help='path for output file',
    )
    

    return parser.parse_args()



if __name__ == '__main__':
    args = parse_arguments()
    pattern = args.pattern
    n = args.number
    
    print(pattern, n)

    address, key = bruteforce(pattern, n)
    print(f'Found! {address} for {key}')

    with open(args.output, 'a') as file:
        file.write(f"{address};{key}\n")