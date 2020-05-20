import json
import asyncio
import websockets

boxes = {}

async def websocket_handler(websocket, path):
    data = json.loads(await websocket.recv())
    if "login" not in data: return await websocket.send(json.dumps({"success": False, "err": "Login not specified"}))
    login = data["login"]
    if "box" not in data: return await websocket.send(json.dumps({"success": False, "err": "Box not specified"}))
    box = data["box"]
    if box not in boxes: boxes[box] = {"clients": []}
    if "pubkey" not in data: return await websocket.send(json.dumps({"success": False, "err": "Pubkey not specified"}))
    boxes[box]["clients"].append({"login": login, "pubkey": data["pubkey"], "ws": websocket})
    await websocket.send(json.dumps({"success": True, "err": ""}))
    print("Connected client [%s]" % login)
    while True:
        data = json.loads(await websocket.recv())
        if "action" not in data: await websocket.send(json.dumps({"success": False, "err": "Action not specified"})); continue
        action = data["action"]
        if action == "get_clients":
            if "box" not in data: await websocket.send(json.dumps({"success": False, "err": "Box not specified"})); continue
            if data["box"] not in boxes: boxes[box] = {"clients": []}
            await websocket.send(json.dumps({"success": True, "err": "", "data": {"clients": [client["pubkey"] for client in boxes[data["box"]]["clients"]]}}))


        return await websocket.send(json.dumps({"success": False, "err": "Unknown error"}))



# await websocket.send(greeting)

start_server = websockets.serve(websocket_handler, "0.0.0.0", 9200)

asyncio.get_event_loop().run_until_complete(start_server)
print("Server started")
asyncio.get_event_loop().run_forever()
