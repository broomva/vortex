#!/bin/bash

# Start the first process
dagster-webserver -h 0.0.0.0 -p 3000 &

# Start the second process
dagster-daemon run &

# Wait for both processes to finish
wait -n