import json
import asyncio
import websockets
from PyQt5.QtCore import QThread, pyqtSignal

from .database import load_data, save_data

class WebSocketServer(QThread):
    messageReceived = pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clients = set()

    async def server(self, websocket, path):
        self.clients.add(websocket)
        try:
            while True:
                data = await websocket.recv()
                print(f"Received: {data}")

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
                    # else:
                    #     response = {"status": "error", "message": f"Action '{action}' not found."}
                    await websocket.send(json.dumps(response))
                    # self.messageReceived.emit(store_data)
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({"status": "error", "message": "Invalid JSON format."}))

        finally:
            self.clients.remove(websocket)

    async def broadcast(self, message):
        if self.clients:
            tasks = [asyncio.create_task(client.send(json.dumps(message))) for client in self.clients]
            await asyncio.wait(tasks)

    def send_data(self, data):
        asyncio.run(self.broadcast(data))

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self.server, "0.0.0.0", 8765)
        loop.run_until_complete(start_server)
        loop.run_forever()
