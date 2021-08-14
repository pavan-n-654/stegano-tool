from PIL import Image
import numpy as np

def Encode(image:str, msg:str, dest:str) -> None :
    """
    Encodes text in image using LSB manipulation of the RGB pixel values.
        Each char(8 bit) is stored in 3 pixel(3x3), 9th bit indicates whether the text ends or not
    """
    img = Image.open(image, 'r')
    width, height = img.size
    arr = np.array(list(img.getdata()))
    pixels = arr.shape[0]
    if len(msg)*3 >= pixels:
        raise Exception("Required higher dimension file")

    #converting char to 8 bit len binary numbers
    msg_data = [format(ord(i), "08b") for i in msg]
    x = 0
    for char in msg_data:
        for bit in range(8):
            col_index = bit%3
            if col_index == 0 and bit != 0:
                x += 1              # increment array index after 3 bits
            arr[x][col_index] = (arr[x][col_index] & 254) | int(char[bit])      # masking the last bit to 0 then modifing a/c to bit
        # making the last value of 3rd tuple to 0 for text continuation
        arr[x][2] = arr[x][2] & 254
        x += 1
    # text termination
    arr[x-1][2] = arr[x-1][2] | 1
    array = arr.reshape(height, width, 3)       # n=3 where n => RGB
    des_img = Image.fromarray(array.astype('uint8'), img.mode)
    des_img.save(dest)
    print("Success")

def Decode(enc_img: str) -> str:
    """
    Decodes LSB encoded image file
    """
    img = Image.open(enc_img, 'r')
    arr = np.array(list(img.getdata()))
    img_pix = arr.shape[0]
    msg = ''
    for pix in range(0, img_pix, 3):
        char = ''
        for col in range(3):
            char += (bin(arr[pix+col][0])[-1])
            char += (bin(arr[pix+col][1])[-1])
            char += (bin(arr[pix+col][2])[-1])
        msg += chr(int(char[:8], 2))
        if char[-1] == '1':     # last bit of 3rd tuple
            break
    return msg

if __name__ == "__main__":
    choice = int(input("Enter choice: \n1. Encode \n2. Decode \n>>> "))
    if choice == 1:
        src = input("Source file name: ")
        msg = input("Message: ")
        dest = input("Destination file name: ")
        Encode(src, msg, dest)
    elif choice == 2:
        src = input("Source file name: ")
        print(Decode(src))
