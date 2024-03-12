#!/bin/bash

# Start the first process
dagster-webserver -h 0.0.0.0 -p 3000 &

# Start the second process
dagster-daemon run &

# Start the third process
#dagster api grpc --python-file dags/web_rag_agent.py --host 0.0.0.0 --port 4266 &

# Wait for both processes to finish
wait -n