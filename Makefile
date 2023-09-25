#!make
include .env
export $(shell sed 's/=.*//' .env)

anvil:
	anvil --fork-url $(FORK_RPC_URL) --fork-block-number 119280500

test:
	python3 -m tox