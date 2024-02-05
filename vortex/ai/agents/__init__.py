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


from typing import Callable, Dict, Union

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from vortex.ai.llm import LLM
from vortex.ai.tools import tools


class VortexAgent(BaseModel):
    llm: LLM = None
    memory: ConversationBufferMemory = None
    tools: list = tools
    hub_prompt: str = "hwchase17/openai-tools-agent"
    agent_type: str = "openai_tools_agent"
    agent: Runnable = None  # Type hinting that it will be populated later

    def __init__(self, **data):
        super().__init__(**data)
        self.llm = LLM().llm
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.tools = tools
        self.agent = AgentFactory.create_agent(self.agent_type, **data)

    class Config:
        arbitrary_types_allowed = True

    def get_agent_response(self, user_content: str):
        agent_executor = AgentExecutor(
            agent=self.agent, tools=self.tools, verbose=True, memory=self.memory
        )
        user_input = {"input": user_content}
        response = agent_executor.invoke(user_input)
        return response["output"]


class AgentFactory:
    agent_type_map = {
        "openai_tools_agent": lambda **kwargs: create_openai_tools_agent(
            llm=kwargs.get("llm"),
            tools=kwargs.get("tools"),
            prompt=kwargs.get("hub_prompt"),
        )
    }

    @staticmethod
    def create_agent(agent_type: str, **kwargs):
        if agent_type not in AgentFactory.agent_type_map:
            raise NotImplementedError(f"Agent Type {agent_type} not implemented.")
        return AgentFactory.agent_type_map[agent_type](**kwargs)


# %%
