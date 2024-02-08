"""
This file is part of the Vortex project, developed by broomva.tech.

Vortex is an open-source project released under the MIT License.
See the LICENSE file at the root of the Vortex project for more details.

The code in this file is subject to the intellectual property rights of broomva.tech.
You may not use this file except in compliance with the License.
"""

import contextlib
import os
from typing import Optional

import psycopg2
from dagster import ConfigurableResource, EnvVar

# from dagster import (
#     AssetExecutionContext,
#     Definitions,
#     InitResourceContext,
#     asset,
#     resource,
# )

# class FancyDbResource:
#     def __init__(self, conn_string: str) -> None:
#         self.conn_string = conn_string

#     def execute(self, query: str) -> None:
#         ...

# @resource(config_schema={"conn_string": str})
# def fancy_db_resource(context: InitResourceContext) -> FancyDbResource:
#     return FancyDbResource(context.resource_config["conn_string"])


class PostgresResource(ConfigurableResource):
    """
    The `PostgresResource` class represents a resource for connecting to a PostgreSQL database.
    It provides methods for executing queries and fetching results from the database.

    Attributes:
        database (Optional[str]): The name of the PostgreSQL database.
        username (Optional[str]): The username for connecting to the database.
        password (Optional[str]): The password for connecting to the database.
        host (Optional[str]): The host address of the database server.
        port (Optional[str]): The port number of the database server.

    Methods:
        run_query(query, params=None): Executes a query on the PostgreSQL database
        and returns the fetched rows.

    """

    database: Optional[str] = EnvVar("POSTGRES_DATABASE")
    username: Optional[str] = EnvVar("POSTGRES_USERNAME")
    password: Optional[str] = EnvVar("POSTGRES_PASSWORD")
    host: Optional[str] = EnvVar("POSTGRES_HOST")
    port: Optional[str] = EnvVar("POSTGRES_PORT")

    @contextlib.contextmanager
    def connect(self):
        """
        Connects to the PostgreSQL database using the provided credentials.

        Returns:
            cursor: A cursor object for executing SQL queries.
        """
        with psycopg2.connect(
            dbname=self.database,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            options="-c client_encoding=utf8",
        ) as conn:
            yield conn.cursor()

    def query(self, query, params=None):
        """
        Executes the given query on the PostgreSQL database and returns the result.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): The parameters to be passed to the query. Defaults to None.

        Returns:
            list: The result of the query as a list of tuples, or None if no rows are returned.
        """
        with self.connect() as cursor:
            cursor.execute(query, params)
            try:
                rows = cursor.fetchall()
            except psycopg2.ProgrammingError as e:
                # Handle specific exceptions here
                print(f"An error occurred: {e}")
                rows = cursor.rowcount or None  # For INSERT, UPDATE, DELETE queries
            cursor.close()
            return rows
