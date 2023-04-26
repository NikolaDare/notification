from fastapi import FastAPI,Request,Response,HTTPException,Depends,WebSocket,WebSocketDisconnect
import uvicorn, os,json
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime

from database.database import SessionLocal, engine
from database import models
from database.crud import get_user_by_email,get_key_from_user
from sqlalchemy.orm import Session

from util.ConnectionManager import ConnectionManager


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


origins = [
    '*'
]

app.add_middleware(
   CORSMiddleware,
    allow_origins =  origins,
    allow_credentials =True,
    allow_methods = ["*"],
    allow_headers= ["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

manager=ConnectionManager()
###############################################################

@app.get('/')
def read_root():
    return{'it':'works'}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
   



if __name__ == "__main__":
    config = uvicorn.Config("index:app", port=8080, log_level="info",workers=4)
    server = uvicorn.Server(config)
    server.run()