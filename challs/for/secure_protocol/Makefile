OUT=dist.zip
IMAGE=registry.vuln.si/challs/forensics/secure-protocol:latest

all:

build:

pack:
	zip ${OUT} challenge.pcap

docker:
	docker build --platform=linux/amd64 -t ${IMAGE} .
	docker push ${IMAGE}

clean:
	rm -f ${OUT}
