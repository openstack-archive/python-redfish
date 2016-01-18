#!/bin/bash

# Build and tag images
docker rmi redfish-simulator
docker build -t "redfish-simulator" .
