FROM openjdk:18

ADD core/target/core-1.0-SNAPSHOT.jar /server.jar

EXPOSE 8080
CMD ["java", "-jar", "/server.jar", "--spring.profiles.active=pro"]
