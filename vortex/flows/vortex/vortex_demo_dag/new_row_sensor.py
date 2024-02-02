import pandas as pd
from dagster import OpExecutionContext, RunRequest, sensor
from dotenv import load_dotenv

from .. import resources

load_dotenv()


@sensor(job_name="vortex_demo_dag", minimum_interval_seconds=420)
def new_row_sensor(
    postgres_resource: resources.PostgresResource, context: OpExecutionContext
):
    rows = postgres_resource.run_query(
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
