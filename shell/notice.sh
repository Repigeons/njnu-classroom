#!/usr/bin/sh

# environment variables
export env=pro
export FLASK_ENV=production

# shellcheck disable=SC2039
source env/bin/activate
python /usr/local/src/NjnuClassroom/manage.py --run Notice
