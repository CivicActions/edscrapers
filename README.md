# U.S. Department of Education scraping kit

> NOTE: More specific documentation is available "on the spot", in the module 
> directories (e.g. `edscrapers/scrapers` or `edscrapers/transformers`).

## Running the tool

You need the `ED_OUTPUT_PATH` environment variable to be set before running. Not
having the variable set in your environment will result in a fatal error.

If GNU Make is available in your environment, you can run the command
`make install`. Alternatively, run `python setup.py install`.

After installing, run the `eds` command in a command line prompt to get more 
info on the usage, or read the [docs](./edscrapers/README.md).

## Terminology

- **Scraping Source**: a website (or section of website) where you scrape 
  information from
- **Scraper**: A script that collects structured data from (rather 
  unstructured) web pages
    - **Crawler**: A script that follows links and identifies all the pages 
      containing information to be parsed
    - **Parser**: A script that identifies data in HTML and loads it into a 
      machine readable data structure
- **Transformer**: a script that takes a data structure and adapts it to a 
  target structure
- **ETL**: Extract + Transform + Load process for metadata.
- **Data.json**: A specific JSON format used by CKAN harvesters. 
  [Example](https://www2.ed.gov/data.json)


# Scrapers

Scrapers are Scrapy powered scripts that crawl through links and parse HTML 
pages. The proposed structure is:

- A crawler class that defines rules for link extraction and page filters
  * This will be instantiated by a `CrawlerProcess` in the main `scraper.py` script
- A parser script that is essentially a callback for fetching HTML pages. It 
  receives a [Scrapy Response](https://docs.scrapy.org/en/latest/topics/request-response.html#scrapy.http.Response) 
  payload, which can be parsed using any HTML parsing methods
  - An optional Model class, to define the properties of extracted datasets and 
    make them more flexible for dumping or automating operations if needed


# Transformers

Transformers are independent scripts that take a input and return it filtered 
and/or restructured. They are meant to complement the work done by scrapers by 
taking their output and making it usable for various applications (e.g. the CKAN 
harvester).

We currently have two transformers in place: one that deduplicates scraping 
output and one that makes it into data.json files for being ingested by 
`ckanext-harvest`.



# License

[GNU AFFERO GENERAL PUBLIC LICENSE](LICENSE.md)
