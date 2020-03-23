## NCES PARSER (WIP)
The NCES subdomain from initial rough crawling houses alot of pages and datasets. The structures of these pages are varied. So we have adopted a gradual stepwise approach of analysing page structures and creating parses.
So far these are the type of page structures discovered:

 1. **Page Structure 1** -  See sample [https://nces.ed.gov/surveys/els2002/tables/APexams_01.asp](https://nces.ed.gov/surveys/els2002/tables/APexams_01.asp). 
 - In this structure, there is only 1 dataset/page. The page's main container is `<div clas="MainContent"></div>`.  
 - The dataset resources are housed in a table `<table></table>`. 
 - Resources have no description, but their name is obtained from a `div` located in `body`of html. The div is `<div class="title"></div>`

 2. **Page Structure 2** -  See sample [https://nces.ed.gov/pubs2009/expenditures/tables/table_08.asp?referrer=report](https://nces.ed.gov/pubs2009/expenditures/tables/table_08.asp?referrer=report). 
 - In this structure, there is only 1 dataset/page. The page's main container is `<div clas="nces"></div>`.  
 - The dataset resources are housed in a table `<table></table>`. 
 - Resources have no description, but their name is obtained from a `table` with `<th class="title"></th>`

  3. **Page Structure 3** -  See sample [https://nces.ed.gov/ipeds/deltacostproject/](https://nces.ed.gov/ipeds/deltacostproject/). 
 - In this structure, there is only 1 dataset/page. The page's main container is `<div clas="MainContent"></div>`.  
 - The dataset resources are housed in a table `<table></table>`. 
 - Resources have no description, but their name is obtained the content of the `a` tag which links to the resource