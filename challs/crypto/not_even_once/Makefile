OUT=dist.zip
IMAGE=registry.vuln.si/challs/crypto/not-even-once:latest

all:

build:

pack:
	zip ${OUT} once.py Dockerfile

docker:
	docker build --platform=linux/amd64 -t ${IMAGE} .
	docker push ${IMAGE}

clean:
