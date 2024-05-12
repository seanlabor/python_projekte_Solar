  GNU nano 7.2                                                                                backup_influxdb.sh
#!/bin/bash

# Define the filename
LOG_FILE="logs/backup_usb.log"

# Check if the file exists
if [ ! -f "$LOG_FILE" ]; then
    # If the file doesn't exist, create it
    touch "$LOG_FILE"
    echo "Log file created: $LOG_FILE"
else
    echo "Log file already exists: $LOG_FILE"
fi


# Create backup directory
mkdir -p /tmp/influxdb_backup

# Run InfluxDB backup
influx backup --bucket bucket_rech --token gNqBY_gn_fN4MBbgaLtcvHE7eMT-J2gKyQuMXn9J6Qr3tFjbKyPBbKaznCGQnPJsnZdvLKEbRkVCAf-ZsPq7Rg== /tmp/influxdb_backup

rename 's/:/_/g' /tmp/influxdb_backup/*.csv

# Count number of files in directory
if [ -d "/tmp/influxdb_backup/" ]; then
    # Count the number of files in the directory
    NUM_FILES_tmp=$(ls -l "/tmp/influxdb_backup/" | grep "^-" | wc -l)
     echo "$NUM_FILES_tmp files in temp backup folder"
fi

# Check if USB stick is already mounted
USB_DEVICE="/dev/sda1"
MOUNT_POINT="/media/rech/49748A3276482A1F"
if grep -qs "$USB_DEVICE" /proc/mounts; then
    echo "USB device is already mounted at $MOUNT_POINT"
else
    # Mount the USB device
    echo "Mounting USB device at $MOUNT_POINT"
    mount "$USB_DEVICE" "$MOUNT_POINT"
fi

CURRENT_DATE=$(date +'%d.%m.%Y')
BACKUP_DESTINATION="$MOUNT_POINT/influx_backup/$CURRENT_DATE/"

# Check if directory exists
if [ -d "$BACKUP_DESTINATION" ]; then
    echo "Directory $BACKUP_DESTINATION already exists"
else
    # Create directory if it doesn't exist
    mkdir -p "$BACKUP_DESTINATION"
    echo "Directory $BACKUP_DESTINATION created"
fi


# Copy backup files to USB stick
cp -r /tmp/influxdb_backup/* "$BACKUP_DESTINATION"

# Count number of files in directory
if [ -d "$BACKUP_DESTINATION" ]; then
    # Count the number of files in the directory
    NUM_FILES=$(ls -l "$BACKUP_DESTINATION" | grep "^-" | wc -l)
fi

echo "Backup saved at $BACKUP_DESTINATION, written $NUM_FILES files, $CURRENT_DATE" | tee -a LOG_FILE

