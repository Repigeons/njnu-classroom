# Dockerfile
FROM centos:8
LABEL name="NjnuClassroom"
LABEL description="南师教室"
LABEL author="Repigeons"
LABEL repository="github:Repigeons/NjnuClassroom"
VOLUME ["/data"]

# Install python and chromium for selenium
RUN dnf install -y epel-release python39
RUN dnf install -y chromedriver chromium chromium-headless
RUN dnf clean all

ADD server/requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -U pip setuptools wheel
RUN python3 -m pip install -r /tmp/requirements.txt

# Append shell file
ADD server/shell/notice.sh  /usr/local/sbin/notice
ADD server/shell/spider.sh  /usr/local/sbin/spider
ADD server/shell/server.sh  /usr/local/sbin/server
ADD server/shell/explore.sh /usr/local/sbin/explore
ADD server/shell/mail.sh    /usr/local/sbin/mail
RUN chmod 744               /usr/local/sbin/*

# Copy source file and create mounting directories
ADD server/src              /usr/local/src
ADD server/resources        /data/resources
ADD server/static           /data/static

WORKDIR /data
CMD ["/bin/bash"]
