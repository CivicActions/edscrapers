
## Description

During the scraping process for Dept Ed, it's important we have verifiable, measurable values that help indicate the progress and scraping performance of the project. We have little or no tangible evidence of how well we are progressing. This python subpackage will tackle such metrics.

  

## Metric Questions
  
1. List of all domains scraped/parsed ordered by number of parsed pages (for both DATOPIAN & AIR)

2. What domains (subdomains) Datopian touched and AIR didn't and How many items (resources) were extracted from them?

3. What domains (subdomains) AIR touched and Datopian didn't? How many items were extracted from them? 

4. what pages collected the most resource for Datopian?

5. What pages collected the most resources for AIR?

6. What resources are EXCLUSIVE to edgov/data.json when compared with Datopian

7. What domains (subdomains) were both touched by Datopian and AIR? How manay items were extracted from the 'shared' touched domains? 

  
## How to run metrics script

- Create a python virtual environment 

- Clone this repo `git clone https://github.com/CivicActions/ckanext-edscrapers.git`

- From the root dorectory of the repo run `pip install requirements.txt`

- From the root dorectory of the repo run `python -m tools.dataset_metrics.run`

- Output from the metrics script is located in *'tools/dataset_metrics/metrics.xlsx'*