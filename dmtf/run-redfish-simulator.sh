#!/bin/bash

docker ps -a | grep -q "redfish-simulator:latest"
if [ "$?" -eq 0 ]; then
	docker rm "redfish-simulator"
fi
# The -p option needs to be after the run command. No warning is given if before but doesn't work
docker run -d -p 8000:80 --name "redfish-simulator" redfish-simulator:latest
echo "Launch your browser and load http://localhost:8000/redfish/v1"
