# # %%
# from typing import Callable, Dict, List, Union

# from langchain.agents import AgentExecutor, create_openai_tools_agent
# from langchain.memory import ConversationBufferMemory
# from langchain_core.runnables import Runnable
# from pydantic import BaseModel

# from vortex.ai.llm import LLM
# from vortex.ai.tools import tools

# # Assuming 'tools' is initialized correctly as a list of tool instances
# # and 'LLM()' instantiation correctly provides an LLM instance.


# class VortexAgent:
#     def __init__(
#         self,
#         llm: LLM = LLM().llm,
#         tools: List = tools,
#         hub_prompt: str = "hwchase17/openai-tools-agent",
#         agent_type: str = "openai_tools_agent",
#     ):
#         self.llm = llm
#         self.memory = ConversationBufferMemory(
#             memory_key="chat_history", return_messages=True
#         )
#         self.tools = tools
#         self.hub_prompt = hub_prompt
#         self.agent_type = agent_type
#         self.agent = create_openai_tools_agent(self.llm, self.tools, self.hub_prompt)


#     def get_agent_response(self, user_content: str):

#         agent_executor = AgentExecutor(
#             agent=self.agent, tools=self.tools, verbose=True, memory=self.memory
#         )
#         user_input = {"input": user_content}
#         response = agent_executor.invoke(user_input)
#         return response["output"]


# # class AgentFactory:
# #     agent_type_map = {
# #         "openai_tools_agent": lambda **kwargs: create_openai_tools_agent(
# #             llm=kwargs.get("llm"),
# #             tools=kwargs.get("tools"),
# #             prompt=kwargs.get("hub_prompt"),
# #         )
# #     }

# #     @staticmethod
# #     def create_agent(agent_type: str, **kwargs):
# #         if agent_type not in AgentFactory.agent_type_map:
# #             raise NotImplementedError(f"Agent Type {agent_type} not implemented.")
# #         return AgentFactory.agent_type_map[agent_type](**kwargs)


# # %%
# %%


# from typing import Callable, Dict, Union

# from langchain.agents import AgentExecutor, create_openai_tools_agent
# from langchain.memory import ConversationBufferMemory
# from langchain_core.runnables import Runnable
# from pydantic import BaseModel

# from vortex.ai.llm import LLM
# from vortex.ai.tools import tools

# class VortexAgent(BaseModel):
#     llm: LLM = None
#     memory: ConversationBufferMemory = None
#     tools: list = tools
#     hub_prompt: str = "hwchase17/openai-tools-agent"
#     agent_type: str = "openai_tools_agent"
#     agent: Runnable = None  # Type hinting that it will be populated later

#     def __init__(self, **data):
#         super().__init__(**data)
#         self.llm = LLM().llm
#         self.memory = ConversationBufferMemory(
#             memory_key="chat_history", return_messages=True
#         )
#         self.tools = tools
#         self.agent = AgentFactory.create_agent(self.agent_type, **data)

#     class Config:
#         arbitrary_types_allowed = True

#     def get_agent_response(self, user_content: str):
#         agent_executor = AgentExecutor(
#             agent=self.agent, tools=self.tools, verbose=True, memory=self.memory
#         )
#         user_input = {"input": user_content}
#         response = agent_executor.invoke(user_input)
#         return response["output"]


# class AgentFactory:
#     agent_type_map = {
#         "openai_tools_agent": lambda **kwargs: create_openai_tools_agent(
#             llm=kwargs.get("llm"),
#             tools=kwargs.get("tools"),
#             prompt=kwargs.get("hub_prompt"),
#         )
#     }

#     @staticmethod
#     def create_agent(agent_type: str, **kwargs):
#         if agent_type not in AgentFactory.agent_type_map:
#             raise NotImplementedError(f"Agent Type {agent_type} not implemented.")
#         return AgentFactory.agent_type_map[agent_type](**kwargs)


# %%



# %%
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import \
    format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import \
    OpenAIToolsAgentOutputParser
from langchain.prompts import MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel

from vortex.ai.llm import LLM
from vortex.ai.tools import tools

MEMORY_KEY = "chat_history"


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
        tools: list = tools,
        hub_prompt: str = "hwchase17/openai-tools-agent",
        agent_type="vortex_tools_agent",
    ):
        self.llm: LLM = llm
        self.tools: list = tools
        self.hub_prompt: str = hub_prompt
        self.agent_type: str = agent_type
        self.chat_history: list = []
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are very powerful assistant.",
                ),
                MessagesPlaceholder(variable_name=MEMORY_KEY),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
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
            agent=self.agent, tools=self.tools, verbose=True
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
            {"input": user_content, "chat_history": self.chat_history},
            functions=functions,
        )
        self.chat_history.extend(
            [
                HumanMessage(content=user_content),
                AIMessage(content=response["output"]),
            ]
        )
        return response["output"]

# %%
