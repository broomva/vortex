# %%
from dagster import (AssetExecutionContext, Definitions, MetadataValue,
                     OpExecutionContext, ScheduleDefinition, asset,
                     define_asset_job, op)

from vortex.ai.tools import scrape_website, scrape_website_selenium
from vortex.flows import resources
from vortex.flows.resources import OpenAIResource


@op(group_name="web_rag", config_schema={'url': str})
def input_url(context):
    response = context.op_config['url']
    context.log.info(f"Got user input url: {response}")
    context.add_output_metadata(
        metadata={
            "response": MetadataValue.md(response),
        }
    )
    return response

@op(group_name="web_rag", config_schema={'user_content': str})
def input_user_content(context):
    response = context.op_config['user_content']
    context.log.info(f"Got user content: {response}")
    context.add_output_metadata(
        metadata={
            "response": MetadataValue.md(response),
        }
    )
    return response
    

@asset(
    group_name="web_rag",
    required_resource_keys={"openai_resource"},
)
def get_article(context, input_url) -> str:
    context.log.info(f"Running get_article with {input_url}")
    if not input_url:
        return None
    try:
        try:
            response = scrape_website(input_url)
            context.log.debug(f"BS4 response {response}")
        except Exception as e:
            response = None
        if response is None:
            context.log.warning(f"Selenium response was None. Using BS4")
            response = scrape_website_selenium(input_url)
            context.log.debug(f"Selenium Scrape response {response}")
    except Exception as e:
        context.log.info(f"Error {e}")
        raise e
    context.log.info(f"Got response {response}")
    context.add_output_metadata(
        metadata={
            "response": MetadataValue.md(response),
        }
    )
    return response


@asset(
    group_name="web_rag",
    required_resource_keys={"openai_resource"},
)
def summarize_article(context: AssetExecutionContext, get_article: str, input_user_content: str) -> str:
    openai_resource: OpenAIResource = context.resources.openai_resource
    if not get_article:
        return None
    user_query = f"""Please generate a new fresh article of similar length based on this information: \n
    {get_article} \n
    {input_user_content}"""
    response = openai_resource.get(user_query)
    context.add_output_metadata(
        metadata={
            "response": MetadataValue.md(response),
        }
    )
    return response

# Schedule

daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="vortex_web_rag"),
    cron_schedule="0 0 * * *",
)

defs = Definitions(
    assets=[
        input_url,
        input_user_content,
        get_article,
        summarize_article,
    ],
    schedules=[daily_refresh_schedule],
    resources={
        "openai_resource": resources.OpenAIResource.configure_at_launch(),
        "postgres_resource": resources.PostgresResource.configure_at_launch(),
        "sqlalchemy_resource": resources.SQLAlchemyResource.configure_at_launch(),
    },
)
