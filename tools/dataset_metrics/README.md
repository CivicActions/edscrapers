
## Description

During the scraping process for Dept Ed, it's important we have verifiable, measurable values that help indicate the progress and scraping performance of the project. We have little or no tangible evidence of how well we are progressing. This python subpackage will tackle such metrics.

  

## Metric Questions
  
1. List of all domains scraped/parsed ordered by number of parsed pages (for both DATOPIAN & AIR).

  
  

## How to run metrics script

- Clone this repo `git clone https://github.com/CivicActions/ckanext-edscrapers.git`

- From the root dorectory of the repo run `python -m tools.dataset_metrics.run`

- Output from the metrics script is located in *'tools/dataset_metrics/metrics.xlsx'*