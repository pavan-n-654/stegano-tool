from PIL import Image
import numpy as np


class lsb_text:

    def __init__(self, **kwargs):
        self.src_path = kwargs.get("src", "")
        self.dest_path = kwargs.get("dest", "")
        self.msg_text = kwargs.get("msg", "")


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
        msg_data = self.msg_text
        msg_size = len(msg_data)
        bit = 0
        for pixel in range(pixels):
            if bit >= msg_size:
                break
            for col in range(0,n):
                if bit >= msg_size:
                    break
                arr[pixel][col] = (arr[pixel][col] & 254) | int(msg_data[bit])       # masking the last bit to 0 then modifing a/c to bit
                bit += 1
        array = arr.reshape(height, width, n)       # n=3 where n => RGB
        des_img = Image.fromarray(array.astype('uint8'), img.mode)
        des_img.save(self.dest_path)
        print("Success")

    def Decode(self) -> str:
        """
        Decodes LSB encoded image file
        """
        img = Image.open(self.src_path, 'r')
        arr = np.array(list(img.getdata()))
        img_pix = arr.shape[0]
        bin_str = ''
        n = 3
        if img.mode == "RGBA":
            n = 4
        ter_str = ''.join([format(ord(ch), "08b") for ch in "$t3g4n0"])
        is_looping = True
        for pixel in range(img_pix):
            for col in range(0, n):
                bin_str += bin(arr[pixel][col])[-1]
                if bin_str[-56:] == ter_str:
                    bin_str = bin_str[:-56]
                    is_looping = False
                    break
            if not is_looping:
                break
        bin_ch = list(map(lambda x: int(x, 2), [bin_str[ind:ind+8] for ind in range(0, len(bin_str), 8)]))
        msg = ''.join(list(map(chr, bin_ch)))
        return msg


