FROM php:8.3-apache

RUN sed -i 's/Listen 80/Listen 8000/' /etc/apache2/ports.conf

COPY php/* /var/www/html/
