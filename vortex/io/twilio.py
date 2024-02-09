# %%
import ast
import base64
import logging
import os
import pickle
import weakref
from datetime import datetime
from typing import Dict

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, Request
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from twilio.rest import Client

from vortex.ai.agents import VortexAgent
from vortex.api.data_models import (ChatsHistory, Conversation, SessionLocal,
                                    get_db)

# db = SessionLocal()
# phone_number = ''
# agent = get_or_create_agent(phone_number, db)
# agent.get_response('hi there, my name is carlos')
# agent_history = agent.chat_history
# history = pickle.dumps(agent_history)
# store_chat_history(phone_number, agent_history, db)

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = "+14155238886" or os.environ.get("TWILIO_NUMBER")

agents: Dict[str, weakref.ref] = weakref.WeakValueDictionary()


def get_or_create_agent(phone_number: str, db) -> VortexAgent:
    agent = agents.get(phone_number)
    try:
        chat_history = get_chat_history(db, phone_number)
    except Exception as e:
        logger.error(f"Error getting chat history for {phone_number}: {e}")
        chat_history = []
    print(f"Chat history: {chat_history}")
    if agent is not None and chat_history:  # Same session stil kept
        print(f"Using existing agent {agent}")
    elif agent is None and chat_history:  # New session but existing user
        print(f"Using reloaded agent with history {chat_history}")
        agent = VortexAgent(context=chat_history)  # Initialize a new agent instance
    elif agent is None and not chat_history:
        print("Using a new agent")
        agent = VortexAgent()
    agents[phone_number] = agent
    return agent


def store_message(whatsapp_number, Body, langchain_response, db):
    conversation = Conversation(
        sender=whatsapp_number, message=Body, response=langchain_response
    )
    db.add(conversation)
    db.commit()
    logger.info(f"Conversation #{conversation.id} stored in database")


def store_chat_history(whatsapp_number, agent_history, db):
    history = pickle.dumps(agent_history)
    # Upsert statement
    stmt = (
        insert(ChatsHistory)
        .values(
            sender=whatsapp_number,
            history=str(history),
            updated_at=datetime.utcnow()  # Explicitly set updated_at on insert
        )
        .on_conflict_do_update(
            index_elements=["sender"],  # Specify the conflict target
            set_={
                "history": str(history),  # Update the history field upon conflict
                "updated_at": datetime.utcnow()  # Update the updated_at field upon conflict
            },
        )
    )
    # Execute the upsert
    db.execute(stmt)
    db.commit()
    logger.info(f"Upsert chat history for user {whatsapp_number} with statement {stmt}")


def get_chat_history(db_session, phone_number: str) -> list:
    history = (
        db_session.query(ChatsHistory)
        .filter(ChatsHistory.sender == phone_number)
        .order_by(ChatsHistory.updated_at.asc())
        .all()
    ) or []
    if not history:
        return []
    chat_history = history[0].history
    print(chat_history)
    loaded = pickle.loads(ast.literal_eval(chat_history))
    print(f"loaded history {loaded}")
    return loaded


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
        store_chat_history(whatsapp_number, agent.chat_history, db)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error storing conversation in database: {e}")
    # Lastly, send message back to user
    send_message(whatsapp_number, langchain_response)
    return {"response": langchain_response}


# %%
