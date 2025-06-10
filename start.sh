#!/bin/bash

# Start all scripts in the background
python3 /app/firewallprod.py >> /app/logs/firewall.log 2>&1 &
python3 /app/qmpprod.py >> /app/logs/qmp.log 2>&1 &
# Wait for all background processes to finish
wait

