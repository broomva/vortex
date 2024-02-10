from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Text

from vortex.api.datamodels import Base, engine

Base.metadata.create_all(engine)


class Conversation(Base):
    """
    Represents a conversation entity.

    Attributes:
        id (int): The unique identifier of the conversation.
        sender (str): The sender of the message.
        message (str): The message content.
        response (str): The response to the message.
        created_at (datetime): The timestamp of when the conversation was created.
    """

    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String)
    message = Column(String)
    response = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatsHistory(Base):
    """
    Represents the chat history for a sender.

    Attributes:
        sender (str): The sender of the chat.
        history (str): The chat history.
        updated_at (datetime): The timestamp of when the chat history was last updated.
    """

    __tablename__ = "chats_history"
    sender = Column(String, primary_key=True, index=True)
    history = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)


class TwilioRequest(BaseModel):
    """
    Represents a Twilio request object.

    Attributes:
        SmsMessage (str): The SMS message.
        NumMedia (str): The number of media files attached.
        SmsSid (str): The SMS SID.
        SmsStatus (str): The SMS status.
        Body (str): The message body.
        To (str): The recipient's phone number.
        NumSegments (str): The number of message segments.
        MessageSid (str): The message SID.
        AccountSid (str): The account SID.
        From (str): The sender's phone number.
        ApiVersion (str): The Twilio API version.
    """

    SmsMessage: str
    NumMedia: str
    SmsSid: str
    SmsStatus: str
    Body: str
    To: str
    NumSegments: str
    MessageSid: str
    AccountSid: str
    From: str
    ApiVersion: str

    @property
    def phone_number(self):
        """
        Extracts the phone number from the 'From' attribute.

        Returns:
            str: The extracted phone number.
        """
        return self.From.split("whatsapp:")[-1]
