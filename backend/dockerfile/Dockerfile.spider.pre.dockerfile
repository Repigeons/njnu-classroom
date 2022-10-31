# docker build -t openjdk:spider .
FROM openjdk:18-slim

RUN sed -i "s@http://deb.debian.org@https://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list
RUN sed -i "s@http://ftp.debian.org@https://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list
RUN sed -i "s@http://security.debian.org@https://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list

RUN apt-get update
RUN apt-get -y install chromium chromium-driver
RUN apt-get clean all
