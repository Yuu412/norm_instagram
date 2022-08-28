# -*- coding: utf-8 -*-
from inspect import Parameter
from re import A, T
from tokenize import group
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
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select

def ret_dic_graph_parameter(code, company_name):

    ##
    # なぜかグラフの数値が取れない
    ###


    # 選考難易度
    selection_level = driver.find_element(by=By.XPATH, value='//*[@id="highcharts-nkdhhov-8"]/svg/g[7]/text[1]/tspan[2]').text
    # 企業理解
    company_understanding = driver.find_element(by=By.XPATH, value='//*[@id="highcharts-nkdhhov-8"]/svg/g[7]/text[3]/tspan[2]').text
    # 業界理解
    industry_understanding = driver.find_element(by=By.XPATH, value='//*[@id="highcharts-nkdhhov-8"]/svg/g[7]/text[2]/tspan[2]').text
    # 自己成長
    growth = driver.find_element(by=By.XPATH, value='//*[@id="highcharts-nkdhhov-8"]/svg/g[7]/text[5]/tspan[2]').text
    # 内定直結度
    preferential_degrees = driver.find_element(by=By.XPATH, value='//*[@id="highcharts-nkdhhov-8"]/svg/g[7]/text[6]/tspan[2]').text

    # 年度の選択
    dropdown = driver.find_element(by=By.ID, value='evaluate')
    select = Select(dropdown)

    print(type(selection_level))
    exit()


    try:
        select.select_by_index(1)
    except Exception:
        pass

    dic_graph_parameter = {
        "証券コード": code,
        "企業名": company_name,
        '選考難易度': selection_level,
        '企業理解': company_understanding,
        '業界理解': industry_understanding,
        '自己成長': growth,
        '内定直結度': preferential_degrees,
    }

    return dic_graph_parameter

# 企業リストを読み込み
filename = "../input/test.csv"
df_company = pd.read_csv(filename, names=['code', 'name'], encoding="utf-8")

options = Options()
driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://syukatsu-kaigi.jp/"

# 列を指定し、空のデータフレーム作成し、代入
cols=[
    '選考難易度',
    '企業理解',
    '内定直結度'
    ]
df_graph_parameter = pd.DataFrame(index=[], columns=cols)

for index, company in df_company.iterrows():
    driver.get(url)
    driver.implicitly_wait(99)

    search_box = driver.find_element(by=By.ID, value="company_form_q_top")
    search_box.send_keys(company['name'])

    driver.implicitly_wait(99)

    search_icon = driver.find_element(by=By.CLASS_NAME, value="p-search-field__button")
    search_icon.click()

    driver.implicitly_wait(99)

    try:
        target_company_element = driver.find_element(by=By.CSS_SELECTOR, value="body > div.l-main-one > div.l-wrapper__gutter > main > div:nth-child(2) > div > div > a").click()
    except Exception:
        continue

    driver.implicitly_wait(99)
    
    try:
        internship_group_element = driver.find_element(by=By.CSS_SELECTOR, value="#company-nav > ul > li:nth-child(5)").click() 
        internship_page_element = driver.find_element(by=By.CSS_SELECTOR, value="#company-nav > ul > li:nth-child(5) > ul > li:nth-child(1) > a").click() 
    except Exception:
        continue

    driver.implicitly_wait(99)
    driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN) 
    driver.implicitly_wait(99)

    dic_graph_parameter = ret_dic_graph_parameter(company['code'], company['name'])
    df_graph_parameter = df_graph_parameter.append(dic_graph_parameter, ignore_index=True)

driver.close()
df_graph_parameter.to_csv("../output/" + "industry" + ".csv", header=cols, encoding="utf-8", index=False)