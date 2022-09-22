master:
	@git checkout master && git pull --prune

build: compile
	@docker-compose -f dockerfile/docker-compose.build.yaml build
	@-docker images | grep '<none>' | awk '{print $$3}' | xargs -r docker rmi

compile: master
	@rm .pull
	@docker-compose -f dockerfile/docker-compose.build.yaml run --rm compile
