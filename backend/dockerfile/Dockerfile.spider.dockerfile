FROM njnu-classroom-spider:cache

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

ADD ./spider/build/libs/spider.jar /server.jar
EXPOSE 8080
