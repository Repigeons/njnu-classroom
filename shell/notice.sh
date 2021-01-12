#!/usr/bin/sh

# environment variables
export env=pro
export FLASK_ENV=production

source env/bin/activate
python /usr/local/src/NjnuClassroom/manage.py --run Notice --log /var/log/NjnuClassroom/notice.log
