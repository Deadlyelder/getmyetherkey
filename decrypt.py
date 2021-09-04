import scrypt
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Hash import keccak

class Decrypter:

    def __init__(self, json_data, password):
        self.extract_variables_from_json(json_data)
        self.password = password

    def decrypt(self):
        dec_key = self.compute_derivation_key()
        self.validate_password(dec_key)
        return self.decrypt_derived_key(dec_key)

    def extract_variables_from_json(self, json_data):
        crypto = json_data['crypto']
        cipher = crypto['cipher']
        self.ciphertext = crypto['ciphertext']
        self.iv = crypto['cipherparams']['iv']
        kdf = crypto['kdf']
        kdfparams = crypto['kdfparams']
        self.dklen = kdfparams['dklen']
        self.n = kdfparams['n']
        self.p = kdfparams['p']
        self.r = kdfparams['r']
        self.salt = kdfparams['salt']
        self.mac = crypto['mac']

    def compute_derivation_key(self):
        scrypt_hash = scrypt.hash(password=bytes(self.password, 'utf-8'),
                                  salt=bytes.fromhex(self.salt),
                                  N=self.n,
                                  r=self.r,
                                  p=self.p,
                                  buflen=self.dklen)
        return scrypt_hash

    def validate_password(self, dec_key):
        validate = dec_key[16:] + bytes.fromhex(self.ciphertext)
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(validate)
        if keccak_hash.hexdigest() != self.mac:
            raise ValueError('Incorrect password')

    def decrypt_derived_key(self, dec_key):
        iv_int = int(self.iv, 16)
        ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)
        dec_suite = AES.new(dec_key[:16], AES.MODE_CTR, counter=ctr)
        plain_key = dec_suite.decrypt(bytes.fromhex(self.ciphertext))
        return plain_key
