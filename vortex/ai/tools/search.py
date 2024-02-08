# %%
import json
import os

import requests

serper_api_key = os.getenv("SERP_API_KEY")


def serper_api_search(query):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {"X-API-KEY": serper_api_key, "Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text
