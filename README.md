# getmyetherkey

The Ethereum wallet keystore file consists of its private and public key. The private key is not easily readable without performing certain computations. 

If you are using Ethereum to test certain applications, it can be hard to remember private keys needed to deploy applications.

The _getmyetherkey_ is a quick script that reads the keystore file and extracts the private key from that.

## Usage

```
python3 getmykey.py -h [keystore_file]

usage: getmykey.py [-h] keystore_file

Get the private key from the Ethereum keystore file

positional arguments:
  keystore_file  Path to the Ethereum keystore file

optional arguments:
  -h, --help     show this help message and exit
```

Upon running it will ask user for the wallet password.

## Example

```
ptython3 getmykey.py /example/keystore/UTC--2020-08-15T01-46-40.945687000Z--ef46e8cafe1b76c92c13824cea5e2e7b1301284e
```
