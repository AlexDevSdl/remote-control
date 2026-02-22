from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.connection_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

# Agente se conecta aquí
@router.websocket("/ws/device/{device_id}")
async def device_ws(websocket: WebSocket, device_id: str):
    await manager.connect_device(device_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_to_controller(device_id, data)
    except WebSocketDisconnect:
        manager.disconnect_device(device_id)

# Controlador se conecta aquí
@router.websocket("/ws/control/{device_id}")
async def control_ws(websocket: WebSocket, device_id: str):
    await manager.connect_controller(device_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_to_device(device_id, data)
    except WebSocketDisconnect:
        manager.disconnect_controller(device_id)