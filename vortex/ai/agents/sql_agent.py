# %%
import os

from langchain.agents import create_openai_tools_agent
from langchain.agents.agent import AgentExecutor
from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain_community.agent_toolkits.sql.prompt import SQL_FUNCTIONS_SUFFIX
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

from vortex.ai.llm import LLM

db = SQLDatabase.from_uri(os.environ.get("SQLALCHEMY_URL"))
llm = LLM().llm
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

# vortex_oai_tools = functions = [convert_to_openai_function(t) for t in vortex_tools]

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
context = toolkit.get_context()
tools = toolkit.get_tools()  # + vortex_oai_tools

messages = [
    HumanMessagePromptTemplate.from_template("{input}"),
    AIMessage(content=SQL_FUNCTIONS_SUFFIX),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
]

prompt = ChatPromptTemplate.from_messages(messages)
prompt = prompt.partial(**context)


agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=True,
)

# %%
agent_executor.invoke({"input": "please extract the NER from the article 10"})


# %%


# %%
# # insert your API key here
# openai_api_key = "<>"

# from langchain.agents import create_sql_agent
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
# from langchain.agents.agent_types import AgentType
# from langchain.llms import OpenAI
# # %%
# from langchain.utilities import SQLDatabase

# # %%

# db = SQLDatabase.from_uri("sqlite:///chinook.db")

# # check that the database has been instantiated correctly

# db.get_usable_table_names()


# llm = OpenAI(temperature=0, verbose=True, openai_api_key=openai_api_key)


# agent_executor = create_sql_agent(
#     llm=llm,
#     toolkit=SQLDatabaseToolkit(db=db, llm=llm),
#     verbose=True,
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
# )


# agent_executor.run("How many employees are there?")


# FORMAT_INSTRUCTIONS = """
# Use the following format:
# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [{tool_names}]
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question"""


# agent_executor.run("Describe the playlisttrack table")


# %%


# %pip install --upgrade --quiet  langchain langchain-community langchain-experimental
