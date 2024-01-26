# %%
import json
import os
import time
from typing import Optional, Type

import html2text
import requests
from bs4 import BeautifulSoup
from langchain.agents import Tool
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

brwoserless_api_key = os.getenv("BROWSERLESS_API_KEY")
serper_api_key = os.getenv("SERP_API_KEY")


def search(query):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {"X-API-KEY": serper_api_key, "Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def scrape_website(url: str):
    # scrape website, and also will summarize the content based on objective if the content is too large
    # objective is the original objective & task that user give to the agent, url is the url of the website to be scraped

    print("Scraping website...")
    # Define the headers for the request
    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
    }

    # Define the data to be sent in the request
    data = {"url": url}

    # Convert Python object to JSON string
    data_json = json.dumps(data)

    # Send the POST request
    response = requests.post(
        f"https://chrome.browserless.io/content?token={brwoserless_api_key}",
        headers=headers,
        data=data_json,
    )

    # Check the response status code
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup #soup.get_text()
        return text
    else:
        print(f"HTTP request failed with status code {response.status_code}")


def scrape_website_selenium(url):
    # Configure Selenium with a headless browser
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    # Access the webpage
    driver.get(url)

    # Wait for JavaScript to render. Adjust time as needed.
    time.sleep(5)  # Time in seconds

    # Extract the page source
    page_source = driver.page_source

    # Close the browser
    driver.quit()

    # Convert HTML to Markdown
    converter = html2text.HTML2Text()
    markdown = converter.handle(page_source)

    return markdown


tools = [
    Tool(
        name="Search",
        func=search,
        description="useful for when you need to answer questions about current events, data. You should ask targeted questions",
    ),
    Tool(
        name="Scrape Website",
        func=scrape_website,
        description="useful when you need to get data from a website url; DO NOT make up any url, the url should only be from the search results",
    ),
    # ScrapeWebsiteTool(),
]
# %%
