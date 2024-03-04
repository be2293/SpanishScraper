from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import math
from bs4 import BeautifulSoup
import pandas as pd 

#Instantiates a selenium Firefox instance
driver = webdriver.Firefox()


#Navigates selenium to the first page associated with a subject
def Navigate_First_Page(subject):
    
    #Catalogue website
    driver.get('http://catalogo.bne.es/uhtbin/webcat')
    
    #Clicks advanced search
    driver.find_element(By.LINK_TEXT, 'Búsqueda avanzada' ).click()
    
    #Sets years from 1500-1930, sorts from oldest to newest, selects spanish language, and inputs the subject before clicking search
    driver.find_element(By.ID, 'searchdata4').send_keys(subject)
    Select(driver.find_element(By.ID, 'language')).select_by_value('CASTELLANO')
    driver.find_element(By.ID, "pubyear").send_keys("1500-1930")
    Select(driver.find_element(By.ID, 'sort_by')).select_by_value('PBYR')
    driver.find_element(By.CLASS_NAME, "button").click()


#gets the number of pages from the first page associated with a search
def Get_Page_Number():
    #This function assumes you are already using a selenium instance and are on the first page of a desired subject
    try:
        Number_Of_Entries = driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/ul/li/div/div/em").text   
        Number_Of_Pages = math.ceil(int(Number_Of_Entries)/30)
    except:
        Number_Of_Pages = 0
    return Number_Of_Pages

#Goes through each page and collects the source code HTML and then moves on to the next page
def Get_HTML(subject):
    
    #Gets to the first page of the subject
    Navigate_First_Page(subject)

    #acquires the number of pages
    Number_Of_Pages = Get_Page_Number()
    
    #iterates through pages, grabbing its HTML source code, and then clicking next
    HTML_List = []
    for x in range(0, Number_Of_Pages):
        HTML_List.append(driver.page_source)
        try:
            driver.find_element(By.LINK_TEXT, ">>").click()
        except:
            break
    return HTML_List

#creates a raw dataframe of the correct lines for each category
def Parse_HTML(response):

    #parses HTML
    soup = BeautifulSoup(response, "html.parser")
    raw = []
    images_raw = []
    
    #Gets all data associated with titles, authors, etc.
    for result in soup.find_all('dd'):
        raw.append(str(result))
    
    #gets all data corresponding to the image (which shows document type)
    Xpath_Expression = 'html>body>div>div>div>div>form>ul>li>ul>li:nth-of-type(4)'
    images = soup.select(Xpath_Expression)
    children = [] 
    for image in images:
        children.append(str(image.findChildren("img", recursive =False)))
    
    #sublists the dd data into the 7 categories: Title, Author, Call_Number, Publisher, Edition, Year and Holdings Statement
    Num_Sublists = 7
    sublists = [[] for _ in range(Num_Sublists)]
    for index, value in enumerate(raw):
        sublists[index % Num_Sublists].append(value)
    Title, Author, Call_Number, Publisher, Edition, Year, Holdings_Statement = sublists 

    #Creates a dataframe from the title, author, call-number, year and document type lines
    Raw_Data = pd.DataFrame({"Title":Title, "Author": Author, "Call_Number": Call_Number, "Year":Year, "Type":children})

    return Raw_Data

#Cleans the raw dataframe outputted by ParseHTML into a readable format
def Clean_HTML_Data_Frame(df):
    
    #readies the new columns
    TitleList = []
    AuthorList = []
    CallList = []
    YearList = []
    TypeList = []
    
    #Cleans title
    for result in df.Title:
        CleanResult = result.replace('\n', '').replace('\t', '')
        FirstIndex = CleanResult.find("View Details for ")+17
        SecondIndex = CleanResult.find("<!-- title -->")-2
        TitleList.append(CleanResult[FirstIndex:SecondIndex])
    df.Title = TitleList
    
    #Cleans Author
    for result in df.Author:
        CleanResult = result.replace('\n', '').replace('\t', '')
        FirstIndex = CleanResult.find("author -->")+10
        SecondIndex = CleanResult.find("<!-- and/or")
        AuthorList.append(CleanResult[FirstIndex:SecondIndex])
    df.Author = AuthorList
    
    #Cleans Call-number 
    for result in df.Call_Number:
        CleanResult = result.replace('\n', '').replace('\t', '')
        FirstIndex = CleanResult.find("allowed -->")+11
        SecondIndex = CleanResult.find("</dd")
        CallList.append(CleanResult[FirstIndex:SecondIndex])
    df.Call_Number = CallList
    
    #Cleans Year
    for result in df.Year:
        CleanResult = result.replace('\n', '').replace('\t', '')
        FirstIndex = CleanResult.find("<dd>")+4
        SecondIndex = CleanResult.find("</dd")
        YearList.append(CleanResult[FirstIndex:SecondIndex])
    df.Year = YearList
    
    #Cleans type data
    for result in df.Type:
        CleanResult = result.replace('\n', '').replace('\t', '')
        FirstIndex = CleanResult.find("g alt =")+12
        SecondIndex = CleanResult.find(" src=")-1
        TypeList.append(CleanResult[FirstIndex:SecondIndex])
    df.Type = TypeList
    
    #Translates type data
    replacements = {"":"NA","Monografías":"Monographs", "Dibujos, carteles, efímera, grabados, fotografías": "Drawings, Posters, Photos", "Manuscritos y archivos personales":"Manuscripts and Personal Archives", "Filminas, transparencias":"", "Grabaciones sonoras":"","Kit o multimedia":"","Mapas":"Maps","Materiales mixtos":"Mixed Materials","Partituras impresas y manuscritas":"sheet music", "Objetos tridimensionales":"Three Dimensional Objects", "Recursos electrónicos locales y remotos":"Electronic and Local Resources", "Prensa y revistas":"Newspapers/Magazines", "Videograbaciones":"videos"}
    df['Type'] = df['Type'].replace(replacements)
    
    #Translates an effective NA to a literal NA in the author column
    AuthorReplacements = {"=\"author\">":"NA"}
    df['Author'] = df['Author'].replace(AuthorReplacements)
    return df 

#the Main function. Goes to the first page, iterates through grabbing HTML, closes the selenium instance, merges all the raw datasets and then cleans them 
def Full_Subject_Scrape(subject):
    HTML_List = Get_HTML(subject)
    df_list = []
    for result in HTML_List:
        df_list.append(Parse_HTML(result))
    try:
        RawSubjectDF = pd.concat(df_list, ignore_index=True)
    except:
        RawSubjectDF = pd.DataFrame({"Title":[], "Author": [], "Call_Number": [], "Year":[], "Type":[]})
    FullSubjectDF = Clean_HTML_Data_Frame(RawSubjectDF)
    FullSubjectDF['Subject'] = subject
    return FullSubjectDF










