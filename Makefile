.PHONY: all install list scrape

all: list

install:
	python setup.py install

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

scrape:
	python -m edscrapers.scrapers.base.cli $(filter-out $@,$(MAKECMDGOALS))

%:
	@:
