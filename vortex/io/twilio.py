# %%
import os

from dotenv import load_dotenv
from fastapi import Depends, Form, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from twilio.rest import Client

from vortex.ai.agents import VortexSession
from vortex.api.datamodels import get_db, wapp

# db = SessionLocal()
# phone_number = ''
# agent = get_or_create_agent(phone_number, db)
# agent.get_response('hi there, my name is carlos')
# agent_history = agent.chat_history
# history = pickle.dumps(agent_history)
# store_chat_history(phone_number, agent_history, db)

load_dotenv()

# Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = os.environ.get("TWILIO_NUMBER") or "+19853323941"

vortex_session = VortexSession()


def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}",
        )
        print(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        print(f"Error sending message to {to_number}: {e}")


async def handle_wapp_message(
    request: Request, Body: str = Form(), db: Session = Depends(get_db)
):
    # Extract the phone number from the incoming webhook request
    # raw_data = await request.form()
    # form_data = wapp.TwilioRequest(**raw_data)
    # whatsapp_number = form_data.phone_number
    form_data = await request.form()
    whatsapp_number = form_data["From"].split("whatsapp:")[-1]
    print(f"Sending the LangChain response to this number: {whatsapp_number}")
    agent = vortex_session.get_or_create_agent(whatsapp_number, db)
    # Get the generated text from the LangChain agent
    langchain_response = agent.get_response(f"user_id: {whatsapp_number}, user_request: {Body}")
    # Store the conversation in the database
    try:
        vortex_session.store_message(whatsapp_number, Body, langchain_response, db)
        vortex_session.store_chat_history(whatsapp_number, agent.chat_history, db)
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error storing conversation in database: {e}")
    # Lastly, send message back to user
    send_message(whatsapp_number, langchain_response)
    return {"response": langchain_response}


# %%
