# %%
import ast
import os
import pickle
import weakref
from datetime import datetime
from typing import Dict

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import \
    format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import \
    OpenAIToolsAgentOutputParser
from langchain.prompts import MessagesPlaceholder
from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits import (SQLDatabaseToolkit,
                                                create_sql_agent)
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import insert

from vortex.ai.llm import LLM
from vortex.ai.prompts import vortex_prompt
from vortex.ai.tools import tools as vortex_tools
from vortex.api.datamodels.wapp import ChatsHistory, Conversation


class VortexAgent:
    """
    Represents a Vortex Agent that interacts with the user and provides responses using OpenAI tools.

    Attributes:
        llm (LLM): The Language Model Manager used by the agent.
        tools (list): The list of tools used by the agent.
        hub_prompt (str): The prompt for the OpenAI tools agent.
        agent_type (str): The type of the agent.
        chat_history (list): The chat history of the agent.
        llm_with_tools: The Language Model Manager with the tools bound.
        prompt: The chat prompt template for the agent.
        agent: The agent pipeline.
        agent_executor: The executor for the agent.

    Methods:
        get_response: Gets the response from the agent given user input.

    """

    def __init__(
        self,
        llm: LLM = LLM().llm,
        tools: list = vortex_tools,
        hub_prompt: str = "hwchase17/openai-tools-agent",
        agent_type="vortex_wapp_tools_agent",
        context: list = [],  # represents the chat history, can be pulled from a db
    ):
        self.llm: LLM = llm
        self.tools: list = tools
        self.hub_prompt: str = hub_prompt
        self.agent_type: str = agent_type
        self.chat_history: list = context

        # self.prompt = vortex_prompt

        self.db = SQLDatabase.from_uri(os.environ.get("SQLALCHEMY_URL"))
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.context = self.toolkit.get_context()
        self.prompt = vortex_prompt.partial(**self.context)
        self.sql_tools = self.toolkit.get_tools()

        self.llm_with_tools = self.llm.bind_tools(self.tools + self.sql_tools)
        self.agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
                "chat_history": lambda x: x["chat_history"],
            }
            | self.prompt
            | self.llm_with_tools
            | OpenAIToolsAgentOutputParser()
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent, tools=self.tools + self.sql_tools, verbose=True
        )

    def get_response(self, user_content: str):
        """
        Gets the response from the agent given user input.

        Args:
            user_content (str): The user input.

        Returns:
            str: The response from the agent.

        """
        response = self.agent_executor.invoke(
            {"input": user_content, "chat_history": self.chat_history}
        )
        self.chat_history.extend(
            [
                HumanMessage(content=user_content),
                AIMessage(content=response["output"]),
            ]
        )
        return response["output"]


class VortexSession:

    def __init__(
        self,
    ):
        self.agents: Dict[str, weakref.ref] = weakref.WeakValueDictionary()

    def get_or_create_agent(self, phone_number: str, db) -> VortexAgent:
        agent = self.agents.get(phone_number)
        try:
            chat_history = self.get_chat_history(db, phone_number)
        except Exception as e:
            print(f"Error getting chat history for {phone_number}: {e}")
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
        self.agents[phone_number] = agent
        return agent

    def store_message(self, whatsapp_number, Body, langchain_response, db):
        conversation = Conversation(
            sender=whatsapp_number, message=Body, response=langchain_response
        )
        db.add(conversation)
        db.commit()
        print(f"Conversation #{conversation.id} stored in database")

    def store_chat_history(self, whatsapp_number, agent_history, db):
        history = pickle.dumps(agent_history)
        # Upsert statement
        stmt = (
            insert(ChatsHistory)
            .values(
                sender=whatsapp_number,
                history=str(history),
                updated_at=datetime.utcnow(),  # Explicitly set updated_at on insert
            )
            .on_conflict_do_update(
                index_elements=["sender"],  # Specify the conflict target
                set_={
                    "history": str(history),  # Update the history field upon conflict
                    "updated_at": datetime.utcnow(),  # Update the updated_at field upon conflict
                },
            )
        )
        # Execute the upsert
        db.execute(stmt)
        db.commit()
        print(f"Upsert chat history for user {whatsapp_number} with statement {stmt}")

    def get_chat_history(self, db_session, phone_number: str) -> list:
        history = (
            db_session.query(ChatsHistory)
            .filter(ChatsHistory.sender == phone_number)
            .order_by(ChatsHistory.updated_at.asc())
            .all()
        ) or []
        if not history:
            return []
        chat_history = history[0].history
        # print(chat_history)
        loaded = pickle.loads(ast.literal_eval(chat_history))
        # print(f"loaded history {loaded}")
        return loaded


# %%
