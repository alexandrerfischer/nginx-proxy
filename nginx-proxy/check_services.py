import re
import json
import glob
import subprocess

NGINX_CONF_PATH = "/etc/nginx/nginx.conf"
OUTPUT_JSON_PATH = "/usr/share/nginx/html/services.json"

# HTTP status code mapping
HTTP_STATUS_MESSAGES = {
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
}

# Fixed regex pattern to correctly capture multiple services
pattern = re.compile(r"location\s+/([\w-]+)/\s*\{[^}]*?proxy_pass\s+(http://[\w\.-]+)", re.DOTALL)

def get_services():
    """ Reads NGINX configuration files and returns the configured services. """
    services = []
    conf_files = [NGINX_CONF_PATH] + glob.glob("/etc/nginx/conf.d/*.conf") + glob.glob("/etc/nginx/sites-enabled/*")

    for conf_file in conf_files:
        with open(conf_file, "r") as f:
            content = f.read()  # Read the entire file
            matches = pattern.findall(content)  # Find all matches

            for name, url in matches:
                services.append((name, url))  # Add all found services

    return services

def check_service(url):
    """ Tests the service using curl and returns the HTTP status code and message. """
    if url.endswith("/"):
        url = url[:-1]  # Remove the trailing slash

    try:
        result = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
                                capture_output=True, text=True, timeout=5)
        status_code = int(result.stdout.strip())
        status_message = HTTP_STATUS_MESSAGES.get(status_code, "Unknown Error")
        return status_code, status_message
    except Exception:
        return 0, "Connection Error"

def update_services():
    """ Updates the JSON file with all services and their statuses. """
    services = get_services()
    service_status = []

    for name, url in services:
        status_code, status_message = check_service(url)
        service_status.append({
            "name": name,
            "url": f"/{name}/",
            "status": f"{status_code} - {status_message}"
        })

    with open(OUTPUT_JSON_PATH, "w") as f:
        json.dump(service_status, f, indent=4)

    print(f"Update completed! {len(service_status)} services checked.")

if __name__ == "__main__":
    update_services()
