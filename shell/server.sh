#!/usr/bin/sh

# environment variables
export env=pro
export FLASK_ENV=production
export SPIDER_SHELL="/opt/NjnuClassroom/spider.sh"
export RESET_CMD="curl -X POST http://localhost:8000/reset"

# shellcheck disable=SC2039
source env/bin/activate
python /usr/local/src/NjnuClassroom/manage.py --run Server --config /etc/NjnuClassroom
