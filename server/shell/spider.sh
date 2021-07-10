#!/usr/bin/sh

cd /opt/NjnuClassroom
env/bin/python src/manage.py --run spider

# update data
curl -X POST http://localhost:8001/reset
