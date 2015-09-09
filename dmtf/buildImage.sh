#!/bin/bash

# Build and tag images
docker rmi redfish-simulator
docker build -t "redfish-simulator" .
docker tag -f redfish-simulator:latest localhost:5000/redfish-simulator
