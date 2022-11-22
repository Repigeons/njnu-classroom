init:
	docker --version
	docker-compose --version
	@mkdir -p /opt/njnu_classroom/application
	@git init /opt/njnu_classroom/NjnuClassroom
	@cd /opt/njnu_classroom/NjnuClassroom && git fetch https://github.com/Repigeons/NjnuClassroom.git --depth=1 master && git reset --hard FETCH_HEAD
	@cp /opt/njnu_classroom/NjnuClassroom/backend/spider/src/main/resources/application.yml  /opt/njnu_classroom/application/spider.yml
	@cp /opt/njnu_classroom/NjnuClassroom/backend/core/src/main/resources/application.yml    /opt/njnu_classroom/application/core.yml
	@cp /opt/njnu_classroom/NjnuClassroom/backend/explore/src/main/resources/application.yml /opt/njnu_classroom/application/explore.yml

fetch_develop:
	@git init /opt/njnu_classroom/NjnuClassroom
	@cd /opt/njnu_classroom/NjnuClassroom && git fetch https://github.com/Repigeons/NjnuClassroom.git --depth=1 develop && git reset --hard FETCH_HEAD
	@cp /opt/njnu_classroom/application/spider-dev.yml  /opt/njnu_classroom/NjnuClassroom/backend/spider/src/main/resources/application-dev.yml
	@cp /opt/njnu_classroom/application/core-dev.yml    /opt/njnu_classroom/NjnuClassroom/backend/core/src/main/resources/application-dev.yml
	@cp /opt/njnu_classroom/application/explore-dev.yml /opt/njnu_classroom/NjnuClassroom/backend/explore/src/main/resources/application-dev.yml

fetch_master:
	@git init /opt/njnu_classroom/NjnuClassroom
	@cd /opt/njnu_classroom/NjnuClassroom && git fetch https://github.com/Repigeons/NjnuClassroom.git --depth=1 master && git reset --hard FETCH_HEAD
	@cp /opt/njnu_classroom/application/spider-pro.yml  /opt/njnu_classroom/NjnuClassroom/backend/spider/src/main/resources/application-pro.yml
	@cp /opt/njnu_classroom/application/core-pro.yml    /opt/njnu_classroom/NjnuClassroom/backend/core/src/main/resources/application-pro.yml
	@cp /opt/njnu_classroom/application/explore-pro.yml /opt/njnu_classroom/NjnuClassroom/backend/explore/src/main/resources/application-pro.yml

deploy_develop: fetch_develop
	@cd NjnuClassroom/backend && ./gradlew clean build -p spider -x test
	@cd NjnuClassroom/backend && ./gradlew clean build -p core -x test
	@cd NjnuClassroom/backend && ./gradlew clean build -p explore -x test
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.develop.yaml up -d --build

deploy_spider: fetch_master
	@cd NjnuClassroom/backend && ./gradlew clean build -p spider -x test
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.production.yaml up -d --build spider
deploy_core: fetch_master
	@cd NjnuClassroom/backend && ./gradlew clean build -p core -x test
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.production.yaml up -d --build core
deploy_explore: fetch_master
	@cd NjnuClassroom/backend && ./gradlew clean build -p explore -x test
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.production.yaml up -d --build explore
