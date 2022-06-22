from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import pickle
import spacy
import string


def scrape_n_posts(mod, n):
    PATH = "C:/Users/Yan Rong/Documents/programming/Orbital/testsite/chromedriver.exe"
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)
    driver = webdriver.Chrome(options = option, executable_path = PATH)
    driver.get("https://www.reddit.com/r/nus/")
    search = driver.find_element_by_id("header-search-bar")
    search.send_keys(mod)
    time.sleep(3)
    search.send_keys(Keys.RETURN)

    result = []
    scale = 0
    inturl = driver.current_url
    while scale < n:
        try:
            main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='QBfRw7Rj8UkxybFpX-USO']")))
        except:
            driver.close()
            return ["Error"]
        links = main.find_elements(By.XPATH,f'//a[contains(@href,"{mod.lower()}")]')
        links[scale].click()
        #driver.switch_to.window(driver.window_handles[1])
        url = driver.current_url
        driver.get(url)
        html =  BeautifulSoup(driver.page_source, "html.parser")
        comments = html.find_all("p",{"class":"_1qeIAgB0cPwnLhDF9XSiJM"})
        for comment in comments:
            result.append(comment.text)
        #driver.close()
        #driver.switch_to.window(driver.window_handles[0])
        scale += 1
        driver.get(inturl)
    driver.close()
    return result

#NLTK VADER
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

def SIA_analyse_sent(comments):
    sia = SIA()
    results = []
    for comment in comments:
        pol_score = sia.polarity_scores(comment)
        pol_score["Comment"] = comment
        results.append(pol_score)

    df = pd.DataFrame.from_records(results)
    return (comments, df["compound"].mean())

def MODeRATE(MOD, n):
    return RFR_AI_model(scrape_n_posts(MOD, n))

def RFR_AI_model(comments):
    cleaned = []
    nlp = spacy.load("en_core_web_sm")
    for message in comments:
        str = ""
        doc = nlp(message)
        for token in doc:
            if not token.is_stop and not (token.text in string.punctuation) and token.text!= "\n":
                str += token.lemma_.lower() + " "
        cleaned.append(str[0:len(str)-1])
    
    model = pickle.load(open("C:/Users/Yan Rong/Documents/programming/Orbital/RFR_model.sav", 'rb'))
    ratings = model.predict(cleaned)
    average = sum(ratings)/len(ratings)
    return (comments, f'{average:.2f}')

def NB_AI_model(comments):
    model = pickle.load(open("NB_model.sav", 'rb'))
    ratings = model.predict(comments)
    average = sum(ratings)/len(ratings)
    return (comments, average)
