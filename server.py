import os
import base64
import socket
import asyncio
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


load_dotenv()
key = os.environ.get('KEY')
if not key:
    raise RuntimeError("No se encontro el .env")
key_bytes = base64.b64decode(key)
def decrypt_msg(msg: str):
    encr_bytes = base64.b64decode(msg)

    cypher = AES.new(key_bytes, AES.MODE_CBC,encr_bytes[:16])
    decryp_padded = cypher.decrypt(encr_bytes[16:])
    decryp_clean = unpad(decryp_padded, AES.block_size)

    return decryp_clean.decode('utf-8')

async def handle_client(reader, writer):
    print(f"[SERVER] connection from {writer.get_extra_info('peername')} has been established")
    while True:
        data = await reader.read(1024)
        if not data:
            break
        incoming_text = data.decode('utf-8')

        print(f"[SERVER] encrypted message recieved (base64): {incoming_text}")

        try:
            dec_msg = decrypt_msg(incoming_text)
            print(f"[SERVER] message decrypted succesfully: {dec_msg}")
        except Exception as e:
            print(f"[SERVER] decryption failed: {e}")

    writer.close()

async def main():
    server = await asyncio.start_server(handle_client,'127.0.0.1',5000)
    print("[SERVER] server is listening on port 5000")
    await server.serve_forever()

asyncio.run(main())


