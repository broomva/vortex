# %%

# %%
from databricks_session import DatabricksSQLSession

# %%
spark_sql = DatabricksSQLSession()
# %%
pdf = spark_sql.sql("select * from samples.nyctaxi.trips limit 10")
print(pdf.head())
# %%
sqlalchemy_engine = spark_sql.get_session()
# %%
df = spark_sql.read(sqlalchemy_engine, "samples.nyctaxi.trips")

# %%
from databricks_session import DatabricksJDBCSession

# %%
spark_jdbc = DatabricksJDBCSession().get_session()


# %%

from databricks_session import DatabricksSparkSession

# %%
spark = DatabricksSparkSession().get_session()

# %%
sdf = spark.read.table("samples.nyctaxi.trips")
print(sdf.show())
# %%

from databricks_session import DatabricksMLFlowSession

# %%
mlflow_session = DatabricksMLFlowSession().get_session()

# %%
print(mlflow_session.client.MlflowClient())
# %%
