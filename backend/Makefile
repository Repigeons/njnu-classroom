package:
	mvn clean kotlin:compile package

deploy: package
	docker-compose up -d --build
	docker images | grep '<none>' | awk '{print $3}' | xargs docker rmi
