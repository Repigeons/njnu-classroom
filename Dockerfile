# Dockerfile
FROM centos:latest
MAINTAINER Repigeons
VOLUME ["/tmp/NjnuClassroom"]

# Install the base service
RUN yum install -y python3 firefox redis nginx
RUN pip3 install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip3 install virtualenv

# Initialize the project directory
RUN mkdir /usr/local/src/NjnuClassroom
RUN mkdir /opt/NjnuClassroom
RUN mkdir /etc/NjnuClassroom
RUN mkdir /var/log/NjnuClassroom

# Copy project files and deployment
ADD python/App /usr/local/src/NjnuClassroom/App
ADD python/utils /usr/local/src/NjnuClassroom/utils
ADD python/manage.py /usr/local/src/NjnuClassroom/manage.py
ADD python/requirements.txt /usr/local/src/NjnuClassroom/requirements.txt

# Initialize the runtime environment
WORKDIR /opt/NjnuClassroom
RUN virtualenv env
RUN env/bin/python -m pip install --upgrade pip setuptools wheel
RUN env/bin/python -m pip install -r /usr/local/src/NjnuClassroom/requirements.txt

# Copy shell script and system config files
ADD shell/ /opt/NjnuClassroom/
ADD systemd/ /lib/systemd/system/
ADD docker/ /

# Set environment variables
ENV env pro
ENV FLASK_ENV production

# Expose port 80: http
EXPOSE 80

# startup
WORKDIR /root
RUN chmod 111 init
ENTRYPOINT ["/root/init"]
