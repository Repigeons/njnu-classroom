#!/usr/bin/sh

# environment variables
export env=pro

# shellcheck disable=SC2039
source env/bin/activate
python /usr/local/src/NjnuClassroom/manage.py --run Spider --config /etc/NjnuClassroom

# post a request to server for latest data
curl -X POST http://localhost:8000/reset
