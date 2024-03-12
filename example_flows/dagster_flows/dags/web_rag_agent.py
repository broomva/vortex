# %%
from dagster import (
    AssetExecutionContext,
    Definitions,
    MetadataValue,
    ScheduleDefinition,
    asset,
    define_asset_job,
)

from vortex.ai.tools import scrape_website, scrape_website_selenium
from vortex.flows import resources
from vortex.flows.resources import OpenAIResource


@asset(
    group_name="web_rag_agent",
    required_resource_keys={"openai_resource"},
    config_schema={"url": str},
)
def get_article(
    context,
) -> str:
    input_url = context.op_config["url"]
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
            context.log.warning(f"BS4 response was None. Using Selenium...")
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
    group_name="web_rag_agent",
    required_resource_keys={"openai_resource"},
)
def summarize_article(context: AssetExecutionContext, get_article: str) -> str:
    openai_resource: OpenAIResource = context.resources.openai_resource
    if not get_article:
        return None
    user_query = f"""Please generate a new fresh article of similar length based on this information: \n
    {get_article}"""
    response = openai_resource.get(user_query)
    context.add_output_metadata(
        metadata={
            "response": MetadataValue.md(response),
        }
    )
    return response


# Schedule
daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="vortex_web_rag_agent"),
    cron_schedule="0 0 * * *",
)

defs = Definitions(
    assets=[
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
