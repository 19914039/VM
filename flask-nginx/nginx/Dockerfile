FROM ubuntu:20.04

RUN apt-get update && apt-get install -y nginx

COPY ./default /etc/nginx/sites-available/default
COPY cert.pem key.pem /home/certificates/

EXPOSE 443

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
