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
