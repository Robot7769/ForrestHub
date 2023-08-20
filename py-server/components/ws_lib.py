import json
import asyncio
import websockets
from PyQt5.QtCore import QThread, pyqtSignal

def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

class WebSocketServer(QThread):
    messageReceived = pyqtSignal(str)

    async def countdown_timer(self, websocket):
        count = 60
        while count > 0:
            await asyncio.sleep(1)
            count -= 1
            response = {"key": "countdown", "payload": count}
            await websocket.send(json.dumps(response))

    async def server(self, websocket, path):
        asyncio.create_task(self.countdown_timer(websocket))
        while True:
            data = await websocket.recv()
            try:
                message = json.loads(data)
                action = message.get('action')
                payload = message.get('payload', {})
                store_data = load_data()

                if action == "set":
                    key = payload.get('key')
                    value = payload.get('value')
                    store_data[key] = value
                    save_data(store_data)
                    response = {"status": "success", "message": f"Key '{key}' set to '{value}'."}
                if action == "get":
                    key = payload.get('key')
                    value = store_data.get(key)
                    if value:
                        response = {"status": "success", "message": f"Value for '{key}' is '{value}'.", "payload": value}
                    else:
                        response = {"status": "error", "message": f"Key '{key}' not found."}
                await websocket.send(json.dumps(response))
            except json.JSONDecodeError:
                await websocket.send(json.dumps({"status": "error", "message": "Invalid JSON format."}))
            self.messageReceived.emit(data)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self.server, "0.0.0.0", 8765)
        loop.run_until_complete(start_server)
        loop.run_forever()
