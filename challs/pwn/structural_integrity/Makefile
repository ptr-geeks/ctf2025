CC=gcc
CCFLAGS=-Wall -Wextra -pedantic
OUT=dist.zip
IMAGE=registry.vuln.si/challs/pwn/structural-integrity:latest

all: build

build: main
	${CC} ${CCFLAGS} -o app main.c

pack:
	zip ${OUT} app Dockerfile

docker:
	docker build --platform=linux/amd64 -t ${IMAGE} .
	docker push ${IMAGE}

clean:
	rm -f ${OUT} app
