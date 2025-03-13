# Use the official NGINX image as a base
FROM nginx:latest

# Install Python3, cron, and dependencies
RUN apt-get update && apt-get install -y python3 cron curl htop vim && rm -rf /var/lib/apt/lists/*

# Copy files into the container
COPY check_services.py /check_services.py
COPY nginx.conf /etc/nginx/nginx.conf
COPY html /usr/share/nginx/html
COPY conf.d /etc/nginx/conf.d

# Add a cron job to run every 15 seconds
RUN echo "*/1 * * * * python3 /check_services.py" > /etc/cron.d/update-index \
    && echo "*/1 * * * * sleep 15; python3 /check_services.py" >> /etc/cron.d/update-index \
    && echo "*/1 * * * * sleep 30; python3 /check_services.py" >> /etc/cron.d/update-index \
    && echo "*/1 * * * * sleep 45; python3 /check_services.py" >> /etc/cron.d/update-index \
    && echo "" >> /etc/cron.d/update-index \
    && chmod 0644 /etc/cron.d/update-index \
    && crontab /etc/cron.d/update-index

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use the entrypoint script to correctly run cron and NGINX
CMD ["/entrypoint.sh"]
