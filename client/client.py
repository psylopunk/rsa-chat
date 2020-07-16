import os
import rsa
import threading
import json
import websocket

config = {
    "HOST": "gurov.co:7007"
}

class Client:
    def __init__(self):
        self.lock = threading.Lock()
        print("Client started")
        self.host = input("Host:Port [%s]: " % config["HOST"]) or config["HOST"]
        self.room = input("Room: ")
        self.login = input("Login: ")
        if not self.room or not self.login: print("Room/Login is not specified"); os._exit(1)
        self.publicKey, self.privateKey = rsa.newkeys(512)
        self.rawPublicKey = self.publicKey.save_pkcs1("PEM").hex()
        print("Keys are generated")
        self.websocket_connect()
        print("Send \"q\" to exit")
        while True:
            self.message = input()
            if self.message == "q": os._exit(1)
            self.ws.send(json.dumps({"action": "get_clients", "room": self.room}))
        with self.lock: self.ws.close()

    def recv_func(self):
        while True:
            try: data = json.loads(self.ws.recv())
            except: continue
            action = data["action"]
            if action == "connect":
                if data["success"]: print("Connected to WebsocketServer")
                else: print("WebsocketServer is not available"); os._exit(1)
            elif action == "wait_connect":
                self.ws.send(json.dumps({"login": self.login, "room": self.room, "pubkey": self.rawPublicKey}))
            elif action == "get_clients":
                crypted_messages = []
                for pubkey in data["data"]["clients"]: crypted_messages.append(rsa.encrypt(self.message.encode("utf8"), rsa.PublicKey.load_pkcs1(bytes(bytearray.fromhex(pubkey)))).hex())
                self.ws.send(json.dumps({"action": "send_message", "room": self.room, "message": crypted_messages}))
            elif action == "receive_message":
                for message in data["data"]:
                    try:
                        decrypted = rsa.decrypt(bytes(bytearray.fromhex(message)), self.privateKey).decode("utf8")
                        print("[%s]: %s" % (data["login"], decrypted))
                    except: pass

    def websocket_connect(self):
        self.ws = websocket.WebSocket()
        self.ws.connect("ws://%s/" % self.host)
        self.recv_thread = threading.Thread(target=self.recv_func, args=[])
        self.recv_thread.daemon = True
        self.recv_thread.start()

    def reconnect(self):
        print("Reconnect inited")
        # TODO: Reconnect function

if __name__ == '__main__':
    client = Client()
