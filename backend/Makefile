init:
	docker --version
	docker-compose --version
	@rm -rf /opt/njnu_classroom/NjnuClassroom
	@mkdir -p /opt/njnu_classroom/application
	@cd /opt/njnu_classroom && git clone --single-branch --depth=1 https://github.com/Repigeons/NjnuClassroom.git
	@cp /opt/njnu_classroom/NjnuClassroom/backend/spider/src/main/resources/application.yml 	/opt/njnu_classroom/application/spider.yml
	@cp /opt/njnu_classroom/NjnuClassroom/backend/core/src/main/resources/application.yml 		/opt/njnu_classroom/application/core.yml
	@cp /opt/njnu_classroom/NjnuClassroom/backend/explore/src/main/resources/application.yml 	/opt/njnu_classroom/application/explore.yml
	@rm -rf /opt/njnu_classroom/NjnuClassroom

clone_develop:
	@rm -rf /opt/njnu_classroom/NjnuClassroom
	@cd /opt/njnu_classroom && git clone --single-branch --depth=1 https://github.com/Repigeons/NjnuClassroom.git -b develop
	@cp /opt/njnu_classroom/application/spider-dev.yml	/opt/njnu_classroom/NjnuClassroom/backend/spider/src/main/resources/application-dev.yml
	@cp /opt/njnu_classroom/application/core-dev.yml 	/opt/njnu_classroom/NjnuClassroom/backend/core/src/main/resources/application-dev.yml
	@cp /opt/njnu_classroom/application/explore-dev.yml /opt/njnu_classroom/NjnuClassroom/backend/explore/src/main/resources/application-dev.yml

clone_master:
	@rm -rf /opt/njnu_classroom/NjnuClassroom
	@cd /opt/njnu_classroom && git clone --single-branch --depth=1 https://github.com/Repigeons/NjnuClassroom.git -b master
	@cp /opt/njnu_classroom/application/spider-pro.yml	/opt/njnu_classroom/NjnuClassroom/backend/spider/src/main/resources/application-pro.yml
	@cp /opt/njnu_classroom/application/core-pro.yml 	/opt/njnu_classroom/NjnuClassroom/backend/core/src/main/resources/application-pro.yml
	@cp /opt/njnu_classroom/application/explore-pro.yml /opt/njnu_classroom/NjnuClassroom/backend/explore/src/main/resources/application-pro.yml

compile_develop: clone_develop
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.build.yaml run --rm compile-spider
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.build.yaml run --rm compile-core
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.build.yaml run --rm compile-explore

compile_spider: clone_master
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.build.yaml run --rm compile_spider
compile_core: clone_master
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.build.yaml run --rm compile_core
compile_explore: clone_master
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.build.yaml run --rm compile_explore

deploy_develop: compile_develop
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.develop.yaml up -d --build --remove-orphans
	@rm -rf /opt/njnu_classroom/NjnuClassroom

deploy_spider: compile_spider
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.production.yaml up -d --build --remove-orphans spider
	@rm -rf /opt/njnu_classroom/NjnuClassroom
deploy_core: compile_core
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.production.yaml up -d --build --remove-orphans core
	@rm -rf /opt/njnu_classroom/NjnuClassroom
deploy_explore: compile_explore
	@docker-compose -f /opt/njnu_classroom/NjnuClassroom/backend/dockerfile/docker-compose.production.yaml up -d --build --remove-orphans explore
	@rm -rf /opt/njnu_classroom/NjnuClassroom
