from fastapi import FastAPI,Request,Response,HTTPException,Depends
import uvicorn, os
from fastapi.middleware.cors import CORSMiddleware



from database.database import SessionLocal, engine
from database import models
from database.crud import get_user_by_email,get_key_from_user
from sqlalchemy.orm import Session




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
###############################################################

@app.get('/')
def read_root():
    return{'it':'works'}

@app.get("/ws/{id}")
def oauth2Callback(request: Request, db:Session=Depends(get_db)):
    key=get_key_from_user(db,1)
    print(key.id)
    return 'test'



if __name__ == "__main__":
    config = uvicorn.Config("index:app", port=8080, log_level="info",workers=4)
    server = uvicorn.Server(config)
    server.run()