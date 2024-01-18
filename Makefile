#!make
include .env
export $(shell sed 's/=.*//' .env)

test:
	python3 -m tox

build:
	python3 setup.py sdist

publish:
	twine upload dist/*