# U.S. Department of Education scraping kit

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

TBD


# License

[GNU AFFERO GENERAL PUBLIC LICENSE](LICENSE.md)
