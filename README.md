Please install requirements

Quickstart:
python3 main.py

You should configure IP addresses and credentials into the main.py file

Also, you are able to turnoff the logger, which makes records to debug.log file

This application is based on ssh tunneling. Means that we connect to each server,
download already configured bash script and run it.


In the end you'll get working app server

appserver_ip:5000(ex. **127.0.0.1:5000**)

postgress db:

user - **db_user**,
password - **DB_password**,
database - **DB**

and nginx configured to serve static files
ex. nginx_ip:8080/index.html or nginx_ip:8080/index.png

Also, it's configured as a load balancer with only one
enabled server.

You can run app this way nginx_ip/app
