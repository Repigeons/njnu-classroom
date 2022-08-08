FROM fedora:latest

RUN dnf install -y java-latest-openjdk-headless chromedriver
RUN dnf clean all

ADD ../core/target/core-1.0-SNAPSHOT.jar /server.jar
