##to use bs2 and selenum to navigate the Conwy planning portal and scrape applications
#for selenium setup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#for scraping
import random
import time
from datetime import date, timedelta
import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml

def main():
    # initialise index, this tracks the page number we are on. every additional page adds 24 to the index

    # create lists to store our data
    all_id = []
    all_locations = []
    all_proposals = []
    all_types = []
    today = date.today().strftime("%m/%d/%Y")
    # yesterday = (date.today() - timedelta(1)).strftime("%m/%d/%Y")
    options = Options()
    #options.add_argument("--headless")
    # get the search page up, and click to do a full search
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://npe.conwy.gov.uk/Northgate/EnglishPlanningExplorer/generalsearch.aspx")
    #click thru to advanced search page
    driver.find_element(By.XPATH, "//*[@id='searchButton']").click()
    #add dates
    inputElement = driver.find_element(By.XPATH, "//*[@id='dateStart']").send_keys('04/01/2020')
    inputElement = driver.find_element(By.XPATH, "//*[@id='dateEnd']").send_keys('15/08/2022')
    #search
    inputElement = driver.find_element(By.XPATH, "//*[@id='csbtnSearch']").send_keys(Keys.ENTER)

    SCROLL_PAUSE_TIME = 2

    planning = driver.page_source

    df_initial = pd.read_html(planning)
    df = pd.concat(df_initial)


   #scroll all pages
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Next"))).click()
            print('here')
            planning = driver.page_source
            df_int = pd.read_html(planning)
            df_next = pd.concat(df_int)
            df = pd.concat([df, df_next])
            print(df)
        except TimeoutException:
            break

    df.to_csv(r"conwy_planning_data.csv")

if __name__ == "__main__":
    main()


