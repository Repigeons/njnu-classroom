package:
	mvn clean kotlin:compile package

deploy: package
	docker-compose up -d --build
