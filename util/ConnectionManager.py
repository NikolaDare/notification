from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self) -> None:
        self.active_connection:List[WebSocket]=[]

    async def connect(self,websocket:WebSocket):
        await websocket.accept()
        self.active_connection.append(websocket)
    
    def disconnect(self,websocket:WebSocket):
        self.active_connection.remove(websocket)
    
    async def send_notification(self,msg:str,websocket:WebSocket):
        await websocket.send_text(msg)

    async def broadcast(self,msg:str,):
        for connection in self.active_connection:
            await connection.send_text(msg)