deploy: package
	docker-compose up -d --build
	docker images | grep '<none>' | awk '{print $$3}' | xargs docker rmi

package:
	mvn clean kotlin:compile package -Dmaven.test.skip=true

core:
	mvn clean kotlin:compile package -Dmaven.test.skip=true -pl core -am

explore:
	mvn clean kotlin:compile package -Dmaven.test.skip=true -pl explore -am
