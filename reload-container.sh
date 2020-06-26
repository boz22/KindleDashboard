#!/bin/sh

#Run this with sudo 
docker build -t boz22/kindledashboard .
docker stop kindledashboard
docker rm kindledashboard_container
docker run --name kindledashboard_container --restart always -d -p 5000:5000 boz22/kindledashboard
