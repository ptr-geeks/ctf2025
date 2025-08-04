OUT=dist.zip
IMAGE=registry.vuln.si/challs/rev/cs:latest

all: build

build:
	go build -o server server.go

pack:
	zip ${OUT} server Dockerfile

docker:
	docker build --platform=linux/amd64 -t ${IMAGE} .
	docker push ${IMAGE}

clean:
	rm -f ${OUT} server
