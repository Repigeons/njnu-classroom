FROM openjdk:spider

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

ADD ./spider/build/libs/spider-1.0-SNAPSHOT.jar /server.jar
EXPOSE 8080
