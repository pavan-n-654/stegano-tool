from lsb_text import lsb_text
from lsb_audio import audio
import argparse
from cryptography.fernet import Fernet
import base64
import os
def is_path_exsits(file_path):
    if os.path.exists(file_path):
        return True
    print(">>>", file_path, "does not exists")
    return False

def str_not_empty(string):
    if string != '':
        return True
    print(">>> empty string passed")
    return False

def get_data(password: str, msg_text: str) -> str:
    key = password * 32
    secret_key = base64.urlsafe_b64encode(str(key[:32]).encode())
    encryption_key = Fernet(secret_key)
    encrypted_text = encryption_key.encrypt(msg_text.encode('utf-8'))
    encrypted_text = encrypted_text.decode()
    encrypted_text += "$t3g4n0"
    binary_value = ''.join([format(ord(character), "08b") for character in encrypted_text])
    return binary_value

def decrypt_data(password, bin_msg):
    key = password * 32
    secret_key = base64.urlsafe_b64encode(str(key[:32]).encode())
    decryption_key = Fernet(secret_key)
    decrypted_text = decryption_key.decrypt(bin_msg.encode())
    return decrypted_text.decode()

parser = argparse.ArgumentParser()
parser.add_argument("-O", "--operation", help= "e, encode := for encoding; d, decode := for decoding;")
parser.add_argument("-ot", "--op_type", help = "audio, image file operation")
parser.add_argument("-s", "--Spath", help= "path str of source file")
parser.add_argument("-t", "--Tpath", help = "path str of destination file for encode operation")
parser.add_argument("-m", "--msg", help = "message string for encode operation")
args = parser.parse_args()

password = input().strip()

if args.operation == "":
    print(">>> Operation is not specified")
    exit()
if (args.operation == 'e' or args.operation == 'encode'):
    if not(is_path_exsits(args.Spath) and str_not_empty(args.msg)):
        exit()
    if (args.op_type == 'audio'):
        encoder = audio(src = args.Spath, dest = args.Tpath, msg = get_data(password, args.msg))
        encoder.Encode()
    elif args.op_type == 'image':
        encoder = lsb_text(src = args.Spath, dest = args.Tpath, msg = get_data(password, args.msg))
        encoder.Encode()
elif (args.operation == 'd' or args.operation == 'decode'):
    if not(is_path_exsits(args.Spath)):
        exit()
    if args.op_type == "audio":
        decoder = audio(src = args.Spath)
        msg = decoder.Decode()
        print(decrypt_data(password, msg))
    elif args.op_type == "image":
        decoder = lsb_text(src = args.Spath)
        msg = decoder.Decode()
        print(decrypt_data(password, msg))
