#!/usr/bin/sh

cd /opt/NjnuClassroom
env/bin/python src/manage.py --run Explore --log /var/log/NjnuClassroom/server.log
