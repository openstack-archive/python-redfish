#!/bin/bash

# Build the docker container first
docker build -t localhost:5000/redfish-simulator:latest .
# Th -p option needs to be after the run command. No warning is given if before but doesn't work
docker rm "redfish-simulator"
docker run -d -p 8000:80 --name "redfish-simulator" localhost:5000/redfish-simulator:latest
echo "Launch your browser and load http://localhost:8000/redfish/v1"
