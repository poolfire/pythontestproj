#!/bin/bash
sudo -S apt-get install -y nginx
sudo wget -O  /etc/nginx/sites-available/default https://raw.githubusercontent.com/poolfire/pythontestproj/master/nginx.conf
sudo systemctl restart nginx
sudo mkdir -p /home/files
sudo wget -O /home/files/index.png https://github.com/poolfire/pythontestproj/raw/master/static/index.png
sudo wget -O /home/files/index.html https://raw.githubusercontent.com/poolfire/pythontestproj/master/static/index.html