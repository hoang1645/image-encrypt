from base64 import b64decode, b64encode
from typing import Literal

#pip(3) install pillow
from PIL import Image
#pip(3) install pycryptodome
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class ImageEncryptor():
    @staticmethod
    def generate_key(nbytes:Literal[16,24,32]=32):
        assert nbytes == 16 or nbytes == 24 or nbytes == 32
        return get_random_bytes(nbytes)

    @staticmethod
    def encrypt(image:str, key:bytes):

        spl = image.split(sep='.')
        if len(spl) == 1:
            return
        ext = spl[-1]
        print(ext)
        filename = ''.join(spl[:-1])

        ima = Image.open(image)
        if ima.mode != 'RGBA':
            ima = ima.convert("RGBA")

        image_bytes = ima.tobytes()
        
        cipher = AES.new(key, mode=AES.MODE_CFB)
        ct_bytes = cipher.encrypt(image_bytes)

        new_image = Image.frombytes(ima.mode, ima.size, ct_bytes)
        iv = b64encode(cipher.iv).decode('utf8')
        while "/" in iv:
            iv = iv.replace("/", "-")
        new_image.save(filename + "_{}.".format(iv) + ext)
        new_image.close()
        return iv

    @staticmethod
    def decrypt(image:str, key:bytes):
        spl = image.split(sep='.')
        if len(spl) == 1:
            return
        ext = spl[-1]
        print(ext)
        filename = ''.join(spl[:-1])

        spl2 = filename.split(sep='_')
        iv = spl2[-1]
        while '-' in iv:
            iv = iv.replace('-', '/')
        iv = b64decode(iv)
        filename = ''.join(spl2[:-1])

        ima = Image.open(image)
        
        image_bytes = ima.tobytes()

        dec = AES.new(key, mode=AES.MODE_CFB, iv=iv)
        pt_bytes = dec.decrypt(image_bytes)
        pt_image = Image.frombytes(ima.mode, ima.size, pt_bytes)
        pt_image.save(filename + '_D.' + ext)
        pt_image.close()