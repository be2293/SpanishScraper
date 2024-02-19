import SpanishScraperFunctions as scraper
import pandas as pd
from bs4 import BeautifulSoup


df = scraper.FullSubjectScrape("ingenieria")
df.to_csv("ingenieria.csv")

