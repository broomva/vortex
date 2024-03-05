FROM --platform=linux/amd64 python:3.11

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

RUN pip install dagster-webserver dagster-postgres dagster-aws vortex-python

# Copy your code and workspace to /opt/dagster/app
COPY . /opt/dagster/app/

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

WORKDIR /opt/dagster/app

EXPOSE 3000

# Use the entrypoint script as the entrypoint
ENTRYPOINT ["./entrypoint.sh"]