CC=clang
CCFLAGS=-std=c11
OUT=dist.zip
IMAGE=registry.vuln.si/challs/rev/proto:latest

all: build

build:
	$(CC) $(CCFLAGS) -o app main.c

pack:
	zip ${OUT} app Dockerfile

docker:
	docker build --platform=linux/amd64 -t ${IMAGE} .
	docker push ${IMAGE}

clean:
	rm -f ${OUT} app
