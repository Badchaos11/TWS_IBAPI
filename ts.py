import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
from time import sleep
import pyautogui as pg


def data_loader(ticker: str):
    try:
        barcode = "seo@2site.ru"
        password = 'MSIGX660'

        # ____________________ Работа с Selenium ____________________________
        path = os.path.join(os.getcwd(), 'chromedriver.exe')
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--start-maximized")

        checker = webdriver.Chrome(options=chrome_options)
        checker.get(f'https://www.gurufocus.com/')
        sleep(3)
        sign_in_click = checker.find_element(by=By.LINK_TEXT, value='''Login''')
        sign_in_click.click()
        sleep(3)
        sign_in_userName = checker.find_element(by=By.ID, value="login-dialog-name-input")
        sign_in_userName.send_keys(barcode)
        sign_in_password = checker.find_element(by=By.ID, value="login-dialog-pass-input")
        sign_in_password.send_keys(password)
        sleep(2)
        sign_in = checker.find_element(by=By.XPATH,
                                       value='''//*[@id="__layout"]/div/div/div[2]/div/div/div[2]/form/div[
                                       6]/button/span/span/div''')
        sign_in.click()
        sleep(5)

        url_f = f"https://www.gurufocus.com/stock/{ticker}/financials"
        checker.get(url_f)
        sleep(5)
        html = checker.find_element(by=By.TAG_NAME, value='body')
        html.click()
        sleep(0.5)
        html.send_keys(Keys.PAGE_DOWN)
        sleep(1)
        html.click()

        pm = pg.size()
        pg.moveTo(pm[0] / 2, pm[1] / 2)
        pg.click()
        pg.scroll(2)
        sleep(10)

        y = checker.find_element(By.XPATH,
                                 "//section[@id='stock-page-container']/main/div[3]/div/div/div[3]/div/div/div[2]/div["
                                 "2]/div/button[5]/span")
        y.click()
        sleep(10)

        x = checker.find_element(By.XPATH,
                                 "//section[@id='stock-page-container']/main/div[3]/div/div/div[3]/div/div/div[2]/div["
                                 "3]/div/button/span")
        x.click()
        sleep(5)
        x2 = checker.find_element(By.XPATH, "//body/ul/li[4]")
        x2.click()
        sleep(3)
        sleep(5)
        print('Go to next ticker')
    except:
        print('Cant download file')


df = pd.read_excel("GDX.xlsx")
for i in range(len(df)):
    tk = df.iloc[i][0]
    data_loader(tk)
