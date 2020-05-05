from Crypto.PublicKey import RSA
import sys
import os
import asyncio
import websockets
import threading
import json

# os._exit(1)

if len(sys.argv) != 3: raise Exception("python3 client.py host login@boxname")

host = sys.argv[1]
login = sys.argv[2].split("@")[0]
boxname = sys.argv[2].split("@")[1]

print("""Client started:
    Host: %s
    Auth: %s@%s""" % (host, login, boxname))

privateKey = RSA.generate(1024)
publicKey = privateKey.publickey()

print("\nKeys are generated")

async def ws_client():
    async with websockets.connect("ws://%s/" % host) as websocket:
        await websocket.send(json.dumps({"login": login, "box": boxname, "pubkey": publicKey.exportKey("PEM").hex()}))
        data = json.loads(await websocket.recv())
        if data["err"]: raise Exception("Error from server: [%s]" % data["err"])

def start_websocket_client(): asyncio.get_event_loop().run_until_complete(ws_client())
threading.Thread(target=start_websocket_client, args=[]).start()
while True:
    message = input("> ")
    print(message)
