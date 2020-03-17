.PHONY: all install list scrape compare transform

all: list

install:
	python setup.py install

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

scrape:
	ed scrape $(filter-out $@,$(MAKECMDGOALS))

compare:
	ed compare $(filter-out $@,$(MAKECMDGOALS))

transform:
	ed transform $(filter-out $@,$(MAKECMDGOALS))

%:
	@:
