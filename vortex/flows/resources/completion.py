# %%
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()


class OpenAIResource(BaseModel):
    api_key: Optional[str] = (
        None or os.environ.get("TOGETHER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    )
    base_url: Optional[str] = os.environ.get("TOGETHER_API_BASE_URL") or os.environ.get(
        "OPENAI_API_BASE_URL"
    )
    # client: Optional[OpenAI] = None
    model: Optional[str] = (
        os.environ.get("TOGETHER_MODEL_NAME") or "mistralai/Mixtral-8x7B-Instruct-v0.1"
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


# %%
