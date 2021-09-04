from PIL import Image
import os
import numpy as np
from cryptography.fernet import Fernet
import base64

class lsb_text:

    def __init__(self, src_path, password, **kwargs):
        self.src_path = src_path
        self.password = password
        self.dest_path = kwargs.get("dest", "")
        self.msg_text = kwargs.get("msg", "")

    def is_path_exsits(self, file_path):
        if os.path.exists(file_path):
            return True
        return False

    def str_not_empty(self, string):
        if string != '':
            return True
        return False

    def get_data(self):

        key = self.password * 32
        secret_key = base64.urlsafe_b64encode(str(key[:32]).encode())
        encryption_key = Fernet(secret_key)

        encrypted_text = encryption_key.encrypt(self.msg_text.encode('utf-8'))

        encrypted_text = str(encrypted_text)

        encrypted_text += "$t3g4n0"

        binary_value = ''.join([format(ord(character), "08b") for character in encrypted_text])
        return binary_value

    def Encode(self) -> None :
        """
        Encodes text in image using LSB manipulation of the RGB pixel values.
        text $t3g4n0 indicates whether the text ends or not
        """
        img = Image.open(self.src_path, 'r')
        width, height = img.size
        arr = np.array(list(img.getdata()))
        n = 3
        if img.mode == "RGBA":
            n = 4
        pixels = arr.shape[0]
        if len(self.msg_text)*n >= pixels:
            raise Exception("Required higher dimension file")

        #converting char to 8 bit len binary numbers
        msg_data = self.get_data()
        msg_size = len(msg_data)
        bit = 0
        for pixel in range(pixels):
            if bit >= msg_size:
                break
            for col in range(0,n):
                arr[pixel][col] = (arr[pixel][col] & 254) | int(msg_data[bit])       # masking the last bit to 0 then modifing a/c to bit
                bit += 1
        array = arr.reshape(height, width, n)       # n=3 where n => RGB
        des_img = Image.fromarray(array.astype('uint8'), img.mode)
        des_img.save(self.dest_path)
        print("Success")

    def Decode(self, enc_img: str) -> str:
        """
        Decodes LSB encoded image file
        """
        img = Image.open(enc_img, 'r')
        arr = np.array(list(img.getdata()))
        img_pix = arr.shape[0]
        bin_str = ''
        n = 3
        if img.mode == "RGBA":
            n = 4
        ter_str = ''.join([format(ord(ch), "08b") for ch in "$t3g4n0"])
        for pixel in range(img_pix):
            for col in range(0, n):
                bin_str += bin(arr[pixel][col])[-1]
            if (pixel*n)%8 == 0 and bin_str[-56:] == ter_str:
                bin_str = bin_str[:-56]
                break
        bin_ch = list(map(lambda x: int(x, 2), [bin_str[ind:ind+8] for ind in range(0, len(bin_str), 8)]))
        msg = ''.join(list(map(chr, bin_ch)))
        return msg


