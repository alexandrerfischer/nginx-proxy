#!/bin/bash

# Inicia o cron em foreground para que continue rodando
cron -f &

# Executa o script uma vez no início para evitar esperar o cron rodar
python3 /check_services.py

# Mantém o NGINX rodando no foreground
nginx -g 'daemon off;'
