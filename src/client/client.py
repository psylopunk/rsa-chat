import os
import rsa
import threading
import time
import json
import websocket

config = {
    "HOST": "gurov.co:7007"
}

class Client:
    def __init__(self, host=False, room=False, login=False):
        self.lock = threading.Lock()
        self.live = True
        print("Client started")
        self.host = host or input("Host:Port [%s]: " % config["HOST"]) or config["HOST"]
        self.room = room or input("Room: ")
        self.login = login or input("Login: ")
        if not self.room or not self.login: print("Room/Login is not specified"); os._exit(1)
        self.publicKey, self.privateKey = rsa.newkeys(512)
        self.rawPublicKey = self.publicKey.save_pkcs1("PEM").hex()
        print("Keys are generated")
        self.websocket_connect()
        print("Send \"q\" to exit")
        try:
            while True:
                self.message = input()
                if self.message == "q": os._exit(1)
                if not self.message: continue
                self.ws.send(json.dumps({"action": "get_clients", "room": self.room}))
        except:
            print("Connection terminated")
            self.reconnect()
        with self.lock: self.ws.close()

    def recv_func(self):
        while self.live:
            try: data = json.loads(self.ws.recv())
            except: continue
            action = data["action"]
            if action == "connect":
                if data["success"]: print("Connected to WebsocketServer")
                else: print("WebsocketServer returned Error [%s]" % data["err"]); os._exit(1)
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

    def websocket_connect(self, reconnect=False):
        self.ws = websocket.WebSocket()
        try:
            self.ws.connect("ws://%s/" % self.host)
            self.recv_thread = threading.Thread(target=self.recv_func, args=[])
            self.recv_thread.daemon = True
            self.recv_thread.start()
        except:
            print("WebsocketServer unavailable")
            self.live = False
            self.reconnect()

    def reconnect(self):
        print("Reconnect in 3 second")
        time.sleep(3)
        client = Client(host=self.host, room=self.room, login=self.login)

if __name__ == '__main__':
    client = Client()
