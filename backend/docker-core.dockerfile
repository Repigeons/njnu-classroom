FROM openjdk:18

ADD core/target/core-1.0-SNAPSHOT.jar /server.jar
ADD core/src/main/resources/chromedriver /usr/bin/chromedriver