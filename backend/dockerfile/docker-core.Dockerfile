FROM fedora:latest

RUN dnf install -y java-latest-openjdk-headless
RUN dnf install -y chromedriver chromium chromium-headless
RUN dnf clean all

ADD ../core/target/core-1.0-SNAPSHOT.jar /server.jar
