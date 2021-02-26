#!/bin/bash
sudo -S apt update
sudo apt install -y python3-pip
sudo python3 -m pip install flask
sudo wget -O /home/app.py https://raw.githubusercontent.com/poolfire/pythontestproj/master/app.py
sudo wget -0 /etc/systemd/system/flaskapp.service https://raw.githubusercontent.com/poolfire/pythontestproj/master/flaskapp.service
sudo systemctl daemon-reload
sudo systemctl enable flaskapp
sudo systemctl start flaskapp