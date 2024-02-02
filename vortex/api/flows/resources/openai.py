import os
from typing import Optional

from dagster import ConfigurableResource
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from openai import OpenAI

from ..tools import tools

load_dotenv()


class OpenAIResource(ConfigurableResource):
    api_key: Optional[str] = (
        None or os.getenv("TOGETHER_API_KEY") or os.getenv("OPENAI_API_KEY")
    )
    base_url: Optional[str] = os.getenv("OPENAI_API_BASE_URL")
    # client: Optional[OpenAI] = None
    model: Optional[str] = (
        os.getenv("OPENAI_MODEL_NAME") or "mistralai/Mixtral-8x7B-Instruct-v0.1"
    )
    # respone_model: Optional[BaseModel] = None
    temperature: Optional[float] = 0.8
    max_tokens: Optional[int] = 8096
    messages: Optional[list] = [
        {
            "role": "system",
            "content": "You are an expert article writter. Include sources, and a social media reporting style.",
        }
    ]
    user_content: Optional[str] = None

    def get(self, user_content):
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        self.messages.append({"role": "user", "content": user_content})
        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            # response_model=self.response_model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content

    def get_agent_response(
        self, user_content: str, hub_prompt: str = "hwchase17/openai-tools-agent"
    ):
        llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            openai_api_base=self.base_url,
            openai_api_key=self.api_key,
        )
        # Construct the OpenAI Tools agent
        agent = create_openai_tools_agent(llm, tools, hub_prompt)
        # Create an agent executor by passing in the agent and tools
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        user_input = {"input": user_content}
        response = agent_executor.invoke(user_input)
        return response["output"]
