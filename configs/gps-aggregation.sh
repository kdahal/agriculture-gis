#!/bin/sh
# Run on each drone to relay GPS data over mesh

while true; do
  GPS_DATA=$(gpspipe -n -r | head -1)  # Assuming gpsd/gpspipe installed
  echo "$GPS_DATA" | nc -u 192.168.1.100 12345  # Send to ground station UDP
  sleep 1  # 1Hz update rate
done