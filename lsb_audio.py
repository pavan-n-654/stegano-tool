import wave
import numpy as np


class audio:
    def __init__(self, **kwargs):
        self.src_path = kwargs.get("src", "")
        self.dest_path = kwargs.get("dest", "")
        self.msg_text = kwargs.get("msg", "")

    def Encode(self) -> None:
        """
        Encodes text in audio using LSB manipulation of the each byte.
            text $t3g4n0 indicates whether the text ends or not
        """
        song = wave.open(self.src_path, mode = 'rb')

        frame_arr = np.array(list(song.readframes(song.getnframes())), dtype=np.uint8)
        frame_size = frame_arr.shape[0]
        bin_msg = list(map(int, self.msg_text))
        if len(bin_msg) >= frame_size:
            raise Exception("Required lager size file")
        for ind, bit in enumerate(bin_msg):
            frame_arr[ind] = (frame_arr[ind] & 254) | bit

        byte_array = frame_arr.tobytes()
        fp = wave.open(self.dest_path, "wb")
        fp.setparams(song.getparams())
        fp.writeframes(byte_array)
        song.close()
        fp.close()

    def Decode(self)->str:
        """
        Decodes LSB encoded audio file
        """
        song = wave.open(self.src_path, mode='rb')
        frame_arr = np.array(list(song.readframes(song.getnframes())))
        song.close()
        msg = ''
        for ind in range(0, len(frame_arr), 8):
            char = '1'
            try:
                char = ''.join(map(str, [frame_arr[i] & 1 for i in range(ind, ind+8)]))
            except:
                print("Entire file was read")
            msg += chr(int(char, 2))
            if msg[-7:] == "$t3g4n0":
                break
        return msg[:-7]


