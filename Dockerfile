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

RUN python3 -m pip install --upgrade pip setuptools wheel
ADD server/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt --user

# Copy source file and create mounting directories
ADD server/src              /usr/local/src
ADD server/resources        /data/resources
ADD server/static           /data/static
RUN mkdir                   /data/logs


ADD server/shell/notice.sh  /usr/local/sbin/notice
ADD server/shell/spider.sh  /usr/local/sbin/spider
ADD server/shell/server.sh  /usr/local/sbin/server
ADD server/shell/explore.sh /usr/local/sbin/explore

RUN chmod  744              /usr/local/sbin/*

WORKDIR /data
CMD ["/bin/bash"]
