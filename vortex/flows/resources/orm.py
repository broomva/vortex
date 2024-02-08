# %%
import contextlib
import os
from typing import Optional

from dagster import ConfigurableResource, EnvVar
from sqlalchemy import create_engine, text


class SQLAlchemyResource(ConfigurableResource):
    """
    Represents a resource for executing SQL queries using SQLAlchemy.

    Attributes:
        url (Optional[str]): The URL of the SQLAlchemy database connection.
    """

    url: Optional[str] = EnvVar("SQLALCHEMY_URL")

    @contextlib.contextmanager
    def connect(self):
        engine = create_engine(self.url, pool_pre_ping=True)
        with engine.connect() as connection:
            yield connection

    def query(self, query, params=None):
        """
        Executes the given SQL query with optional parameters.

        Args:
            query (str): The SQL query to execute.
            params (Optional[dict]): Optional parameters to be used in the query.

        Returns:
            The result of the query execution. For SELECT queries, it returns a list of rows.
            For INSERT, UPDATE, DELETE queries, it returns the number of affected rows.
            If an error occurs during query execution, it returns None.
        """
        with self.connect() as connection:
            try:
                # Convert string query to a SQL expression
                query = text(query)
                result = connection.execute(query, params)
                rows = result.fetchall()  # For SELECT queries
            except Exception as e:
                # Handle specific exceptions here
                print(f"An error occurred: {e}")
                rows = result.rowcount or None  # For INSERT, UPDATE, DELETE queries
            return rows
