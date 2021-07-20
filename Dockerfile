# Dockerfile
FROM centos:8
LABEL name="NjnuClassroom"
LABEL description="南师教室"
LABEL author="Repigeons"
LABEL repository="github:Repigeons/NjnuClassroom"
VOLUME ["/tmp/NjnuClassroom"]

# Install the base service
RUN dnf install -y epel-release
RUN dnf update  -y
RUN dnf install -y git python39 nginx redis cronie
RUN dnf install -y chromedriver chromium chromium-headless
RUN dnf clean all
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install virtualenv

# Initialize the project directory
RUN mkdir /opt/NjnuClassroom
RUN mkdir /var/log/NjnuClassroom

# Copy project files and deployment
ADD server/manage.py        /opt/NjnuClassroom/src/manage.py
ADD server/app              /opt/NjnuClassroom/src/app
ADD server/orm              /opt/NjnuClassroom/src/orm
ADD server/modules          /opt/NjnuClassroom/src/modules
ADD server/ztxlib           /opt/NjnuClassroom/src/ztxlib
ADD server/resources        /opt/NjnuClassroom/resources
ADD server/requirements.txt /opt/NjnuClassroom/requirements.txt

# Initialize the virtual environment
RUN virtualenv /opt/NjnuClassroom/env
RUN /opt/NjnuClassroom/env/bin/pip install --upgrade pip setuptools wheel
RUN /opt/NjnuClassroom/env/bin/pip install -r /opt/NjnuClassroom/requirements.txt

# Copy shell script and configuration files
ADD server/shell/  /opt/NjnuClassroom/bin/
ADD server/docker/ /

# Set environment variables
ENV env pro

# Expose port 80 (http)
EXPOSE 80

# Startup
WORKDIR /root
RUN chmod 111 init
ENTRYPOINT ["/root/init"]
