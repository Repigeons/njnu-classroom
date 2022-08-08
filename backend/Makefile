push: build
	@docker-compose -f dockerfile/docker-compose.build.yaml push

build: compile
	@docker-compose -f dockerfile/docker-compose.build.yaml build
	@docker images | grep '<none>' | awk '{print $$3}' | xargs docker rmi

compile: .pull
	@docker-compose -f dockerfile/docker-compose.build.yaml run compile

.pull:
	@git reset --hard && git pull --prune
