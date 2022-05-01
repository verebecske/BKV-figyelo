#!/bin/bash
echo "Start cert generator"
mkdir traefik/certs
cd traefik/certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout cert.key -out cert.crt
chmod 644 cert.crt
chmod 600 cert.key
