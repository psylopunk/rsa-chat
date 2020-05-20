from PyQt5 import QtWidgets, uic
import websocket
import rsa
import design_app
import design_connect
import sys
import json
import time

HOST = "localhost:9200"

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

        self.btnSend.clicked.connect(self.send_message)

    def connectBox(self):
        self.box = self.connectGui.inputBox.text()
        self.name = self.connectGui.inputName.text()
        print("Box: %s\nName: %s" % (self.box, self.name))
        self.connectGui.close()
        self.ws = websocket.create_connection("ws://%s/" % HOST)
        self.ws.send(json.dumps({"login": self.name, "box": self.box, "pubkey": self.rawPublicKey}))
        res = json.loads(self.ws.recv())
        # TODO except if not connect
        print(res)

    def send_message(self):
        self.ws.send(json.dumps({"action": "get_clients", "box": self.box}))
        res = json.loads(self.ws.recv())

        crypted_messages = []
        message = self.inputMessage.text()

        for pubkey in res["data"]["clients"]: crypted_messages.append(rsa.encrypt(message.encode("utf8"), pubkey).hex())

        self.ws.send(json.dumps({"action": "send_message", "box": self.box, "message": crypted_messages}))

        self.textBrowser.setText(self.inputMessage.text())

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AppGui()
    window.show()
    window.show_connect_window()
    app.exec()

if __name__ == '__main__':
    main()
