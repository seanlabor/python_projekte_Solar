sudo docker run --restart always  --user "$(id -u)" -p 3000:3000 --restart always -d --volume "$PWD/grafana/data:/var/lib/grafana" grafana/grafana:latest


raspberry 
ip: 192.168.0.5 
Benutzer: rech
PW: pi

Ip used in InfluxDBCall.py 

1.1	Cronjobs
* * * * * /home/rech/sunrise_sunset_docker.sh
Every minute check sunrise_sunset_docker.sh in home/rech/sunrise_sunset.sh to start or stop docker container with the sun

0 0 * * 0 /home/rech/backup_influxdb.sh
Every Sunday at midnight, a backup of influxdb is written to the usb stick

Copy Files to Raspberry via SSH
scp C:\Users\Flo\Documents\Projekte\Solarserver\python_projekte_Solar\backup_influxdb.sh rech@192.168.0.5:/home/rech/

1.1.1	GMAIL
gmail app password
name Solarbackup
app password: kbew qziw swnq gsmc 

Send email with mutt
echo "This is the body of the email" | mutt -s "Subject of the email" -a hello_world.txt  -- florech@mail.de

Docker restart policies for both sungattherers:

docker update --restart=unless-stopped e7036c943273


Raspberry image

https://github.com/seamusdemora/RonR-RPi-image-utils

sudo image-backup
image name: /media/rech/49748A3276482A1F/raspberry_image/20240512_Pi4B_imagebackup.img
Attention - usb stick must be ntfs for files larger 8gb

portainer
https://192.168.0.5:9443
Login: rech
PW: Sonnengold875


TODO
Check if time written to influx is correct

Sh scripts give permissions
chmod +x backup_influxdb.sh

