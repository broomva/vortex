import logging
import os
import weakref
from typing import Dict

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from twilio.rest import Client

from vortex.ai.agents import VortexAgent
from vortex.api.data_models import Conversation, SessionLocal, get_db

load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = "+14155238886" or os.environ.get("TWILIO_NUMBER")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# agent = VortexAgent() # TODO: should be linked to a specific user/context/session

agents: Dict[str, weakref.ref] = weakref.WeakValueDictionary()

def get_or_create_agent(phone_number: str, db) -> VortexAgent:
    agent = agents.get(phone_number)
    if agent is None:
        chat_history = get_chat_history(db, phone_number) or []
        agent = VortexAgent(context=chat_history)  # Initialize a new agent instance
        agents[phone_number] = agent  # Store it using the phone number as the key
    return agent


def store_message(whatsapp_number, Body, langchain_response, db):
    conversation = Conversation(
        sender=whatsapp_number, message=Body, response=langchain_response
    )
    db.add(conversation)
    db.commit()
    logger.info(f"Conversation #{conversation.id} stored in database")


def get_chat_history(db_session, phone_number: str) -> list:
    return (
        db_session.query(Conversation)
        .filter(Conversation.phone_number == phone_number)
        .order_by(Conversation.created_at.asc())
        .all()
        or []
    )


def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}",
        )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")


async def handle_wapp_message(
    request: Request, Body: str = Form(), db: Session = Depends(get_db)
):
    # Extract the phone number from the incoming webhook request
    form_data = await request.form()
    whatsapp_number = form_data["From"].split("whatsapp:")[-1]
    print(f"Sending the LangChain response to this number: {whatsapp_number}")
    agent = get_or_create_agent(whatsapp_number, db)
    # Get the generated text from the LangChain agent
    langchain_response = agent.get_response(Body)
    # Store the conversation in the database
    try:
        store_message(whatsapp_number, Body, langchain_response, db)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error storing conversation in database: {e}")
    # Lastly, send message back to user
    send_message(whatsapp_number, langchain_response)
    return {"response": langchain_response}
