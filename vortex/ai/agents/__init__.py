# %%
import ast
import os
import pickle
import weakref
from datetime import datetime
from tempfile import TemporaryDirectory
from typing import Dict

from langchain.agents import AgentExecutor, load_tools
from langchain.agents.format_scratchpad.openai_tools import \
    format_to_openai_tool_messages
# from langchain.agents.output_parsers.openai_functions import OpenAIFunctionsAgentOutputParser
from langchain.agents.output_parsers.openai_tools import \
    OpenAIToolsAgentOutputParser
from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits import (FileManagementToolkit,
                                                SQLDatabaseToolkit)
from langchain_core.messages import AIMessage, HumanMessage
from sqlalchemy.dialects.postgresql import insert

from vortex.ai.llm import LLM
from vortex.ai.prompts import vortex_prompt
from vortex.ai.router import semantic_layer
from vortex.ai.tools import tools as vortex_tools
from vortex.datamodels.wapp import ChatsHistory, Conversation


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
        # hub_prompt: str = "hwchase17/openai-tools-agent",
        agent_type="vortex_wapp_tools_agent",
        context: list = [],  # represents the chat history, can be pulled from a db
        user_id: str = None,
    ):
        self.llm: LLM = llm
        self.tools: list = tools
        # self.hub_prompt: str = hub_prompt
        self.agent_type: str = agent_type
        self.chat_history: list = context
        self.user_id: str = user_id

        # self.prompt = vortex_prompt

        self.db = SQLDatabase.from_uri(os.environ.get("SQLALCHEMY_URL"))
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.context = self.toolkit.get_context()
        self.prompt = vortex_prompt.partial(**self.context)
        self.sql_tools = self.toolkit.get_tools()
        self.working_directory = TemporaryDirectory()
        self.file_system_tools = FileManagementToolkit(root_dir=str(self.working_directory.name)).get_tools()
        self.parser = OpenAIToolsAgentOutputParser()
        self.bare_tools = load_tools(
            [
                "llm-math",
                # "human",
                # "wolfram-alpha"
            ],
            llm=self.llm,
        )
        self.agent_tools = self.tools + self.sql_tools + self.bare_tools + self.file_system_tools
        self.llm_with_tools = self.llm.bind_tools(self.agent_tools)
        # self.llm_with_functions = self.llm.bind_functions(self.tools + self.sql_tools)
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
            | self.parser
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent, tools=self.agent_tools, verbose=True
        )

    def get_response(self, user_content: str):
        """
        Gets the response from the agent given user input.

        Args:
            user_content (str): The user input.

        Returns:
            str: The response from the agent.

        """
        routed_content = semantic_layer(query=user_content, user_id=self.user_id)
        response = self.agent_executor.invoke(
            {"input": routed_content, "chat_history": self.chat_history}
        )
        self.chat_history.extend(
            [
                HumanMessage(content=user_content),
                AIMessage(content=response["output"]),
            ]
        )
        return response["output"]


class VortexSession:
    def __init__(self, session_factory):
        """
        Initializes a new instance of the VortexSession class.

        :param session_factory: A callable that returns a new SQLAlchemy Session instance when called.
        """
        self.session_factory = session_factory
        self.agents: Dict[str, weakref.ref] = weakref.WeakValueDictionary()

    def get_or_create_agent(self, user_id: str) -> "VortexAgent":
        """
        Retrieves or creates a VortexAgent for a given user_id.

        :param user_id: The unique identifier for the user.
        :return: An instance of VortexAgent.
        """
        agent = self.agents.get(user_id)
        chat_history = []

        # Obtain a new database session
        try:
            chat_history = self.get_chat_history(user_id)
        except Exception as e:
            print(f"Error getting chat history for {user_id}: {e}")

        # print(f"Chat history: {chat_history}")

        if agent is not None and chat_history:
            print(f"Using existing agent {agent}")
        elif agent is None and chat_history:
            print(f"Using reloaded agent with history {chat_history}")
            agent = VortexAgent(context=chat_history, user_id=user_id)  # Initialize with chat history
        elif agent is None and not chat_history:
            print("Using a new agent")
            agent = VortexAgent(user_id=user_id)  # Initialize without chat history

        self.agents[user_id] = agent
        return agent

    def store_message(self, user_id: str, body: str, response: str):
        """
        Stores a message in the database.

        :param user_id: The unique identifier for the user.
        :param Body: The body of the message sent by the user.
        :param response: The response generated by the system.
        """
        with self.session_factory as db_session:
            conversation = Conversation(sender=user_id, message=body, response=response)
            db_session.add(conversation)
            db_session.commit()
            print(f"Conversation #{conversation.id} stored in database")

    def store_chat_history(self, user_id, agent_history):
        """
        Stores or updates the chat history for a user in the database.

        :param user_id: The unique identifier for the user.
        :param agent_history: The chat history to be stored.
        """
        history = pickle.dumps(agent_history)
        # Upsert statement
        stmt = (
            insert(ChatsHistory)
            .values(
                sender=user_id,
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
        with self.session_factory as db:
            db.execute(stmt)
            db.commit()
            print(f"Upsert chat history for user {user_id} with statement {stmt}")

    def get_chat_history(self, user_id: str) -> list:
        """
        Retrieves the chat history for a user from the database.

        :param db_session: The SQLAlchemy Session instance.
        :param user_id: The unique identifier for the user.
        :return: A list representing the chat history.
        """
        with self.session_factory as db_session:
            history = (
                db_session.query(ChatsHistory)
                .filter(ChatsHistory.sender == user_id)
                .order_by(ChatsHistory.updated_at.asc())
                .all()
            ) or []
        if not history:
            return []
        chat_history = history[0].history
        loaded = pickle.loads(ast.literal_eval(chat_history))
        return loaded


# %%
