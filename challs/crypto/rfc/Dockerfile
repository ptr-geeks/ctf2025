FROM ubuntu:24.04

EXPOSE 1337

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y update && \
    apt-get -y install socat coreutils python3

WORKDIR /app

COPY flag.txt /app
COPY rfc.py /app

CMD socat -T 10 \
    TCP-LISTEN:1337,nodelay,reuseaddr,fork \
    EXEC:"stdbuf -i0 -o0 -e0 python3 rfc.py"
