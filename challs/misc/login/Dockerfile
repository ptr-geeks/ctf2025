FROM ubuntu:24.04

EXPOSE 1337

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y update && \
    apt-get -y install python3

WORKDIR /app

ENV FLAG=ptr{demo_flag}
COPY login.py /app

CMD stdbuf -i0 -o0 -e0 python3 login.py
