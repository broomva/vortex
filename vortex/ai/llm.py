#%%
import os
from typing import Callable, Dict, Union

# from langchain_community.llms import OpenAI
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_openai import ChatOpenAI
from openai import OpenAI
from pydantic import BaseModel


class LLM(BaseModel):
    """This is a stub for the LLM model."""

    provider: str = "ChatOpenAI"
    llm: Union[ChatOpenAI, OpenAI, str, int, float] = None
    messages: list = [
        {
            "role": "system",
            "content": "You are a helpful and friendly assistant.",
        }
    ]

    def __init__(self, **data):
        super().__init__(**data)
        self.llm = LLMFactory.create_llm(self.provider, **data)

    class Config:
        arbitrary_types_allowed = True

    def get(self, user_content):
        if self.provider in ("OpenAI", "TogetherAI"):
            self.messages.append({"role": "user", "content": user_content})
            response = self.llm.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL_NAME", 'gpt-3.5-turbo'),
                messages=self.messages,
                # temperature=self.temperature,
                # max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content


class LLMFactory:
    provider_map: Dict[str, Callable[..., Union[ChatOpenAI, OpenAI, str, int, float]]] = {
        "ChatOpenAI": lambda **kwargs: ChatOpenAI(
            temperature=kwargs.get("temperature", 0.7),
            model_name=kwargs.get("model", "gpt-4-1106-preview"), #os.getenv("OPENAI_MODEL_NAME", 'gpt-3.5-turbo')),
            # openai_api_base=kwargs.get("openai_api_base", os.getenv("OPENAI_API_BASE_URL", None)),
            # openai_api_key=kwargs.get("openai_api_key", os.environ.get("TOGETHER_API_KEY") or os.environ.get("OPENAI_API_KEY")),
            # streaming=kwargs.get("streaming", True),
            callbacks=[],  # StreamingStdOutCallbackHandler()]
        ),
        "OpenAI": lambda **kwargs: OpenAI(
            # model_name=kwargs.get("model", os.getenv("OPENAI_API_KEY", 'gpt-3.5-turbo')),
            api_key=kwargs.get("openai_api_key", os.environ.get("OPENAI_API_KEY")),
            base_url=kwargs.get("openai_api_base", os.getenv("OPENAI_API_BASE_URL", None)),
        ),
        "TogetherAI": lambda **kwargs: OpenAI(
            # model_name=kwargs.get("model", os.getenv("OPENAI_API_KEY", 'gpt-3.5-turbo')),
            api_key=kwargs.get("openai_api_key", os.environ.get("TOGETHER_API_KEY")),
            base_url=kwargs.get("openai_api_base", os.getenv("OPENAI_API_BASE_URL", None)),
        ),
    }

    @staticmethod
    def create_llm(provider: str, **kwargs):
        if provider not in LLMFactory.provider_map:
            raise NotImplementedError(f"LLM provider {provider} not implemented.")
        provider_func = LLMFactory.provider_map[provider]
        return provider_func(**kwargs)
# %%
