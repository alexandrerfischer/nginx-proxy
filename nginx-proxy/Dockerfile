# Usa a imagem oficial do NGINX como base
FROM nginx:latest

# Instala Python3, cron e dependências
RUN apt-get update && apt-get install -y python3 cron curl htop vim && rm -rf /var/lib/apt/lists/*

# Copia os arquivos para o container
COPY check_services.py /check_services.py
COPY nginx.conf /etc/nginx/nginx.conf
COPY html /usr/share/nginx/html
COPY conf.d /etc/nginx/conf.d

# Adiciona um cron job para rodar a cada 15 segundos
RUN echo "*/1 * * * * python3 /check_services.py" > /etc/cron.d/update-index \
    && echo "*/1 * * * * sleep 15; python3 /check_services.py" >> /etc/cron.d/update-index \
    && echo "*/1 * * * * sleep 30; python3 /check_services.py" >> /etc/cron.d/update-index \
    && echo "*/1 * * * * sleep 45; python3 /check_services.py" >> /etc/cron.d/update-index \
    && echo "" >> /etc/cron.d/update-index \
    && chmod 0644 /etc/cron.d/update-index \
    && crontab /etc/cron.d/update-index

# Copia o script de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Usa o script de entrada para rodar cron e NGINX corretamente
CMD ["/entrypoint.sh"]
