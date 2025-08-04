OUT=dist.zip
IMAGE=registry.vuln.si/challs/crypto/poc:latest

all:

build:

pack:
	zip ${OUT} poc.py Dockerfile

docker:
	docker build --platform=linux/amd64 -t ${IMAGE} .
	docker push ${IMAGE}

clean:

