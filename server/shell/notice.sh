#!/usr/bin/sh

cd /opt/NjnuClassroom
env/bin/python src/manage.py --run Notice --log /var/log/NjnuClassroom/notice.log
