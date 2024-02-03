# %%

import os

import pandas as pd
from dagster import (
    AssetExecutionContext,
    MetadataValue,
    OpExecutionContext,
    RunRequest,
    asset,
    sensor,
)

# from langchain import hub
# from langchain.agents import AgentExecutor, create_openai_tools_agent
# from langchain_openai import ChatOpenAI
from openai import OpenAI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from vortex.api.flows.assets import openai_asset, postgres_asset
from vortex.api.flows.resources import OpenAIResource, PostgresResource
from vortex.api.flows.tools import scrape_website, scrape_website_selenium, tools


@postgres_asset(
    name="get_url",
    group_name="gather_articles",
    query="""
        select url, article_id, email
        from public.airtable_articles aa
        where not exists (
            select 1 
            from public.processed_articles pa 
            where pa.article_id=aa.article_id
        )
        order by aa.article_id asc 
        limit 1
    """,
)
def get_url(context: AssetExecutionContext, response):
    if response:
        url, article_id, email = response[0][0], response[0][1], response[0][2]
    else:
        url, article_id, email = None, None, None
    context.log.info(f"Got url {url}")
    context.add_output_metadata(
        metadata={
            "url": MetadataValue.url(url),
        }
    )
    if not url:
        raise Exception("No url found")
    return url, article_id, email


@asset(
    group_name="gather_articles",
    required_resource_keys={"openai_resource"},
)
def get_article(context, get_url) -> str:
    context.log.info(f"Running get_article with {get_url[0]}")
    if not get_url:
        return None
    try:
        try:
            response = scrape_website(get_url[0])
            context.log.debug(f"BS4 response {response}")
        except Exception as e:
            response = None
        if response is None:
            context.log.warning(f"Selenium response was None. Using BS4")
            response = scrape_website_selenium(get_url[0])
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
    group_name="gather_articles",
    required_resource_keys={"openai_resource"},
)
def summarize_article(context: AssetExecutionContext, get_article: str) -> str:
    openai_resource: OpenAIResource = context.resources.openai_resource
    if not get_article:
        return None
    user_query = f"Please generate a new fresh article of similar length based on this information: {get_article}"
    response = openai_resource.get(user_query)
    context.add_output_metadata(
        metadata={
            "response": MetadataValue.md(response),
        }
    )
    return response


@asset(
    group_name="gather_articles",
    required_resource_keys={"postgres_resource"},
)
def update_articles_table_with_summary(
    context, summarize_article, get_article, get_url
):
    postgres_resource: PostgresResource = context.resources.postgres_resource
    query = """
        INSERT INTO public.processed_articles (article_id, url, content, summary, created_at, reprocess)
        VALUES (%s, %s, %s, %s, NOW(), false)
        ON CONFLICT (article_id) DO UPDATE
        SET 
            url = EXCLUDED.url,
            content = EXCLUDED.content,
            summary = EXCLUDED.summary,
            created_at = EXCLUDED.created_at,
            reprocess = EXCLUDED.reprocess
    """
    response = postgres_resource.query(
        query, (get_url[1], get_url[0], get_article, summarize_article)
    )
    context.log.info(f"Running write_summary with {query}")
    context.add_output_metadata(
        metadata={
            "response": MetadataValue.md(str(response)),
        }
    )
    return response


@asset(
    deps=[update_articles_table_with_summary],
    group_name="gather_articles",
)
def send_email_with_sendgrid(context, get_url, summarize_article):
    email = get_url[2]
    message = Mail(
        from_email="carlos@broomva.tech",
        to_emails=[email, "carlos@broomva.tech"],
        subject="Here is your URL summary! 🎉",
        plain_text_content=summarize_article,
    )

    context.log.info(f"Sending email to {email}")
    context.log.info(f"Sending email with {summarize_article}")

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        context.log.info(f"Email sent. Status code: {response.status_code}")
    except Exception as e:
        context.log.error(f"Failed to send email: {e}")
        raise e


# @postgres_asset(
#     name="update_articles_table_with_summary",
#     group_name="gather_articles",
#     query="""
#         INSERT INTO public.processed_articles (article_id, url, content, summary, created_at, reprocess)
#         VALUES (%s, %s, %s, %s, NOW(), false)
#         ON CONFLICT (article_id) DO UPDATE
#         SET
#             url = EXCLUDED.url,
#             content = EXCLUDED.content,
#             summary = EXCLUDED.summary,
#             created_at = EXCLUDED.created_at,
#             reprocess = EXCLUDED.reprocess
#     """,
#     # params=(get_url()[1], get_url()[0], get_article(), summarize_article())
# )
# def update_articles_table_with_summary(
#     context, response, **{}
# ):
#     if response:
#         return response


# @asset(
#     deps=[update_articles_table_with_summary],
#     group_name="articles_sumarization",
#     required_resource_keys={"postgres_resource"},
# )
# def get_articles_summaries(context: AssetExecutionContext):
#     postgres_resource = context.resources.postgres_resource
#     response = postgres_resource.run_query(
#         "select summary, url, article_id from public.processed_articles order by article_id desc limit 3"
#     )
#     if response:
#         summaries = []
#         urls = []
#         articles = []
#         for i in response:
#             summaries.append(i[0])
#             urls.append(i[1])
#             articles.append(i[2])
#     context.log.info(f"Got articles {summaries}")
#     context.add_output_metadata(
#         metadata={
#             "articles": MetadataValue.md(str(summaries)),
#         }
#     )
#     return summaries, urls, articles


# @asset(
#     group_name="articles_sumarization",
#     required_resource_keys={"openai_resource"},
# )
# def consolidated_summary(context: AssetExecutionContext, get_articles_summaries):
#     openai_resource = context.resources.openai_resource
#     user_query = f"Please generate a new fresh article summarizing based on these articles, separate each article and include sources: {get_articles_summaries}"
#     context.log.info(f"Summarizing {user_query}")
#     response = openai_resource.get_completion(user_query)
#     context.log.info(f"Got response {response}")
#     context.add_output_metadata(
#         metadata={
#             "response": MetadataValue.md(str(response)),
#         }
#     )
#     return response


# @asset(
#     group_name="articles_sumarization",
#     required_resource_keys={"postgres_resource"},
# )
# def write_consolidated_summary(context, consolidated_summary, get_articles_summaries):
#     postgres_resource = context.resources.postgres_resource
#     urls = get_articles_summaries[1]
#     articles_ids = get_articles_summaries[2]
#     # Create a dictionary where the keys are article_ids and the values are urls
#     url_dict = {article_id: url for article_id, url in zip(articles_ids, urls)}
#     # Convert the dictionary to a JSON string
#     urls = json.dumps(url_dict)
#     query = f"""
#         INSERT INTO public.articles_summary (summary, dependencies, created_at)
#         VALUES (%s, %s, NOW())
#     """
#     context.log.info(f"Running write_consolidated_summary with {query}")
#     response = postgres_resource.run_query(query, (consolidated_summary, urls))
#     context.add_output_metadata(
#         metadata={
#             "response": MetadataValue.md(str(response)),
#         }
#     )
#     return response


# # %%


@sensor(job_name="vortex_demo_dag", minimum_interval_seconds=420)
def new_row_sensor(postgres_resource: PostgresResource, context: OpExecutionContext):
    rows = postgres_resource.query(
        """
        select article_id 
        from public.airtable_articles aa
        where not exists (
            select 1 
            from public.processed_articles pa 
            where pa.article_id=aa.article_id
        )
        order by aa.article_id asc 
        limit 1
        """
    )
    article_id = rows[0][0] if rows else None
    metadata = {
        "article_id": article_id,
        "timestamp": pd.Timestamp.now().isoformat() if article_id else "",
    }
    # context.add_output_metadata(metadata=metadata)
    context.log.info(f"Got id {article_id}")

    if rows:
        # Trigger the job run
        yield RunRequest(
            run_key=f"new_article_trigger_id_{metadata['article_id']}_{metadata['timestamp']}",
            run_config={},
        )


# %%


from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)

from vortex.api.flows import resources

# from .vortex_demo_dag.new_row_sensor import new_row_sensor

# Schedule

daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="vortex_demo_dag"),
    cron_schedule="0 0 * * *",
)


defs = Definitions(
    assets=[
        get_url,
        get_article,
        summarize_article,
        update_articles_table_with_summary,
        send_email_with_sendgrid,
    ],
    sensors=[new_row_sensor],
    schedules=[daily_refresh_schedule],
    resources={
        "openai_resource": resources.OpenAIResource.configure_at_launch(),
        "postgres_resource": resources.PostgresResource.configure_at_launch(),
        "sqlalchemy_resource": resources.SQLAlchemyResource.configure_at_launch(),
    },
)
