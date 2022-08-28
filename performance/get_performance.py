# -*- coding: utf-8 -*-
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
import chromedriver_binary
from webdriver_manager.chrome import ChromeDriverManager

INPUT_DIR_PATH = '../../input'
OUTPUT_DIR_PATH = "../../output_performance/"


def remake_webdriver():
    driver.quit()
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(99)

def get_parameter(xpath, css_selector):
    try:
        value = driver.find_element(by=By.XPATH, value=xpath).text,
    except Exception:
        try:
            value = driver.find_element(by=By.XPATH, value=css_selector).text,
        except Exception:
            return '-'
    return value[0]
    
def ret_dic_graph_parameter(code, company_name):
    dic_graph_parameter = {
        "証券コード": code,
        "企業名": company_name.replace(' ', ''),
        'prior1Year': get_parameter(
            '//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[1]/th',
            '#xcompany_info > div:nth-child(2) > div.md_card.md_box > div > div.ly_content_wrapper.size_ss > div > table > tbody > tr:nth-child(1) > th'
        ).split('年')[0],
        'prior2Year': get_parameter(
            '//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[2]/th',
            '#xcompany_info > div:nth-child(2) > div.md_card.md_box > div > div.ly_content_wrapper.size_ss > div > table > tbody > tr:nth-child(2) > th'
        ).split('年')[0],
        'prior3Year': get_parameter(
            '//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[3]/th',
            '#xcompany_info > div:nth-child(2) > div.md_card.md_box > div > div.ly_content_wrapper.size_ss > div > table > tbody > tr:nth-child(3) > th'
        ).split('年')[0],
        'prior4Year': get_parameter(
            '//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[4]/th',
            '#xcompany_info > div:nth-child(2) > div.md_card.md_box > div > div.ly_content_wrapper.size_ss > div > table > tbody > tr:nth-child(4) > th'
        ).split('年')[0],
        
        'prior1YearSales': get_parameter(
            '//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[1]/td[1]',
            '#xcompany_info > div:nth-child(2) > div.md_card.md_box > div > div.ly_content_wrapper.size_ss > div > table > tbody > tr:nth-child(1) > td:nth-child(2)'
        ),
        'prior2YearSales': get_parameter(
            '//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[2]/td[1]',
            '#xcompany_info > div:nth-child(2) > div.md_card.md_box > div > div.ly_content_wrapper.size_ss > div > table > tbody > tr:nth-child(2) > td:nth-child(2)'
        ),
        'prior3YearSales': get_parameter(
            '//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[3]/td[1]',
            '#xcompany_info > div:nth-child(2) > div.md_card.md_box > div > div.ly_content_wrapper.size_ss > div > table > tbody > tr:nth-child(3) > td:nth-child(2)'
        ),
        
        'prior4YearSales': get_parameter(
            '//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[4]/td[1]',
            '#xcompany_info > div:nth-child(2) > div.md_card.md_box > div > div.ly_content_wrapper.size_ss > div > table > tbody > tr:nth-child(4) > td:nth-child(2)'
        ),

        'prior1YearProfit': get_parameter(
            '//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[1]/td[2]',
            '#xcompany_info > div:nth-child(2) > div.md_card.md_box > div > div.ly_content_wrapper.size_ss > div > table > tbody > tr:nth-child(1) > td:nth-child(3)'
        ),
        'prior2YearProfit': get_parameter(
            '//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[2]/td[2]',
            '#xcompany_info > div:nth-child(2) > div.md_card.md_box > div > div.ly_content_wrapper.size_ss > div > table > tbody > tr:nth-child(2) > td:nth-child(3)'
        ),
        'prior3YearProfit': get_parameter(
            '//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[3]/td[2]',
            '#xcompany_info > div:nth-child(2) > div.md_card.md_box > div > div.ly_content_wrapper.size_ss > div > table > tbody > tr:nth-child(3) > td:nth-child(3)'
        ),
        'prior4YearProfit': get_parameter(
            '//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[4]/td[2]',
            '#xcompany_info > div:nth-child(2) > div.md_card.md_box > div > div.ly_content_wrapper.size_ss > div > table > tbody > tr:nth-child(4) > td:nth-child(3)'
        ),
    }
    """
    'prior1YearEquityRatio': driver.find_element(by=By.XPATH, value='//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[1]/td[4]').text,
    'prior2YearEquityRatio': driver.find_element(by=By.XPATH, value='//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[2]/td[4]').text,
    'prior3YearEquityRatio': driver.find_element(by=By.XPATH, value='//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[3]/td[4]').text,
    'prior4YearEquityRatio': driver.find_element(by=By.XPATH, value='//*[@id="xcompany_info"]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[4]/td[4]').text,
    'prior1YearROA': (driver.find_element(by=By.XPATH, value='//*[@id="xcompany_info"]/div[2]/div[2]/div/div[4]/div[2]/div[2]/div/table/tbody/tr[1]/td[1]').text).replace('%', ''),
    'prior2YearROA': (driver.find_element(by=By.XPATH, value='//*[@id="xcompany_info"]/div[2]/div[2]/div/div[4]/div[2]/div[2]/div/table/tbody/tr[2]/td[1]').text).replace('%', ''),
    'prior3YearROA': (driver.find_element(by=By.XPATH, value='//*[@id="xcompany_info"]/div[2]/div[2]/div/div[4]/div[2]/div[2]/div/table/tbody/tr[3]/td[1]').text).replace('%', ''),
    'prior4YearROA': (driver.find_element(by=By.XPATH, value='//*[@id="xcompany_info"]/div[2]/div[2]/div/div[4]/div[2]/div[2]/div/table/tbody/tr[4]/td[1]').text).replace('%', ''),
    'prior1YearROE': (driver.find_element(by=By.XPATH, value='//*[@id="xcompany_info"]/div[2]/div[2]/div/div[4]/div[2]/div[2]/div/table/tbody/tr[1]/td[2]').text).replace('%', ''),
    'prior2YearROE': (driver.find_element(by=By.XPATH, value='//*[@id="xcompany_info"]/div[2]/div[2]/div/div[4]/div[2]/div[2]/div/table/tbody/tr[2]/td[2]').text).replace('%', ''),
    'prior3YearROE': (driver.find_element(by=By.XPATH, value='//*[@id="xcompany_info"]/div[2]/div[2]/div/div[4]/div[2]/div[2]/div/table/tbody/tr[3]/td[2]').text).replace('%', ''),
    'prior4YearROE': (driver.find_element(by=By.XPATH, value='//*[@id="xcompany_info"]/div[2]/div[2]/div/div[4]/div[2]/div[2]/div/table/tbody/tr[4]/td[2]').text).replace('%', ''),
    """

    return dic_graph_parameter

# 業界名のcsv一覧を取得
indestry_csv_list = os.listdir(INPUT_DIR_PATH)

for industry_csv in indestry_csv_list:
    industry_name = industry_csv.replace('.csv', '')
    print(industry_name + ': START!!')

    if(industry_name == '.DS_Store'):
        continue

    # すでに探索済みの業界の場合
    if(os.path.isfile(OUTPUT_DIR_PATH + industry_name + ".csv")):
        continue

    # 企業リストを読み込み
    filename = INPUT_DIR_PATH + '/' + industry_name + ".csv"
    df_company = pd.read_csv(filename, names=['code', 'name'], encoding="utf-8")

    # 列を指定し、空のデータフレーム作成し、代入
    cols=[
        '証券コード',
        '企業名',
        'prior1Year',
        'prior2Year',
        'prior3Year',
        'prior4Year',
        'prior1YearSales',
        'prior2YearSales',
        'prior3YearSales',
        'prior4YearSales',
        'prior1YearProfit',
        'prior2YearProfit',
        'prior3YearProfit',
        'prior4YearProfit',
        ]

    """
    'prior1YearEquityRatio',
    'prior2YearEquityRatio',
    'prior3YearEquityRatio',
    'prior4YearEquityRatio',
    'prior1YearROA',
    'prior2YearROA',
    'prior3YearROA',
    'prior4YearROA',
    'prior1YearROE',
    'prior2YearROE',
    'prior3YearROE',
    'prior4YearROE',
    """

    df_graph_parameter = pd.DataFrame(index=[], columns=cols)
    # webdriver インスタンス作成
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver = webdriver.Chrome()
    driver.implicitly_wait(99)

    for index, company in df_company.iterrows():
        url = "https://minkabu.jp/stock/" + str(company['code']) + "/settlement"
        try:
            driver.get(url)
        except Exception:
            print('例外発生')
            driver.quit()
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.implicitly_wait(99)
            driver.get(url)
        try:
            site_map = driver.find_element(by=By.CSS_SELECTOR, value='#breadcrumbs > div').text
        except Exception:
            print('例外発生')
            driver.quit()
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.implicitly_wait(99)
            driver.get(url)

        if(site_map == '株式/指数 サイトマップ'):
            continue

        #time.sleep(5)
        try:
            company_name = driver.find_element(by=By.CLASS_NAME, value='md_stockBoard_stockName').text
            print(company['name'] + '( ' + company_name + ' ) | ' + str(company['code']))
        except Exception:
            print('例外発生')
            driver.quit()
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.implicitly_wait(99)
            driver.get(url)

        dic_graph_parameter = ret_dic_graph_parameter(company['code'], company['name'])
        df_graph_parameter = df_graph_parameter.append(dic_graph_parameter, ignore_index=True)

    driver.quit()
    df_graph_parameter.to_csv(OUTPUT_DIR_PATH + industry_name + ".csv", header=cols, encoding="utf-8", index=False)
