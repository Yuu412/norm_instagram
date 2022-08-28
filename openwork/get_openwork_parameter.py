# -*- coding: utf-8 -*-
from inspect import Parameter
from re import A, T
import chromedriver_binary
from cv2 import add, split
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
import random
import Levenshtein

INPUT_DIR_PATH = '../../input'
OUTPUT_DIR_PATH = '../../output_openwork/'

def ret_dic_graph_parameter(code, company_name):
    # 待遇面の満足度
    salary_satisfaction = driver.find_element(by=By.CSS_SELECTOR, value="li.scoreList_item-satisfy > dl > dd").text
    # 社員の士気
    employee_morale = driver.find_element(by=By.CSS_SELECTOR, value="li.scoreList_item-spirit > dl > dd").text
    # 風通しの良さ
    mood = driver.find_element(by=By.CSS_SELECTOR, value="li.scoreList_item-airy > dl > dd").text
    # 社員の相互尊重
    mutual_respect = driver.find_element(by=By.CSS_SELECTOR, value="li.scoreList_item-team > dl > dd").text
    # 20代成長環境
    growth_environment_junior = driver.find_element(by=By.CSS_SELECTOR, value="li.scoreList_item-junior > dl > dd").text
    # 人材の長期育成
    growth_environment_senior = driver.find_element(by=By.CSS_SELECTOR, value="li.scoreList_item-senior > dl > dd").text
    # 法令遵守意識
    compliance = driver.find_element(by=By.CSS_SELECTOR, value="li.scoreList_item-law > dl > dd").text
    # 人事評価の適正感
    hr_evaluation = driver.find_element(by=By.CSS_SELECTOR, value="li.scoreList_item-assess > dl > dd").text

    # 残業時間
    overtime_hours = driver.find_element(by=By.CSS_SELECTOR, value="div.jq_horizontalChart.w-250.mt-25.gray > dl:nth-child(1) > dd > span").text

    dict_graph_parameter = {
        "証券コード": code,
        "企業名": company_name,
        "待遇面の満足度": salary_satisfaction,
        "社員の士気": employee_morale,
        "風通しの良さ": mood,
        "社員の相互尊重": mutual_respect,
        "20代成長環境": growth_environment_junior,
        "人材の長期育成": growth_environment_senior,
        "法令遵守意識": compliance,
        "人事評価の適正感": hr_evaluation,   
        "残業時間": overtime_hours,
    }

    return dict_graph_parameter

def ret_dic_graph_null_parameter(code, company_name):
    dic_graph_null_parameter = {
        "証券コード": code,
        "企業名": company_name,
        "待遇面の満足度": '-',
        "社員の士気": '-',
        "風通しの良さ": '-',
        "社員の相互尊重": '-',
        "20代成長環境": '-',
        "人材の長期育成": '-',
        "法令遵守意識": '-',
        "人事評価の適正感": '-', 
        "残業時間": '-',
    }

    return dic_graph_null_parameter

# 業界名のcsv一覧を取得
indestry_csv_list = os.listdir(INPUT_DIR_PATH)

for industry_csv in indestry_csv_list:
    industry_name = industry_csv.replace('.csv', '')
    print(industry_name + ': START!!')

    if(industry_name == '.DS_Store'):
        continue

    output_filename = OUTPUT_DIR_PATH + industry_name + ".csv"
    incomplete_output_filename = OUTPUT_DIR_PATH + industry_name + "__incomplete.csv"

    cols=[
        '証券コード',
        '企業名',
        '待遇面の満足度',
        '社員の士気',
        '風通しの良さ',
        '社員の相互尊重',
        '20代成長環境',
        '人材の長期育成',
        '法令遵守意識',
        '人事評価の適正感',
        '残業時間'
    ]

    if(os.path.isfile(output_filename)):    
        continue
    elif(os.path.isfile(incomplete_output_filename)):
        df_graph_parameter = pd.read_csv(incomplete_output_filename, encoding="utf-8")
    else:
        df_graph_parameter = pd.DataFrame(index=[], columns=cols)

    # 企業リストを読み込み
    input_filename = INPUT_DIR_PATH + '/' + industry_csv
    df_company = pd.read_csv(input_filename, names=['code', 'name'], encoding="utf-8")

    # webdriver インスタンス作成
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(99)
    url = "https://www.vorkers.com/"

    driver.get(url)
    
    add_null_flag = True
    for index, company in df_company.iterrows():
        if(company['name'] in df_graph_parameter['企業名'].to_list()):
            continue

        time.sleep(random.randint(10,30))
        try:
            search_box = driver.find_element(by=By.CLASS_NAME, value="keywordSearch_input")
            search_box.send_keys(company['name'])
            time.sleep(5)
        except Exception:
            print('例外発生')
            driver.quit()
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.implicitly_wait(99)
            continue
        
        search_icon = driver.find_element(by=By.CLASS_NAME, value="keywordSearch_button")
        search_icon.click()
        time.sleep(5)

        # 検索結果に表示された企業一覧をリストに格納
        target_company_elements = driver.find_elements(by=By.CSS_SELECTOR, value='#contentsBody > section > ul > li > div.searchCompanyName > div:nth-child(1) > h3 > a')
        target_url_list = []
        for target_company_element in target_company_elements:
            target_url_list.append(target_company_element.get_attribute("href"))

        for target_url in target_url_list:  
            driver.get(target_url)
            time.sleep(random.randint(15,20))

            # 「もっと見る」をクリック
            driver.find_element(by=By.CSS_SELECTOR, value='.jsViewMoreCompanyInfoBox > .jsViewMoreCompanyInfo').click()
            time.sleep(3)

            # 証券コードを取得し、一致した場合のみ情報取得し、ループを抜ける
            target_code = driver.find_elements(by=By.CSS_SELECTOR, value=".definitionList-wiki > dd")[8].text.split(' (')[0]
            try:
                if(int(target_code) == int(company['code'])):
                    dic_graph_parameter = ret_dic_graph_parameter(company['code'], company['name'])
                    df_graph_parameter = df_graph_parameter.append(dic_graph_parameter, ignore_index=True)
                    df_graph_parameter.to_csv(incomplete_output_filename, header=cols, encoding="utf-8", index=False)
                    add_null_flag = False
                    break
            except Exception:
                print('Cant get target Code')
                continue
        
        #該当情報が存在しなかった場合は、各パラメーターに'-'を入れる
        if(add_null_flag):
            dic_graph_parameter = ret_dic_graph_null_parameter(company['code'], company['name'])
            df_graph_parameter = df_graph_parameter.append(dic_graph_parameter, ignore_index=True)
            df_graph_parameter.to_csv(incomplete_output_filename, header=cols, encoding="utf-8", index=False)
        add_null_flag = True
    
    #完成版を保存し、未完成版を削除
    df_graph_parameter.to_csv(output_filename, header=cols, encoding="utf-8", index=False)
    os.remove(incomplete_output_filename)

    driver.quit()
    
    #アクセス過多を防ぐために一旦抜ける仕様にしている
    #exit()