#!make
include .env
export $(shell sed 's/=.*//' .env)

test:
	python3 -m tox