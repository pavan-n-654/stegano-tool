import wave
import numpy as np

def Encode(song_src: str, msg: str, song_dest:str) -> None:
    """
    Encodes text in audio using LSB manipulation of the each byte.
        text $t3g4n0 indicates whether the text ends or not
    """
    song = wave.open(song_src, mode = 'rb')

    frame_arr = np.array(list(song.readframes(song.getnframes())), dtype=np.uint8)
    msg += '$t3g4n0'
    bin_msg = list(map(int, ''.join([format(ord(i), "08b") for i in msg])))

    for ind, bit in enumerate(bin_msg):
        frame_arr[ind] = (frame_arr[ind] & 254) | bit

    byte_array = frame_arr.tobytes()
    fp = wave.open(song_dest, "wb")
    fp.setparams(song.getparams())
    fp.writeframes(byte_array)
    song.close()
    fp.close()

def Decode(song_src: str)->str:
    """
    Decodes LSB encoded audio file
    """
    song = wave.open(song_src, mode='rb')
    frame_arr = np.array(list(song.readframes(song.getnframes())))
    msg = ''
    for ind in range(0, len(frame_arr), 8):
        char = ''.join(map(str, [frame_arr[i] & 1 for i in range(ind, ind+8)]))
        msg += chr(int(char, 2))
        if msg[-7:] == "$t3g4n0":
            break
    return msg[:-7]

if __name__ == "__main__":
    choice = int(input("Enter choice: \n1. Encode \n2. Decode\n>>> "))
    if choice == 1:
        src = input("Source file name: ")
        msg = input("Message: ")
        dest = input("Destination file name: ")
        Encode(src, msg, dest)
    elif choice == 2:
        src = input("Source file name: ")
        print(Decode(src))
