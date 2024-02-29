import SpanishScraperFunctions as scraper
import pandas as pd
from bs4 import BeautifulSoup


df_list = []
subject_list = ["Tecnología", "Máquinas","Agricultura","Economía doméstica","Cuidado y administración del hogar","Hostelería","Organización y gestión de la industria, el comercio y de las communicaciones","química","Industrias afines", "Industria y oficios diversos","Construcción"]
for x in subject_list:
    df_list.append(scraper.FullSubjectScrape(x))
FullDataFrame = pd.concat(df_list)
FullDataFrame.to_csv("FullSpanishData.csv")

