CC=gcc
CCFLAGS=-fno-stack-protector -no-pie
OUT=dist.zip
IMAGE=registry.vuln.si/challs/pwn/return2sender:latest

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
