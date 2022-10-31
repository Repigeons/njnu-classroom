FROM openjdk:18-slim

RUN sed -i "s@http://deb.debian.org@https://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list \
 && sed -i "s@http://ftp.debian.org@https://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list \
 && sed -i "s@http://security.debian.org@https://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list \
 && apt-get update \
 && apt-get -y install chromium chromium-driver \
 && apt-get clean all

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

ADD ./spider/build/libs/spider-1.0-SNAPSHOT.jar /server.jar
EXPOSE 8080
