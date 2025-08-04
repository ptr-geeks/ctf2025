CXX=clang++
CXXFLAGS=-std=c++20 -Wall -Wextra
LDFLAGS=-Wl,-z,relro,-z,now
OUT=dist.zip
IMAGE=registry.vuln.si/challs/pwn/wtable:latest

all: build

build:
	$(CXX) $(CXXFLAGS) ${LDFLAGS} -o app main.cpp

pack:
	zip ${OUT} main.cpp app Dockerfile

docker:
	docker build --platform=linux/amd64 -t ${IMAGE} .
	docker push ${IMAGE}

clean:
	rm -f ${OUT} app
