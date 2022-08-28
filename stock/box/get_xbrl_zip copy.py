#######

# /Users/yuu/develop/norm_automation/output_stock/summary.csv　
# から証券コードを指定して、該当するデータの最新情報を取得＆その期間のxbrlをDLして、xbrl2csvして、業績グラフと、安定性etcスコアを自動生成するようにする

#######


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

START_DATE = datetime(2021, 6, 24)
END_DATE = datetime(2022, 3, 26)

COLS = ['seqNumber', 'docID', 'edinetCode', 'secCode', 'JCN', 'filerName','fundCode', 'ordinanceCode', 'formCode', 'docTypeCode', 'periodStart',
       'periodEnd', 'submitDateTime', 'docDescription', 'issuerEdinetCode',
       'subjectEdinetCode', 'subsidiaryEdinetCode', 'currentReportReason',
       'parentDocID', 'opeDateTime', 'withdrawalStatus', 'docInfoEditStatus',
       'disclosureStatus', 'xbrlFlag', 'pdfFlag', 'attachDocFlag',
       'englishDocFlag'],

def get_submitted_summary(params):
    url = EDINET_API_URL + '/documents.json'
    response = requests.get(url, params=params)
     
    # responseが200でなければエラーを出力
    assert response.status_code==200
       
    return response.json()

def get_document(doc_id, params):
    url = EDINET_API_URL + '/documents/' + doc_id
    response = requests.get(url, params)
     
    return response

def download_document(doc_id, save_path):
    params = {'type': 1}
    doc = get_document(doc_id, params)
    if doc.status_code == 200:
        with open(save_path + doc_id + '.zip', 'wb') as f:
            for chunk in doc.iter_content(chunk_size=1024):
                f.write(chunk)

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
        #df_doc_summary.to_csv(save_path + date + '/doc_summary.csv')
 
        # 書類を保存
        for _, doc in df_doc_summary.iterrows():
            if(doc['secCode'] == None):
                continue
            #download_document(doc['docID'], save_path + date + '/')
            #open_zip_file(doc['docID'], save_path + date + '/')
        return df_doc_summary
     
    return df_doc_summary

def open_zip_file(doc_id, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path + doc_id)
    
    print(os.path.basename(save_path + doc_id + '.zip'))

    with zipfile.ZipFile(save_path + doc_id + '.zip') as zip_f:
        zip_f.extractall(save_path + doc_id)

def date_range(start_date: datetime, end_date: datetime):
    diff = (end_date - start_date).days + 1
    return (start_date + timedelta(i) for i in range(diff))

def remove_empty_folder():
    # OUTPUT_PATH内の全フォルダを取得
    dirs = [f for f in os.listdir(OUTPUT_PAHT) if os.path.isdir(os.path.join(OUTPUT_PAHT, f))]

    for dir in dirs:
        dir_path = OUTPUT_PAHT + '/' + dir
        files = [f for f in os.listdir(dir_path) if not f.startswith(".")]
        if not files:
            shutil.rmtree(dir_path)

def split_df_by_year(df):
    df_2022 = df[df['periodEnd'] > '2021-12-31']
    df_2021 = df[(df['periodEnd'] > '2020-12-31') & (df['periodEnd'] <= '2021-12-31')]
    df_2020 = df[(df['periodEnd'] > '2019-12-31') & (df['periodEnd'] <= '2020-12-31')]
    return {
        '2022': df_2022,
        '2021': df_2021,
        '2020': df_2020,
    }

for i, date in enumerate(date_range(START_DATE, END_DATE)):
    date_str = str(date)[:10]
    print(date_str)

    df_doc_summary = download_all_documents(date_str, OUTPUT_PAHT)
    #if(type(df_doc_summary) == bool):
        #continue

    if i == 0:
        df_doc_summary_all = df_doc_summary.copy()
    else:
        #df_doc_summary_all = pd.concat([df_doc_summary_all, df_doc_summary])
        df_doc_summary_all = df_doc_summary_all.append(df_doc_summary, ignore_index=True)

#print('split')
#df_doc_summary_all = split_df_by_year(df_doc_summary_all)

df_doc_summary_all.to_csv(OUTPUT_SUMMARY_PATH)

remove_empty_folder()

#df_doc_summary.query('edinetCode=="E31070"')
#download_document(doc_id='S100IC1B', OUTPUT_PATH='./')

