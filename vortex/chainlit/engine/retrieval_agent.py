import chainlit as cl
from chainlit.input_widget import Select, Slider, Switch
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.tools import DuckDuckGoSearchRun
from langchain.utilities import WikipediaAPIWrapper

# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

search = DuckDuckGoSearchRun()
wikipedia = WikipediaAPIWrapper()


@cl.on_chat_start
async def init():
    settings = await cl.ChatSettings(
        [
            Select(
                id="model",
                label="OpenAI - Model",
                values=[
                    "gpt-3.5-turbo",
                    "gpt-3.5-turbo-1106",
                    "gpt-4",
                    "gpt-4-1106-preview",
                ],
                initial_index=0,
            ),
            Switch(id="streaming", label="OpenAI - Stream Tokens", initial=True),
            Slider(
                id="temperature",
                label="OpenAI - Temperature",
                initial=1,
                min=0,
                max=2,
                step=0.1,
            ),
            Slider(
                id="k",
                label="RAG - Retrieved Documents",
                initial=3,
                min=1,
                max=20,
                step=1,
            ),
        ]
    ).send()

    # Web Search Tool
    search_tool = Tool(
        name="Web Search",
        func=search.run,
        description="A useful tool for searching the Internet to find information on world events, issues, etc. Worth using for general topics. Use precise questions.",
    )

    # Wikipedia Tool
    wikipedia_tool = Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="A useful tool for searching the Internet to find information on world events, issues, etc. Worth using for general topics. Use precise questions.",
    )

    prompt = PromptTemplate(
        template="""Plan: {input}

    History: {chat_history}

    Let's think about answer step by step.
    If it's information retrieval task, solve it like a professor in particular field.""",
        input_variables=["input", "chat_history"],
    )

    plan_prompt = PromptTemplate(
        input_variables=["input", "chat_history"],
        template="""Prepare plan for task execution. (e.g. retrieve current date to find weather forecast)

        Tools to use: wikipedia, web search

        REMEMBER: Keep in mind that you don't have information about current date, temperature, informations after September 2021. Because of that you need to use tools to find them.

        Question: {input}

        History: {chat_history}

        Output look like this:
        '''
            Question: {input}

            Execution plan: [execution_plan]

            Rest of needed information: [rest_of_needed_information]
        '''

        IMPORTANT: if there is no question, or plan is not need (YOU HAVE TO DECIDE!), just populate {input} (pass it as a result). Then output should look like this:
        '''
            input: {input}
        '''
        """,
    )

    llm = ChatOpenAI(
        temperature=settings["temperature"],
        streaming=settings["streaming"],
        model=settings["model"],
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    plan_chain = ConversationChain(
        llm=llm,
        memory=memory,
        input_key="input",
        prompt=plan_prompt,
        output_key="output",
    )

    # Initialize Agent
    agent = initialize_agent(
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        tools=[search_tool, wikipedia_tool],
        llm=llm,
        verbose=True,  # verbose option is for printing logs (only for development)
        max_iterations=3,
        prompt=prompt,
        memory=memory,
    )

    # Store the chain in the user session
    cl.user_session.set("plan_chain", plan_chain)
    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    plan_chain = cl.user_session.get("plan_chain")
    agent = cl.user_session.get("agent")

    # Call the chain asynchronously
    plan_result = await plan_chain.acall(
        message, callbacks=[cl.AsyncLangchainCallbackHandler()]
    )

    # Agent execution
    res = await agent(plan_result)

    # Send the response
    cl.Message(content=res["output"]).send()
