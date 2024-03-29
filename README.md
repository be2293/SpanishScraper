# Spanish National Library Scraper

*Created by Benjamin Eyal, February 2024.*

This program scrapes the catalog of the Spanish National Library for technical items published between 1500 and 1930.

The program records the following data for each item:
- Title
- Author
- Call Number
- Publication Year
- Document Type
- Title with Numerics Removed (AltTitle)
- Subject (query)

## Search details
The searches made by this scraper are equivalent to filling out the following fields in the advanced search (http://catalogo.bne.es/uhtbin/webcat) form of the catalog:
- [x] Years Published/Created: From 1500 to 1930 
- [x] Type of Material: All
- [x] Subject = Query input
- [x] Language: Spanish

The scraper will scrape all of the results pages. If a search does not have any results, the program will not have any output. If it does, it will output a CSV of the results 

## Saving Results
The program will save two csv to your working directory, one "raw" dataset with all entries accrued, and one clean one that removes entries that are duplicates of another (Primary key = Year, Title)

## Functions
If you want to scrape a topic, or group of topics, load the functions in SpanishScraperfunctions.R to your workspace. Then, run the following full code of SpanishScraperMain:
```py
import SpanishScraperFunctions as scraper
import pandas as pd
from bs4 import BeautifulSoup

#instantiates a list to put the data in
df_list = []

#picks the list of subjects to scrape
subject_list = ["Your Subjects Here", "More Subjects Here"]

#Scrapes each subject
for x in subject_list:
    df_list.append(scraper.Full_Subject_Scrape(x))

#gets both a raw and duplicates-removed frame 
FullDataFrame = pd.concat(df_list)
DuplicatesRemovedDataFrame = FullDataFrame.drop_duplicates(subset=['Title','Year'], keep = 'first')

#saves frames to your computer 
FullDataFrame.to_csv("FullSpanishData.csv")
DuplicatesRemovedDataFrame.to_csv("CleanSpanishData.csv")
```
The function FullSubjectScrape is structured as follows:
1. Navigates through selenium from the search page to the first page of the results
2. Extract the number of results pages associated with that search.
3. Loop through each page number and:
   1. Extract the source code from the page.
   2. Iterate to the next page
4. Parse the HTML into a dataframe with the required results for each page
5. Collect all the dataframes into a single dataset
6. Clean the dataframe
7. Assign the subject category
8. Return the dataset


## note on alteration:
Because the Spanish Library does not allow you to pick more than one doc type, we have yet to decide which document types are relevant to our research. This can be done simply through excel, R, Python or any other program. 