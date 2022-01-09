import random
#pip(3) install pycryptodome
from Crypto.Hash import SHA256

from rabin_miller import isPrime
from egcd import egcd

class RSA():
    def __init__(self, n) -> None:
        assert n % 2 == 0
        bits = n // 2
        
        self.e = 0


        p = q = e = 0
        gcd = 0
        while gcd != 1:
            while not isPrime(p, 64):
                p = random.getrandbits(bits)
            while not isPrime(q, 64):
                q = random.getrandbits(bits)
            while not isPrime(e, 64):
                e = random.getrandbits(bits)
            
            self.n = p * q
            gcd, self.d, _ = egcd(self.e, (p - 1) * (q - 1))
    
    ##########################################################
    def set_keys(self, n:int, e:int, d:int):
        self.n = n
        self.e = e
        self.d = d
    ##########################################################
    def encrypt(self, message:bytes) -> bytes:
        assert isinstance(message, bytes)
        hexa = message.hex()
        long = int(hexa, base=16)

        encrypt_long = pow(long, self.e, self.n)
        encrypt_bytes = bytes(encrypt_long)
        return encrypt_bytes
    ##########################################################
    def decrypt(self, cipher:bytes) -> bytes:
        assert isinstance(cipher, bytes)
        cipher_hexa = cipher.hex()
        cipher_long = int(cipher_hexa, base=16)

        long = pow(cipher_long, self.d, self.n)
        return bytes(long)
    ##########################################################  
    def sign(self, S:str) -> str:
        assert isinstance(S, str)
        S_bytes = S.encode(encoding='utf8')
        
        h = SHA256.new()
        h.update(S_bytes)
        return h.hexdigest()
