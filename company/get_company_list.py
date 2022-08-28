# -*- coding: utf-8 -*-
from re import T
import chromedriver_binary
import pandas as pd
import csv
import sys
import time
import os
from os import wait
from asyncio import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = Options()
driver = webdriver.Chrome()

# 業界リストを読み込み
industry_list = []
filename = "../input/industry.csv"
with open(filename, encoding='utf8', newline='') as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        industry_list.append(row[0])

for industry in industry_list:
    stock_id_list = []
    company_name_list = []
    
    print(industry + ": start!!")
    url = "https://www.jpubb.com/list/list.php?listed=1&ind=" + industry
    driver.get(url)

    while True:
        company_elems = driver.find_elements(by=By.CLASS_NAME, value='fillcolor')
        # そのページの該当するリンクをリストに格納
        for company_elem in company_elems:
            try:
                stock_id = company_elem.find_element(by=By.CLASS_NAME, value='code').text
                company_name = company_elem.find_element(by=By.CLASS_NAME, value='name').text

                stock_id_list.append(stock_id)
                company_name_list.append(company_name)
            except Exception:
                continue

        company_elems = driver.find_elements(by=By.CLASS_NAME, value='nofill')
        # そのページの該当するリンクをリストに格納
        for company_elem in company_elems:
            try:
                stock_id = company_elem.find_element(by=By.CLASS_NAME, value='code').text
                company_name = company_elem.find_element(by=By.CLASS_NAME, value='name').text

                stock_id_list.append(stock_id)
                company_name_list.append(company_name)
            except Exception:
                continue

        # そのページの一番下にスクロール
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(99)

        # 次へをクリックしページ遷移する
        try:
            next_button = driver.find_element(by=By.LINK_TEXT, value='Next »')
            next_button.click()
            driver.implicitly_wait(99)
        except Exception:
            print("exception")
            break

    dict = {
        'code': stock_id_list,
        'name': company_name_list,
    } 
    df = pd.DataFrame(dict) 
    df.to_csv("../output/" + industry + ".csv", header=False, encoding="utf-8", index=False)

driver.quit()

