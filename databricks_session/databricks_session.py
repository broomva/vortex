from pydantic import BaseSettings
from typing import Optional
import os
from pydantic import validator
from databricks import sql as adb_sql
import os
import pandas as pd
import re
import mlflow

def init():
    print("Databricks Session Utility Installed")


class SparkSession(BaseSettings):
    ...

    class Config:
        env_file = ".env"


class DatabricksSparkSession(SparkSession):
    databricks_token: str
    databricks_host: str
    databricks_cluster_id: str
    spark: Optional[object] = None

    def get_session(self):
        from databricks.connect import DatabricksSession

        print("Creating a Databricks Compute Cluster Spark Session")
        connection_string = f"sc://{self.databricks_host}:443/;token={self.databricks_token};x-databricks-cluster-id={self.databricks_cluster_id}"
        self.spark = DatabricksSession.builder.remote(
            conn_string=connection_string
        ).getOrCreate()
        return self.spark


class DatabricksJDBCSession(SparkSession):
    databricks_token: str
    databricks_username: str
    databricks_host: str
    databricks_cluster_id: str
    databricks_sql_http_path: str
    spark: Optional[object] = None

    def get_session(self):
        # create a local spark session and load the databricks_session/jars/DatabricksJDBC42.jar
        from pyspark.sql import SparkSession

        self.spark = (
            SparkSession.builder.appName("Databricks JDBC Session")
            .config("spark.jars", "databricks_session/jars/DatabricksJDBC42.jar")
            .getOrCreate()
        )
        return self.spark

    def read(self, table: str):
        spark_df = (
            self.spark.read.format("jdbc")
            .option(
                "url",
                f"jdbc:databricks://{self.databricks_host}:443;HttpPath={self.databricks_sql_http_path}",
            )
            .option("dbtable", table)
            .option("user", self.databricks_username)
            .option("password", self.databricks_token)
            .option("driver", "com.simba.spark.jdbc.Driver")
            .load()
        )
        return spark_df


class DatabricksSQLSession(SparkSession):
    databricks_token: str
    databricks_host: str
    databricks_sql_http_path: str
    engine: Optional[object] = None

    def get_session(self):
        from sqlalchemy import create_engine

        # Create a connection
        self.engine = create_engine(
            f"databricks+connector://token:{self.databricks_token}@{self.databricks_host}:443/default",
            connect_args={
                "http_path": self.databricks_sql_http_path,
            },
        )
        return self.engine

    def read(self, engine, table):
        from sqlalchemy import MetaData, Table, select
        from sqlalchemy.orm import sessionmaker
        import pandas as pd

        # create a Table object
        metadata = MetaData(bind=engine)
        table = Table(table, metadata, autoload=True)

        # run a SQL query
        result = select([table]).execute()

        # convert the result to pandas DataFrame
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df

        # # Run a SQL query within a session
        # with sessionmaker(bind=self.engine) as session:
        #     # Create a Table object
        #     metadata = MetaData(bind=session)
        #     table = Table(table, metadata, autoload=True)
        #     result = select([table]).execute()

        #     # Convert the result to a pandas DataFrame
        #     df = pd.DataFrame(result.fetchall(), columns=result.keys())
        #     return df

    def query(self, query):
        import pandas as pd

        # Execute the SQL query using Pandas
        query_result = pd.read_sql(query, self.engine)
        return query_result

    def sql(self, query) -> pd.DataFrame:
        """
        Executes databricks sql query and returns result as data as dataframe.
        Example of parameters
        :param sql: sql query to be executed
        """
        print("Opening a Databricks SQL Cursor Connection")
        try:
            with adb_sql.connect(
                server_hostname=self.databricks_host,
                http_path=self.databricks_sql_http_path,
                access_token=self.databricks_token,
            ) as adb_connection:
                try:
                    with adb_connection.cursor() as cursor:
                        cursor.execute(query)
                        column_names = [desc[0] for desc in cursor.description]
                        data = cursor.fetchall()
                        df = pd.DataFrame(data, columns=column_names)
                        return df
                except Exception as e:
                    print(f"Error in cursor {e}")
        except Exception as e:
            print(f"Error in connection {e}")


class MLFlowSession(BaseSettings):
    deployment_client: Optional[object] = None

    class Config:
        env_file = ".env"

    def get_deployment_client(self, client_name: str):
        from mlflow.deployments import get_deploy_client

        self.deployment_client = get_deploy_client(client_name)
        return self.deployment_client


class DatabricksMLFlowSession(MLFlowSession):
    databricks_experiment_name: str = "mlflow_experiments"
    databricks_experiment_id: Optional[str] = None
    databricks_username: Optional[str] = None
    databricks_token: Optional[str] = None
    databricks_host: Optional[str] = None
    databricks_password: Optional[str] = databricks_token
    _mlflow_tracking_uri: Optional[str] = "databricks"

    @validator("databricks_host", pre=True, always=True)
    def check_https_pattern(cls, path):
        if not re.match(r"^https://", path):
            path = "https://" + path
        return path

    def get_session(self):
        print("Creating a Databricks MLFlow Session")
        os.environ["experiment_id"] = self.databricks_experiment_id
        # Set the Databricks credentials
        os.environ["DATABRICKS_HOST"] = self.databricks_host
        os.environ["DATABRICKS_TOKEN"] = self.databricks_token
        os.environ["MLFLOW_TRACKING_URI"] = self._mlflow_tracking_uri
        os.environ["DATABRICKS_USERNAME"] = self.databricks_username
        os.environ["DATABRICKS_PASSWORD"] = self.databricks_password

        # Set the tracking uri
        mlflow.set_tracking_uri(self._mlflow_tracking_uri)
        mlflow.set_experiment(self.databricks_experiment_name)

        return mlflow
