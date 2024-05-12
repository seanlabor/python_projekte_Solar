#!/bin/bash

EMAIL="msrech@freenet.de"
timestamp=$(date +'%d-%m-%Y')

# Define the filename
LOG_FILE="logs/backup_email.log"

# Check if the file exists
if [ ! -f "$LOG_FILE" ]; then
    # If the file doesn't exist, create it
    touch "$LOG_FILE"
    echo "Log file created: $LOG_FILE"
else
    echo "Log file already exists: $LOG_FILE"
fi


# Create backup directory
mkdir -p /tmp/influxdb_backup_zip

# Run InfluxDB backup
influx backup --bucket bucket_rech --token gNqBY_gn_fN4MBbgaLtcvHE7eMT-J2gKyQuMXn9J6Qr3tFjbKyPBbKaznCGQnPJsnZdvLKEbRkVCAf-ZsPq7Rg== /tmp/influxdb_backup_zip

# Rename CSV files
rename 's/:/_/g' /tmp/influxdb_backup_zip/*.csv

# Destination ZIP file
DESTINATION_ZIP="/tmp/influxdb_backup_zip/influxdb_backup_$timestamp.zip"

# Zip all files in the source directory
zip -r "$DESTINATION_ZIP" /tmp/influxdb_backup_zip/*

# Send email with backup attached
echo "Influx DB Backup vom $timestamp" | mutt -s "Influx DB Backup" -a "$DESTINATION_ZIP" -- "$EMAIL"

echo "InfluxDB Backup sent to $EMAIL at $timestamp" | tee -a LOG_FILE
