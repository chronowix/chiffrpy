import os
from cryptography.fernet import Fernet
import sys, getopt

# function: generate an encryption key file if the latter doesn't exist, if it exists, overwrites it by replacing the key
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

    if os.path.exists("key.key"):
        new_key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(new_key)

# function: reads the key file
def load():
    return open("key.key", "rb").read()

# function: encrypt the file with the key file
def encrypt(file, key):
    f = Fernet(key)
    with open(file, "rb") as fi:
        data = fi.read()
        enc_data = f.encrypt(data)
    with open(file, "wb") as fi:
        fi.write(enc_data)

# function: decrypt the encrypted file
def decrypt(file, key):
    f = Fernet(key)
    with open(file, "rb") as fi:
        enc_data = fi.read()
        dec_data = f.decrypt(enc_data)
    with open(file, "wb") as fi:
        fi.write(dec_data)
        return dec_data.decode()

# ------------------ Help menu -------------------
def help():
    print("Usage: Writing/overwriting key file: -w key.key \n"
        "         Encrypting file: -e <filename>\n"
        "         Decrypting file: -d <filename>\n")

# ------------------ Arguments reading -----------
def read_args(argv):
    key = ''
    file = ''
    opts, args = getopt.getopt(argv, "hw:e:d:", ["write=", "encrypt=", "decrypt="]) # arguments list

    if len(opts) < 1:
        help()
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ('-w', '--write'):
            write_key()
            print('Key file created')
        elif opt in ('-e', '--encrypt'):
            key = load()
            file = arg
            encrypt(file, key)
            print('File encrypted')
        elif opt in ('-d', '--decrypt'):
            key = load()
            file = arg
            decrypt(file, key)
            print('File decrypted')
    return key, file

def main(argv):
    read_args(argv)

main(sys.argv[1:])
