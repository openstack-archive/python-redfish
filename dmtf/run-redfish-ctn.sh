#!/bin/bash

# Th -p option needs to be after the run command. No warning is given if before but doesn't work
docker run -p 8000:80 localhost:5000/pb:docker-redfish
