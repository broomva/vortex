from functools import update_wrapper, wraps

from dagster import AssetExecutionContext, MetadataValue, asset

from vortex.flows.resources.completion import OpenAIResource
from vortex.flows.resources.postgres import PostgresResource


def postgres_asset(name: str, group_name: str, query: str, params=None, deps=None):
    def decorator(func):
        @wraps(func)
        @asset(
            name=name,
            group_name=group_name,
            required_resource_keys={"postgres_resource"},
            deps=deps,
        )
        def wrapper(context: AssetExecutionContext, **kwargs):
            postgres_resource: PostgresResource = context.resources.postgres_resource
            try:
                context.log.info(f"Running: \n{query}")
                response = postgres_resource.query(query=query, params=params)
                # Call the decorated function with the query result
                context.add_output_metadata(
                    metadata={
                        "postgres_response": MetadataValue.md(str(response)),
                    }
                )
                return func(context, response, **kwargs)
            except Exception as e:
                context.log.error(f"Error in asset {func.__name__}: {e}")
                raise e

        # Update wrapper function to reflect the name and docstring of the decorated function
        update_wrapper(wrapper, func)
        return wrapper

    return decorator


def openai_asset(name: str, group_name: str, query: str):
    def decorator(func):
        @wraps(func)
        @asset(
            name=name, group_name=group_name, required_resource_keys={"openai_resource"}
        )
        def wrapper(context: AssetExecutionContext):
            openai_resource: OpenAIResource = context.resources.openai_resource
            try:
                response = openai_resource.get(query)
                context.add_output_metadata(
                    metadata={
                        "openai_response": MetadataValue.md(response),
                    }
                )
                return response
            except Exception as e:
                context.log.error(f"Error in asset {func.__name__}: {e}")
                raise e

        update_wrapper(wrapper, func)
        return wrapper

    return decorator
