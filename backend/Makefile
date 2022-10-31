init:
	docker --version
	docker-compose --version
	@rm -rf /opt/njnu_classroom/NjnuClassroom
	@mkdir -p /opt/njnu_classroom/application
	@cd /opt/njnu_classroom && git clone --single-branch --depth=1 https://gitee/Repigeons/NjnuClassroom.git #gitee同步镜像
	@cp /opt/njnu_classroom/NjnuClassroom/backend/spider/src/main/resources/application.yml 	/opt/njnu_classroom/application/spider.yml
	@cp /opt/njnu_classroom/NjnuClassroom/backend/core/src/main/resources/application.yml 		/opt/njnu_classroom/application/core.yml
	@cp /opt/njnu_classroom/NjnuClassroom/backend/explore/src/main/resources/application.yml 	/opt/njnu_classroom/application/explore.yml
	@rm -rf /opt/njnu_classroom/NjnuClassroom

clone_develop:
	@rm -rf /opt/njnu_classroom/NjnuClassroom
	@cd /opt/njnu_classroom && git clone --single-branch --depth=1 https://gitee/Repigeons/NjnuClassroom.git -b develop #gitee同步镜像
	@cp /opt/njnu_classroom/application/spider-dev.yml	/opt/njnu_classroom/NjnuClassroom/backend/spider/src/main/resources/application-dev.yml
	@cp /opt/njnu_classroom/application/core-dev.yml 	/opt/njnu_classroom/NjnuClassroom/backend/core/src/main/resources/application-dev.yml
	@cp /opt/njnu_classroom/application/explore-dev.yml /opt/njnu_classroom/NjnuClassroom/backend/explore/src/main/resources/application-dev.yml

clone_master:
	@rm -rf /opt/njnu_classroom/NjnuClassroom
	@cd /opt/njnu_classroom && git clone --single-branch --depth=1 https://gitee/Repigeons/NjnuClassroom.git -b master #gitee同步镜像
	@cp /opt/njnu_classroom/application/spider-pro.yml	/opt/njnu_classroom/NjnuClassroom/backend/spider/src/main/resources/application-pro.yml
	@cp /opt/njnu_classroom/application/core-pro.yml 	/opt/njnu_classroom/NjnuClassroom/backend/core/src/main/resources/application-pro.yml
	@cp /opt/njnu_classroom/application/explore-pro.yml /opt/njnu_classroom/NjnuClassroom/backend/explore/src/main/resources/application-pro.yml

deploy_develop: clone_develop
	@cd NjnuClassroom/backend && ./gradlew clean build -p spider -x test --parallel
	@cd NjnuClassroom/backend && ./gradlew clean build -p core -x test --parallel
	@cd NjnuClassroom/backend && ./gradlew clean build -p explore -x test --parallel
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.develop.yaml up -d --build
	@rm -rf /opt/njnu_classroom/NjnuClassroom

deploy_spider: clone_master
	@cd NjnuClassroom/backend && ./gradlew clean build -p spider -x test --parallel
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.production.yaml up -d --build spider
	@rm -rf /opt/njnu_classroom/NjnuClassroom
deploy_core: clone_master
	@cd NjnuClassroom/backend && ./gradlew clean build -p core -x test --parallel
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.production.yaml up -d --build core
	@rm -rf /opt/njnu_classroom/NjnuClassroom
deploy_explore: clone_master
	@cd NjnuClassroom/backend && ./gradlew clean build -p explore -x test --parallel
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.production.yaml up -d --build explore
	@rm -rf /opt/njnu_classroom/NjnuClassroom
