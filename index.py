from fastapi import FastAPI,Request,Response,HTTPException,Depends,WebSocket,WebSocketDisconnect
import uvicorn, os,json, datetime
from fastapi.middleware.cors import CORSMiddleware



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

@app.websocket()("/ws/{id}")
async def websocket_endpoint(websocket:WebSocket,id:int, db:Session=Depends(get_db)):
    await manager.connect(websocket)
    now=datetime.now()

    current_time=now.strftime("%H:%M")

    try:
        while True:
            data=await websocket.receive_text()
            msg={"time":current_time,"id":id,'msg':data}
            await manager.broadcast(json.dumps(msg))
    except WebSocketDisconnect:
        manager.disconnect()
        msg={"time":current_time,"id":id,'msg':'OFFLINE'}
        await manager.broadcast(json.dumps(msg))
   



if __name__ == "__main__":
    config = uvicorn.Config("index:app", port=8080, log_level="info",workers=4)
    server = uvicorn.Server(config)
    server.run()