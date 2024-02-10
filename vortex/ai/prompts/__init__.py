from typing import cast

from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    MessagesPlaceholder)

VORTEX_SYSTEM_PROMPT = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.
"""

# VORTEX_SYSTEM_PROMPT_SUFFIX = """Begin!

# Question: {input}
# Thought: I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables.
# {agent_scratchpad}"""

VORTEX_SYSTEM_PROMPT_FUNCTIONS_SUFFIX = """I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables."""


MEMORY_KEY = "chat_history"

AGENT_SCRATCHPAD = "agent_scratchpad"

# VORTEX_SYSTEM_PROMPT = (
#         "system",
#         "You are very powerful assistant.",
#     )


VORTEX_DEFAULT_PROMPT = [
    SystemMessage(content=cast(str, VORTEX_SYSTEM_PROMPT)),
    MessagesPlaceholder(variable_name=MEMORY_KEY),
    HumanMessagePromptTemplate.from_template("{input}"),
    AIMessage(content=VORTEX_SYSTEM_PROMPT_FUNCTIONS_SUFFIX),
    MessagesPlaceholder(variable_name=AGENT_SCRATCHPAD),
]

vortex_prompt = ChatPromptTemplate.from_messages(VORTEX_DEFAULT_PROMPT)


# VORTEX_DEFAULT_PROMPT = [
#     VORTEX_SYSTEM_PROMPT,
#     MessagesPlaceholder(variable_name=MEMORY_KEY),
#     # AIMessage(content=SQL_FUNCTIONS_SUFFIX),
#     ("user", "{input}"),
#     MessagesPlaceholder(variable_name=AGENT_SCRATCHPAD),
# ]
