FROM openjdk:18-slim

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

ADD ./explore/target/explore-1.0-SNAPSHOT.jar /server.jar
EXPOSE 8080
