FROM fedora:latest

RUN dnf install -y java-latest-openjdk-headless
RUN dnf clean all

ADD ../explore/target/explore-1.0-SNAPSHOT.jar /server.jar
