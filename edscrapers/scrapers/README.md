# Scrapers for U.S. Department of Education

## Objectives

The modules in this directory have the unique purpose of exploring various web 
targets and collecting unstructured information as structured, macine readable 
data.

Each specific target is operated by a scraper subpackage. In our case, the acronym of the office or the name of the site dictates the package name.

A scraper package usually has the following structure:

* a crawler
  * determine the rules for navigating the web (which sites, links etc.)
  * calls a parser function on every successfully accessed page
* a parser
  * called while crawling
  * identifies information in page
  * populates models with data

The scrapers inherit from a `base` scraper package, that contains:

* a set of helper functions
* models for Resource and Dataset
* a pipeline that:
  * logs the activity
  * saves the returned models to JSON
* custom middlewares for the Scrapy process

## Crawling

Crawler classes are essentially [Scrapy 
spiders](https://docs.scrapy.org/en/latest/topics/spiders.html).
They have a unique `name` property that identifies them **and** 
directs the output to a specific folder. The `name` should be the same as the target/package in which the crawler is contained

Every crawler class needs an `allowed_regex` property that determines which 
URLs are acceptable to parse in the navigation process.

All the accepted parameters and their documentation can be found in the [Scrapy 
Docs related to Spiders](https://docs.scrapy.org/en/latest/topics/spiders.html).

## Parsing

Parser callback invoked by the crawlers is a function that takes the result object and parses the HTML inside.

Depending on the complexity of the page(s) parsed, there could be more parsers 
and a main function (parser task master) that switches between them based on HTML markers in the 
page.

### Input

The parser gets a response object (the `text` attribute of this object contains the *crawled* HTML content) from the crawler process. In order to parse it, there is unlimited flexibility in terms of which libraries to use (e.g. 
`beautifulsoup`).

### Output

Upon successful identification of datasets or resources in the parsed page, the 
parser will need to create instances of the `Dataset` and `Resource`, respectively. 

If multiple datasets are detected on page, for every dataset model completed 
(i.e. has all the extracted properties and at least one resource) the parser 
need to `yield` the resulting object.

If only one dataset is detected, then a simple `return` statement is used to return the resulting object.

## How to create a new scraper

Assuming we're about to create a new scraper called `students`:

* create a new directory under `edscrapers/scrapers` called `students`
* inside the new directory, create empty `__init__.py`, `crawler.py` and 
  `parser.py` files

The `crawler.py` needs to contain:

```python
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor

from edscrapers.scrapers.students.parser import parse


class Crawler(CrawlSpider):

    name = 'students'

    # This is the regex for allowed URLs
    allowed_regex = r'students.example.org'

    def __init__(self):

        self.start_urls = [
            # This is the starting point
            'https://students.example.org/',
        ]

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                allow=self.allowed_regex,
            ), callback=parse, follow=True),
        ]

        # Inherit parent
        super(Crawler, self).__init__()
```


A `parser.py` example:

```python
from slugify import slugify

from edscrapers.scrapers import base
from edscrapers.scrapers.base.models import Dataset, Resource
import edscrapers.scrapers.base.helpers as h


# mandatory: list of patterns to ignore
deny_list = []

def parse(res):

    # Initialize the model
    dataset = Dataset()
    dataset['resources'] = []

    # Using helper function to extract a list of stub resources
    # (from this point on, feel free to improve the parsing)
    h.get_all_resources(res, dataset, h.get_data_extensions(), deny_list=deny_list)

    # No resources, no dataset
    if len(dataset['resources']) > 0:

        # Get source_url
        dataset['source_url'] = res.url
        # Get title from <meta> tags
        dataset['title'] = res.xpath('//meta[@name="DC.title"]/@content').get('text')
        if not dataset['title'] or dataset['title'] == 'text':
            # ...or from the <title> tag
            dataset['title'] = res.xpath('/html/head/title/text()').get('text')
        # Get dataset name by slugifying the URL
        dataset['name'] = slugify(res.url)
        # Get description from <meta> tags
        dataset['notes'] = res.xpath('//meta[@name="DC.description"]/@content').get('text')

        # Return the only dataset extracted
        return dataset

    # Return None if nothing was found
    return None
```
