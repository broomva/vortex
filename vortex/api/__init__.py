from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from vortex.datamodels import get_db
from vortex.io.twilio import handle_wapp_message

load_dotenv()

app = FastAPI()


@app.get("/api/check")
def hello_world():
    return {"message": "Vortex is Running!"}


@app.get("/")
async def index():
    return {"message": "Vortex is Running!"}


@app.post("/message")
async def reply(request: Request, Body: str = Form(), db: Session = Depends(get_db)):
    print(Body)
    print(request)
    await handle_wapp_message(request, Body, db)
    return ""
