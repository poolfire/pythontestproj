#!/bin/bash
sudo -S apt update
sudo apt install -y postgresql postgresql-contrib;
sudo -u postgres createuser -s -e db_user
echo "Changing password"
sudo -u postgres psql postgres -c "ALTER USER db_user WITH ENCRYPTED PASSWORD 'DB_password'"
echo "Creating DB"
sudo -u postgres createdb DB db_user


