OUT=dist.zip
IMAGE=registry.vuln.si/challs/crypto/rfc:latest

all:

build:

pack:
	zip ${OUT} rfc.py Dockerfile

docker:
	docker build --platform=linux/amd64 -t ${IMAGE} .
	docker push ${IMAGE}

clean:
