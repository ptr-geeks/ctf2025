OUT=dist.zip
IMAGE=registry.vuln.si/challs/misc/login:latest

all:

pack:
	zip ${OUT} login.py Dockerfile

docker:
	docker build --platform=linux/amd64 -t ${IMAGE} .
	docker push ${IMAGE}

clean:
	rm -f ${OUT}
