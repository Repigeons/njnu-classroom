package: .pull
	@mvn clean kotlin:compile package -Dmaven.test.skip=true

core: .pull
	@mvn clean kotlin:compile package -Dmaven.test.skip=true -pl core -am

explore: .pull
	@mvn clean kotlin:compile package -Dmaven.test.skip=true -pl explore -am

deploy: package
	@docker-compose up -d --build
	@docker images | grep '<none>' | awk '{print $$3}' | xargs docker rmi

clean:
	@mvn clean

.pull:
	@git pull
