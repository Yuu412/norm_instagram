import requests
import os
import zipfile
import shutil
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

EDINET_API_URL = "https://disclosure.edinet-fsa.go.jp/api/v1"
OUTPUT_PAHT = "../../output_stock/original_data/"
OUTPUT_SUMMARY_PATH = '../../output_stock/summary.csv'

END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=5*365) #5年x365日

def get_submitted_summary(params):
    url = EDINET_API_URL + '/documents.json'
    response = requests.get(url, params=params)
     
    # responseが200でなければエラーを出力
    assert response.status_code==200
    return response.json()

SUMMARY_TYPE = 2
def download_all_documents(date, save_path, doc_type_codes=['120']):
    params = {'date': date, 'type': SUMMARY_TYPE}
    doc_summary = get_submitted_summary(params)
    try:
        df_doc_summary = pd.DataFrame(doc_summary['results'])
    except Exception:
        return False

    # 対象とする報告書のみ抽出
    if len(df_doc_summary) >= 1:
        df_doc_summary = df_doc_summary.loc[df_doc_summary['docTypeCode'].isin(doc_type_codes)]
 
        # 一覧を保存
        if not os.path.exists(save_path + date):
            os.makedirs(save_path + date)

        return df_doc_summary
     
    return df_doc_summary

def date_range(start_date: datetime, end_date: datetime):
    diff = (end_date - start_date).days + 1
    return (start_date + timedelta(i) for i in range(diff))

def remove_unnessesary_row(df):
    # secCodeが0のindexのリストを作成
    index_list = df['secCode'].dropna(axis=0).index
    df = df.loc[index_list]
    df = df.reset_index(drop=True)

    return df

for i, date in enumerate(date_range(START_DATE, END_DATE)):
    date_str = str(date)[:10]
    print(date_str)

    df_doc_summary = download_all_documents(date_str, OUTPUT_PAHT)

    if i == 0:
        df_doc_summary_all = df_doc_summary.copy()
    else:
        df_doc_summary_all = df_doc_summary_all.append(df_doc_summary, ignore_index=True)

df_doc_summary_all = remove_unnessesary_row(df_doc_summary_all)
df_doc_summary_all.to_csv(OUTPUT_SUMMARY_PATH)