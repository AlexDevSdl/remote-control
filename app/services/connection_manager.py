from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.devices = {}        # device_id -> websocket
        self.controllers = {}    # device_id -> websocket

    async def connect_device(self, device_id: str, websocket: WebSocket):
        await websocket.accept()
        self.devices[device_id] = websocket

    async def connect_controller(self, device_id: str, websocket: WebSocket):
        await websocket.accept()
        self.controllers[device_id] = websocket

    def disconnect_device(self, device_id: str):
        self.devices.pop(device_id, None)

    def disconnect_controller(self, device_id: str):
        self.controllers.pop(device_id, None)

    async def send_to_device(self, device_id: str, data: str):
        if device_id in self.devices:
            await self.devices[device_id].send_text(data)

    async def send_to_controller(self, device_id: str, data):
        if device_id in self.controllers:
            await self.controllers[device_id].send_text(data)