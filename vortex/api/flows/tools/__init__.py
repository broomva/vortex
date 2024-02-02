from langchain.agents import Tool

from .scrapping import scrape_website, scrape_website_selenium
from .search import search

tools = [
    Tool(
        name="Search",
        func=search,
        description="Useful for when you need to answer questions about current events, data. You should ask targeted questions",
    ),
    Tool(
        name="Scrape Website",
        func=scrape_website,
        description="Useful when you need to get data from a website url; DO NOT make up any url, the url should only be from the search results",
    ),
    Tool(
        name="Scrape Website with Selenium",
        func=scrape_website_selenium,
        description="Useful when you need to get data from a website url and the regular Scrape Website method is not working correctly; DO NOT make up any url, the url should only be from the search results",
    ),
]
