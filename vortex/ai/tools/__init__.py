# %%
from dotenv import load_dotenv
from langchain.agents import Tool, load_tools, tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_experimental.utilities import PythonREPL

from vortex.ai.tools.scrapping import scrape_website, scrape_website_selenium
from vortex.ai.tools.search import serper_api_search

load_dotenv()


@tool
def get_word_length(word: str) -> int:
    """
    Returns the length of a word.

    Parameters:
    word (str): The word to calculate the length of.

    Returns:
    int: The length of the word.
    """
    return len(word)


wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=4096)
)

tavily_tool = TavilySearchResults()

serper_api_search_tool = Tool(
    name="serper_api_search",
    func=serper_api_search,
    description="Useful for when you need to answer questions about current events, data. You should ask targeted questions. Prefer Tavily seach tool over this one",
)


scrape_with_bs4_tool = Tool(
    name="scrape_website_with_beautifulsoup",
    func=scrape_website,
    description="Useful when you need to get data from a website url; DO NOT make up any url, the url should only be from the search results. Prefer Tavily seach tool over this one unless explicitly asked to perform a scrapping task. Prefer Selenium tool and if it does not work, then use this one.",
)

scrape_with_selenuim_tool = Tool(
    name="scrape_website_with_selenium",
    func=scrape_website_selenium,
    description="Useful when you need to get data from a website url and the regular Scrape Website method is not working correctly; DO NOT make up any url, the url should only be from the search results. Prefer Tavily seach tool over this one unless explicitly asked to perform a scrapping task",
)


python_repl = PythonREPL()

repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)

tools = [
    get_word_length,
    wikipedia_tool,
    tavily_tool,
    serper_api_search_tool,
    scrape_with_bs4_tool,
    scrape_with_selenuim_tool,
    repl_tool,
]

# %%
