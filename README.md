# Databricks Session Util
**A simple utility for spark and mlflow session objects**


## Setup

### Quick Install

```shell
python -m pip install databricks_session
```

### Build from source

Clone the repository

```shell
git clone https://github.com/Broomva/databricks_session.git
```

Install the package

``` shell
cd databricks_session && make install
```

### Build manually

After cloning, create a virtual environment

```shell
conda create -n databricks_session python=3.10
conda activate databricks_session
```

Install the requirements

```shell
pip install -r requirements.txt
```

Run the python installation

```shell
python setup.py install
```

## Usage

The deployment requires a .env file created under local folder:

```shell
touch .env
```

It should have a schema like this:

```toml
databricks_experiment_name=''
databricks_experiment_id=''
databricks_host=''
databricks_token=''
databricks_username=''
databricks_password=''
databricks_cluster_id=''
databricks_sql_http_path=''
```

```python
import databricks_session 

# Create a Spark session
spark = DatabricksSparkSession().get_session()

# Connect to MLFLow Artifact Server
mlflow_session = DatabricksMLFlowSession().get_session()
```