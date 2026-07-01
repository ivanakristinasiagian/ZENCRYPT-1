from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Random import get_random_bytes
import os
import struct

SALT_SIZE = 16
KEY_SIZE = 32
NONCE_SIZE = 16
TAG_SIZE = 16

MAGIC_HEADER = b"ZENCRYPT"
MAX_FILE_SIZE = 10 * 1024 * 1024


def generate_key(password, salt):
    return PBKDF2(password.encode(), salt, dkLen=KEY_SIZE)


def check_file_size(filepath):
    size = os.path.getsize(filepath)
    if size > MAX_FILE_SIZE:
        raise Exception("Ukuran file melebihi 10 MB!")


def encrypt_file(filepath, password, output_folder):
    check_file_size(filepath)

    with open(filepath, "rb") as f:
        file_data = f.read()

    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)

    # ext misalnya ".docx" -> "docx"
    ext = ext.replace(".", "")

    salt = get_random_bytes(SALT_SIZE)
    key = generate_key(password, salt)

    # pakai nonce tetap 16 byte biar pasti sinkron
    nonce = get_random_bytes(NONCE_SIZE)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    ciphertext, tag = cipher.encrypt_and_digest(file_data)

    output_file = os.path.join(output_folder, name + ".crypt")

    with open(output_file, "wb") as f:
        f.write(MAGIC_HEADER)
        f.write(salt)
        f.write(nonce)
        f.write(tag)

        ext_bytes = ext.encode("utf-8")
        f.write(struct.pack("I", len(ext_bytes)))
        f.write(ext_bytes)

        f.write(ciphertext)

    return output_file


def decrypt_file(filepath, password, output_folder):
    with open(filepath, "rb") as f:
        header = f.read(len(MAGIC_HEADER))
        if header != MAGIC_HEADER:
            raise Exception("Bukan file ZenCrypt!")

        salt = f.read(SALT_SIZE)
        nonce = f.read(NONCE_SIZE)
        tag = f.read(TAG_SIZE)

        ext_length_data = f.read(4)
        if len(ext_length_data) != 4:
            raise Exception("File rusak! Panjang ekstensi tidak valid.")

        ext_length = struct.unpack("I", ext_length_data)[0]
        ext = f.read(ext_length).decode("utf-8")

        ciphertext = f.read()

    key = generate_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    try:
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    except Exception:
        raise Exception("Password salah atau file rusak!")

    filename = os.path.basename(filepath)
    if filename.endswith(".crypt"):
        name = filename[:-6]   # hapus ".crypt"
    else:
        name = filename

    output_file = os.path.join(output_folder, f"{name}.{ext}")

    with open(output_file, "wb") as f:
        f.write(decrypted_data)

    return output_file