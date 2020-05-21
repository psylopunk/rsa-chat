from PyQt5 import QtWidgets, uic
import threading
import websocket
import rsa
import design_app
import design_connect
import sys
import json
import time

HOST = "192.236.179.125:9200"

def on_message(ws, message):
    data = json.loads(message)
    print("[WS] < %s" % (data))
    action = data["action"]
    if action == "get_clients":
        crypted_messages = []
        message = window.inputMessage.text()
        for pubkey in data["data"]["clients"]: crypted_messages.append(rsa.encrypt(message.encode("utf8"), rsa.PublicKey.load_pkcs1(bytes(bytearray.fromhex(pubkey)))).hex())
        window.ws.send(json.dumps({"action": "send_message", "box": window.box, "message": crypted_messages}))
    elif action == "receive_message":
        for message in data["data"]:
            try:
                decrypted = rsa.decrypt(bytes(bytearray.fromhex(message)), window.privateKey).decode("utf8")
                window.textBrowser.setText(window.textBrowser.toPlainText() + ("[%s]: %s\n" % (data["login"], decrypted)))
            except: pass

def on_error(ws, error):
    print("Error websockets")

def on_close(ws):
    print("[WS] Closed connection")
    window.connect_ws()
    window.ws.send(json.dumps({"login": self.name, "box": self.box, "pubkey": self.rawPublicKey}))


class ConnectGui(QtWidgets.QMainWindow, design_connect.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class AppGui(QtWidgets.QMainWindow, design_app.Ui_MainWindow):
    def show_connect_window(self):
        self.connectGui = ConnectGui()
        self.connectGui.btnConnect.clicked.connect(self.connectBox)
        self.connectGui.show()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.publicKey, self.privateKey = rsa.newkeys(512)
        self.rawPublicKey = self.publicKey.save_pkcs1("PEM").hex()
        print(self.privateKey.save_pkcs1("PEM").hex())

        self.btnSend.clicked.connect(self.send_message)

    def connect_ws(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://%s/" % (HOST), on_message = on_message, on_error = on_error, on_close = on_close)
        threading.Thread(target=self.ws.run_forever, args=[]).start()

    def connectBox(self):
        self.box = self.connectGui.inputBox.text()
        self.name = self.connectGui.inputName.text()
        print("Box: %s\nName: %s" % (self.box, self.name))
        self.connectGui.close()
        self.connect_ws()
        time.sleep(0.1)
        self.ws.send(json.dumps({"login": self.name, "box": self.box, "pubkey": self.rawPublicKey}))
        # TODO except if not connect

    def send_message(self):
        self.ws.send(json.dumps({"action": "get_clients", "box": self.box}))

        # self.textBrowser.setText(self.inputMessage.text())

def main():
    global window
    app = QtWidgets.QApplication(sys.argv)
    window = AppGui()
    window.show()
    window.show_connect_window()
    app.exec()

if __name__ == '__main__':
    main()
