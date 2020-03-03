.PHONY: all install list scrape compare

all: list

install:
	python setup.py install

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

scrape:
	python -m edscrapers.scrapers.base.cli $(filter-out $@,$(MAKECMDGOALS))

compare:
	python -m tools.compare $(filter-out $@,$(MAKECMDGOALS))

%:
	@:
