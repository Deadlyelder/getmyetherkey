import sys
import json
import argparse
import getpass

from eth_utils import address
from decrypt import Decrypter


def main(args):
    print('Enter wallet password: ')
    password = getpass.getpass()
    json_data = load_keystore_file(args.keystore_file)

    decrypter = Decrypter(json_data, password)
    encoded_address = address.to_checksum_address(json_data['address'])
    private_key = None
    try:
        private_key = decrypter.decrypt().hex()
    except ValueError as err:
        print(str(err), file=sys.stderr)
        exit(-1)
    print('Public Key/Address: ' + encoded_address)
    print('Private Key: ' + private_key)

def load_keystore_file(filename):
    with open(filename) as keystore_file:
        data = json.load(keystore_file)
    return data

def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Get the private key from the Ethereum keystore file')
    parser.add_argument('keystore_file', type=str, help='Path to the Ethereum keystore file')
    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
