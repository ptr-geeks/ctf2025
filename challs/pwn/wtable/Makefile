CXX=clang++
CXXFLAGS=-std=c++20 -Wall -Wextra
LDFLAGS=-Wl,-z,relro,-z,now

all: build

build:
	$(CXX) $(CXXFLAGS) ${LDFLAGS} -o app main.cpp
