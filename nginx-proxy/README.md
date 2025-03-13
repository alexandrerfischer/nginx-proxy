# Nginx Reverse Proxy with Service Monitoring

This project sets up an Nginx reverse proxy running in a Docker container, automatically detecting and monitoring backend services. It includes a cron job that periodically checks the status of services and updates a JSON file, which can be used for a dynamic service dashboard.

## Features

- **Reverse Proxy**: Routes traffic to multiple backend services.
- **Service Monitoring**: Checks service availability using `curl`.
- **Auto-Update JSON**: Periodically updates `services.json` with active services.
- **Cron Job Execution**: Runs scheduled checks every 15 seconds.

## Requirements

- Docker
- Docker Compose (optional)

## Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/your-repo/nginx-reverse-proxy.git
   cd nginx-reverse-proxy
   ```

2. **Build and Run the Container**
   ```sh
   docker build -t nginx-proxy .
   docker run -d -p 80:80 --name nginx-proxy nginx-proxy
   ```

3. **(Optional) Run with Docker Compose**
   ```sh
   docker-compose up -d
   ```

## Configuration

- **Nginx Configuration**: Modify `nginx.conf` and place custom configurations in `conf.d/`.
- **Service Monitoring Script**: The `check_services.py` script scans `nginx.conf` and connected configuration files to check for running services.
- **Cron Job**: Runs `check_services.py` every 15 seconds to update `services.json`.

## Files Overview

- `Dockerfile` – Builds the Nginx proxy container with Python and cron.
- `nginx.conf` – Main Nginx configuration file.
- `conf.d/` – Additional Nginx configuration files.
- `check_services.py` – Script that checks service availability.
- `entrypoint.sh` – Script that starts cron and Nginx.

## Logs & Debugging

Check the logs to ensure everything is running correctly:
```sh
docker logs nginx-proxy
```

Manually run the monitoring script:
```sh
docker exec nginx-proxy python3 /check_services.py
```

Check if cron jobs are running inside the container:
```sh
docker exec -it nginx-proxy crontab -l
```

## Contributing

Feel free to fork this project, submit pull requests, or report issues!
