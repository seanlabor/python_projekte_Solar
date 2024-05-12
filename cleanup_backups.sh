#!/bin/bash

# Directory path
DIRECTORY="/media/rech/49748A3276482A1F/influx_backup"
timestamp=$(date +'%d-%m-%Y')


# Define the filename
LOG_FILE="logs/cleanup_backups.log"

# Check if the file exists
if [ ! -f "$LOG_FILE" ]; then
    # If the file doesn't exist, create it
    touch "$LOG_FILE"
    echo "Log file created: $LOG_FILE"
else
    echo "Log file already exists: $LOG_FILE"
fi

# Change to the directory
cd "$DIRECTORY" || exit

# List directories sorted by modification time, oldest first
OLD_DIRECTORIES=$(ls -t -d */ | head -n -10)

# Remove old directories
if [ -n "$OLD_DIRECTORIES" ]; then
    echo "$timestamp Cleaning up USB Stick, keeping newest 10 InfluxDB backups removing older ones" | tee -a LOG_FILE
    echo "$OLD_DIRECTORIES"
    rm -r $OLD_DIRECTORIES
else
    echo "$timestamp No old directories to remove." | tee -a LOG_FILE
fi
