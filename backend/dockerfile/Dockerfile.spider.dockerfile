FROM openjdk:18-slim

RUN apt-get update
RUN apt-get -y install chromium chromium-driver
RUN apt-get clean all

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

ADD ./spider/target/spider-1.0-SNAPSHOT.jar /server.jar
EXPOSE 8080
