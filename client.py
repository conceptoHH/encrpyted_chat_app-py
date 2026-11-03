import os
import base64
import socket
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


load_dotenv()
key = os.environ.get('KEY')
if not key:
    raise RuntimeError("No se encontro el .env")
key_bytes = base64.b64decode(key)

def encrypt_msg(msg: str):
    iv_bytes = os.urandom(16)
    cypher = AES.new(key_bytes, AES.MODE_CBC,iv_bytes)

    msg_bytes = msg.encode('utf-8')

    pad_msg_bytes = pad(msg_bytes, AES.block_size)

    encrypted = cypher.encrypt(pad_msg_bytes)
    return base64.b64encode(iv_bytes + encrypted).decode('utf-8')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))

while True:
    message = input("Ingresa tu mensaje: ")
    if not message:
        break

    en_text = encrypt_msg(message)
    print(f"Mensage encriptado a enviar: {en_text}")

    client_socket.sendall(en_text.encode('utf-8'))

client_socket.close()
