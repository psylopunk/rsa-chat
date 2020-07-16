import websockets
import asyncio
import json
import sys

config = {
    "PORT": "7007"
}

arg_name = False
for argument in sys.argv[1:]:
    if "-" in argument:
        arg_name = argument.split("-")[-1]
        continue
    if arg_name == "p":
        config["PORT"] = int(argument)
    arg_name = False

rooms = {}

async def websocket_handler(websocket, path):
    try:
        await websocket.send(json.dumps({"action": "wait_connect"}))
        data = json.loads(await websocket.recv())
        print("[WS] < %s" % data)
        if "login" not in data: return await websocket.send(json.dumps({"action": "connect", "success": False, "err": "Login not specified"}))
        if "room" not in data: return await websocket.send(json.dumps({"action": "connect", "success": False, "err": "Room not specified"}))
        if "pubkey" not in data: return await websocket.send(json.dumps({"action": "connect", "success": False, "err": "Pubkey not specified"}))
        login = data["login"]
        room = data["room"]
        if room not in rooms: rooms[room] = {"clients": []}
        for client in rooms[room]["clients"]:
            if client["login"] == login: return await websocket.send(json.dumps({"action": "connect", "success": False, "err": "Login is busy"}))
        rooms[room]["clients"].append({"login": login, "pubkey": data["pubkey"], "ws": websocket})
        await websocket.send(json.dumps({"action": "connect", "success": True, "err": ""}))
        print("Connected client [%s]" % login)
        while True:
            data = json.loads(await websocket.recv())
            print("[WS] < %s" % data)
            if "action" not in data: await websocket.send(json.dumps({"success": False, "err": "Action not specified"})); continue
            action = data["action"]
            if action == "get_clients":
                if "room" not in data: await websocket.send(json.dumps({"success": False, "err": "Room not specified"})); continue
                if data["room"] not in rooms: rooms[room] = {"clients": []}
                await websocket.send(json.dumps({"action": "get_clients", "success": True, "err": "", "data": {"clients": [client["pubkey"] for client in rooms[data["room"]]["clients"]]}}))
            elif action == "send_message":
                if "room" not in data: await websocket.send(json.dumps({"success": False, "err": "Room not specified"})); continue
                if data["room"] not in rooms: rooms[room] = {"clients": []}
                for client in rooms[data["room"]]["clients"]:
                    await client["ws"].send(json.dumps({"action": "receive_message", "login": login, "data": data["message"]}))
            else: await websocket.send(json.dumps({"action": "unknown", "success": False, "err": "Unknown error"}))
    except: pass

start_server = websockets.serve(websocket_handler, "0.0.0.0", config["PORT"])

asyncio.get_event_loop().run_until_complete(start_server)
print("Server started on port %s" % config["PORT"])
asyncio.get_event_loop().run_forever()
