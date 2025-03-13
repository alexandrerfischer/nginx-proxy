#!/bin/bash

# Start cron in the foreground so it keeps running
cron -f &

# Run the script once at startup to avoid waiting for cron to trigger
python3 /check_services.py

# Keep NGINX running in the foreground
nginx -g 'daemon off;'
