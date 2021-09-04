import wave
import numpy as np
import os
from cryptography.fernet import Fernet
import base64

class audio:
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
    def Encode(self, song_src: str, msg: str, song_dest:str) -> None:
        """
        Encodes text in audio using LSB manipulation of the each byte.
            text $t3g4n0 indicates whether the text ends or not
        """
        song = wave.open(song_src, mode = 'rb')

        frame_arr = np.array(list(song.readframes(song.getnframes())), dtype=np.uint8)
        frame_size = frame_arr[0]
        bin_msg = list(map(int, ''.join([format(ord(i), "08b") for i in msg])))
        if bin_msg >= frame_size:
            raise Exception("Required lager size file")
        for ind, bit in enumerate(bin_msg):
            frame_arr[ind] = (frame_arr[ind] & 254) | bit

        byte_array = frame_arr.tobytes()
        fp = wave.open(song_dest, "wb")
        fp.setparams(song.getparams())
        fp.writeframes(byte_array)
        song.close()
        fp.close()

    def Decode(self, song_src: str)->str:
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


