SHELL:=/bin/bash
MAKE:=make
CHALLS:=$(wildcard challs/for/* challs/rev/* challs/crypto/* challs/pwn/* challs/web/pass)

all: pack docker push

pack:
	for chall in $(CHALLS); do \
		echo "> Packing $$chall"; \
		$(MAKE) -C "$$chall" pack; \
	done

docker:
	for chall in $(CHALLS); do \
		echo "> Building Docker image for $$chall"; \
		$(MAKE) -C "$$chall" docker; \
	done

push:
	source .env && python3 scripts/ctfd.py \
		--url "$$CTFD_URL" \
		--token "$$CTFD_TOKEN" \
		--config challs.yml

clean:
	for chall in $(CHALLS); do \
		$(MAKE) -C ${chall} clean; \
	done
