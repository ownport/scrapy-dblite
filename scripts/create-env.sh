#!/bin/sh

echo 'Creating user: dev ...'
adduser --disabled-password --gecos '' --uid 1000 dev 
adduser dev sudo
echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
chown -R dev:dev /data/scrapy-dblite
exec su - dev

