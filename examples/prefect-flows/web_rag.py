from prefect import task, flow
from vortex.ai.tools import scrape_website, scrape_website_selenium
from prefect.artifacts import create_markdown_artifact
from vortex.flows.resources import OpenAIResource

openai_resource = OpenAIResource()

@task
def get_article(input_url: str) -> str:
    if not input_url:
        return None
    try:
        try:
            response = scrape_website(input_url)
        except Exception:
            response = None
        if response is None:
            response = scrape_website_selenium(input_url)
    except Exception as e:
        raise e
    return response

@task
def summarize_article(article_text: str) -> str:
    if not article_text:
        return None
    user_query = f"Please generate a new fresh article of similar length based on this information: \n{article_text}"
    response = openai_resource.get(user_query)
    return response

@flow(log_prints=True)
def web_rag_flow(input_url: str = "https://github.com/Broomva/vortex"):
    article_text = get_article(input_url)
    article_summary = summarize_article(article_text)
    print(article_summary)

if __name__ == "__main__":
    web_rag_flow.deploy(
        name="web-rag-flow", 
        work_pool_name="broomva-worker",
        parameters={"input_url": "https://github.com/Broomva/vortex"},
    )