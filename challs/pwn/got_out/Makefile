CC=gcc
CCFLAGS=
OUT=dist.zip
IMAGE=registry.vuln.si/challs/pwn/got-out:latest

all: build

build:
	${CC} ${CCFLAGS} -o app main.c

pack:
	zip ${OUT} app Dockerfile

docker:
	docker build --platform=linux/amd64 -t ${IMAGE} .
	docker push ${IMAGE}

clean:
	rm -f ${OUT} app
