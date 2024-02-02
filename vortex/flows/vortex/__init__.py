from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)

from vortex.api.flows import resources

from . import vortex_demo_dag
from .vortex_demo_dag.new_row_sensor import new_row_sensor

# Schedule

daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="vortex_demo_dag"),
    cron_schedule="0 0 * * *",
)


defs = Definitions(
    assets=load_assets_from_package_module(vortex_demo_dag),
    sensors=[new_row_sensor],
    schedules=[daily_refresh_schedule],
    resources={
        "openai_resource": resources.OpenAIResource.configure_at_launch(),
        "postgres_resource": resources.PostgresResource.configure_at_launch(),
        "sqlalchemy_resource": resources.SQLAlchemyResource.configure_at_launch(),
    },
)
