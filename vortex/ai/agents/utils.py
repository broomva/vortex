# %%
import logging
import os

from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent, load_tools

# Third-party imports
from twilio.rest import Client

from vortex.ai.llm import LLM

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


# Sending message logic through Twilio Messaging API
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


# def search_wikipedia(query):
#     """Search Wikipedia through the LangChain API
#     and use the OpenAI LLM wrapper and retrieve
#     the agent result based on the received query
#     """
#     # llm = OpenAI(temperature=0, openai_api_key=os.environ.get("OPENAI_API_KEY"))
#     llm = LLM().llm
#     tools = load_tools(["wikipedia"], llm=llm)
#     agent = initialize_agent(
#         tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False
#     )
#     return agent.run(query)


# %%
