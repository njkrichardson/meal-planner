.PHONY: docker-build, docker-run, clean

IMAGE_TAG:=meal_planner

docker-build: 
	docker build --tag ${IMAGE_TAG}:latest . 

docker-run: 
	docker run -dt -v "$(shell pwd):/meal_planner" --name ${IMAGE_TAG} ${IMAGE_TAG}:latest /bin/bash

clean: 
	docker stop ${IMAGE_TAG} && docker rm ${IMAGE_TAG}
