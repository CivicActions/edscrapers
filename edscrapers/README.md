# ED Scrapers Command Line Interface

## Usage

```
$ ed --help
Usage: ed [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  compare    Run a comparison algorhitm against AIR's resources.
  dash       Run the dash server for displaying HTML statistics.
  scrape     Run a Scrapy pipeline for crawling / parsing / dumping output
  stats      Run a statistics algorhitm on the data extracted to provide...
  transform  Run a transformer on a scraper output to generate data in a...
```


## Command help

### Scrape

```
$ ed scrape --help
Usage: ed scrape [OPTIONS] NAME

  Run a Scrapy pipeline for crawling / parsing / dumping output

Options:
  --cache / --no-cache    Do not use Scrapy cache (i.e. "live" scrape)
  --resume / --no-resume  Resume a previously interrupted scrape
  -v, --verbose           Show INFO and DEBUG messages.
  -q, --quiet             Do not show anything.

  -h, --help              Show this message and exit.
```

### Transform

```
$ ed transform --help
Usage: ed transform [OPTIONS] TRANSFORMER

  Run a transformer on a scraper output to generate data in a format useful
  for other applications

Options:
  -i, --input PATH   Input file, if used by requested transformer (e.g.
                     datajson transformer can use a dedup output) If a
                     directory will be provided instead, it will be traversed
                     recursivelly to obtain the list of files.

  -n, --name TEXT    If specified, the transformer will only act on the
                     mentioned output (i.e. a scraper's name)

  -v, --verbose      Show INFO and DEBUG messages.
  -q, --quiet        Do not show anything.

  -h, --help         Show this message and exit.
```

### Compare

```
$ ed compare --help  
Usage: ed compare [OPTIONS]

  Run a comparison algorhitm against AIR's resources.

Options:
  -f, --format [ascii|json]  Format of the output.
  -v, --verbose              Show INFO and DEBUG messages.
  -q, --quiet                Do not show anything.

  -h, --help                 Show this message and exit.
```

### Stats

```
$ ed stats --help  
Usage: ed stats [OPTIONS]

  Run a statistics algorhitm on the data extracted to provide more insights
  about the output. This does not compare against AIR.

Options:
  -n, --name TEXT    Optionally, run the stats just for a specific output
                     pipeline, identified by name (e.g. nces)

  -v, --verbose      Show INFO and DEBUG messages.
  -q, --quiet        Do not show anything.

  -h, --help         Show this message and exit.
```

### Dash

```
$ ed dash --help 
Usage: ed dash [OPTIONS]

  Run the dash server for displaying HTML statistics.

Options:
  -d                  Run the server in a detached process
  --debug             Flag for turning debug mode on
  -p, --port INTEGER  Change the server port (default is 8050)
  -h, --host TEXT     Change the server host (default is 0.0.0.0)
  -v, --verbose       Show INFO and DEBUG messages.
  -q, --quiet         Do not show anything.

  --help              Show this message and exit.
```
