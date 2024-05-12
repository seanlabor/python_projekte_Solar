#!/bin/bash

# Define your location (latitude and longitude)
LATITUDE="49.6105"
LONGITUDE="8.0935"

# Get today's date in YYYY-MM-DD format
TODAY=$(date +%F)

# Calculate sunrise and sunset times using the Sunrise-Sunset API
SUNRISE=$(curl -s "https://api.sunrise-sunset.org/json?lat=$LATITUDE&lng=$LONGITUDE&date=$TODAY" | jq -r '.results.sunrise')
SUNSET=$(curl -s "https://api.sunrise-sunset.org/json?lat=$LATITUDE&lng=$LONGITUDE&date=$TODAY" | jq -r '.results.sunset')

# Convert sunrise and sunset times to seconds since midnight
SUNRISE_SECONDS=$(date -d "$SUNRISE" +%s)
SUNSET_SECONDS=$(date -d "$SUNSET" +%s)
CURRENT_TIME_SECONDS=$(date +%s)

current_datetime=$(date +"%Y-%m-%d %T")

# Check if it's daytime (between sunrise and sunset)
if [ $CURRENT_TIME_SECONDS -ge $SUNRISE_SECONDS ] && [ $CURRENT_TIME_SECONDS -lt $SUNSET_SECONDS ]; then
    # Start Docker container if it's daytime
    echo "It is: $current_datetime, the sun is rising, starting docker container" >> sunrise_sunset_docker.log
    docker start sungather_sg12rt
    docker start sungather_sg4rt

else
    # Stop Docker container if it's nighttime
    echo "It is: $current_datetime, the sun is setting, stopping docker container" >> sunrise_sunset_docker.log
    docker stop sungather_sg12rt
    docker stop sungather_sg4rt
fi


sleep 60

# Define the name of the Docker container
container_name="sungather_sg12rt"

# Check if the container is running
if docker ps --format '{{.Names}}' | grep -q "^$container_name$"; then
    echo "$container_name is running" >> sunrise_sunset_docker.log
else
    echo "Error: $container_name is not running" >> sunrise_sunset_docker.log
fi

# Define the name of the Docker container
container_name="sungather_sg4rt"

# Check if the container is running
if docker ps --format '{{.Names}}' | grep -q "^$container_name$"; then
    echo "$container_name is running" >> sunrise_sunset_docker.log
else
    echo "Error: $container_name is not running" >> sunrise_sunset_docker.log
fi