# %%
import os
import re

from dotenv import load_dotenv
from fastapi import Depends, Form, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from twilio.rest import Client

from vortex.ai.agents import VortexSession
from vortex.datamodels import get_db

load_dotenv()

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = os.environ.get("TWILIO_NUMBER") or "+19853323941"


def send_message(to_number, body_text):
    """
    Sends a message to the specified WhatsApp number using the Twilio API.

    Parameters:
    - to_number: str. The recipient's WhatsApp number.
    - body_text: str. The text of the message to send.
    """
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}",
        )
        print(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        print(f"Error sending message to {to_number}: {e}")


def send_message_in_parts(whatsapp_number, text, max_length=1600):
    """
    Send the message in parts, ensuring each part is split at a punctuation mark or whitespace
    and below the threshold, using regex for optimal splitting.

    Parameters:
    - whatsapp_number: The recipient's WhatsApp number.
    - text: The text to be sent.
    - max_length: Maximum length of each message part. Defaults to 1600.
    """
    # Pattern to find punctuation followed by a space or just a space, to consider as split points
    pattern = re.compile(r"(\.|\?|!|;|:)\s+|\s")

    parts = []
    start = 0
    while start < len(text):
        # If remaining text is within max_length, just add it and break
        if len(text) - start <= max_length:
            parts.append(text[start:])
            break

        # Find all possible split positions within the next chunk of max_length characters
        chunk = text[start : start + max_length]
        split_positions = [match.start() for match in pattern.finditer(chunk)]

        # If no suitable split position found, enforce split at max_length
        if not split_positions:
            split_pos = max_length
        else:
            # Prefer the last possible split position to maximize chunk size
            split_pos = split_positions[-1] + 1

        parts.append(text[start : start + split_pos])
        start += split_pos

    # Send each part
    for part in parts:
        send_message(whatsapp_number, part)


async def handle_wapp_message(
    request: Request, Body: str = Form(), db: Session = Depends(get_db)
):
    """
    Handles incoming WhatsApp messages, responds using the LangChain agent, and stores the conversation.

    Parameters:
    - request: Request. The request object.
    - Body: str. The body of the WhatsApp message.
    - db: Session. The SQLAlchemy session for database operations.
    """
    vortex_session = VortexSession(db)
    form_data = await request.form()
    whatsapp_number = form_data["From"].split("whatsapp:")[-1]
    print(f"Sending the LangChain response to this number: {whatsapp_number}")
    agent = vortex_session.get_or_create_agent(whatsapp_number)
    # Get the generated text from the LangChain agent
    langchain_response = agent.get_response(user_content=Body)
    # Store the conversation in the database
    try:
        vortex_session.store_message(
            user_id=whatsapp_number, body=Body, response=langchain_response
        )
        vortex_session.store_chat_history(
            user_id=whatsapp_number, agent_history=agent.chat_history
        )
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error storing conversation in database: {e}")

    # Check if the response is larger that 1600, if so, split it into multiple messages and send them
    if len(langchain_response) > 1600:
        send_message_in_parts(whatsapp_number, langchain_response)
    else:
        send_message(whatsapp_number, langchain_response)
        return {"response": langchain_response}
