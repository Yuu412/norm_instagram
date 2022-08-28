#######

# /Users/yuu/develop/norm_automation/output_stock/summary.csv　
# から証券コードを指定して、該当するデータの最新情報を取得＆その期間のxbrlをDLして、xbrl2csvして、業績グラフと、安定性etcスコアを自動生成するようにする

#######

from cmath import nan
import math
import glob
import requests
import os
import sys
import zipfile
import shutil
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
sys.path.append(r'F:\project\kabu\Arelle')
from arelle import Cntlr

# path管理
EDINET_API_URL = "https://disclosure.edinet-fsa.go.jp/api/v1"
INPUT_PATH = '../../input'
OUTPUT_PAHT = "../../output/"
INPUT_SUMMARY_PATH = '../../output_stock/summary.csv'

START_DATE = datetime(2017, 8, 20)
END_DATE = datetime(2022, 8, 20)
TODAY = datetime.today().date()

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

def download_document(company_name, doc_id, code, industry_path):
    params = {'type': 1}
    doc = get_document(doc_id, params)
    if doc.status_code == 200:
        save_path = industry_path + '/' + str(code) + '_' + company_name + '/有価証券報告書'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with open(save_path + '/' + doc_id + '.zip', 'wb') as f:
            for chunk in doc.iter_content(chunk_size=1024):
                f.write(chunk)

SUMMARY_TYPE = 2
def download_all_documents(date, doc_type_codes=['120']):
    params = {'date': date, 'type': SUMMARY_TYPE}
    doc_summary = get_submitted_summary(params)
    try:
        df_doc_summary = pd.DataFrame(doc_summary['results'])
    except Exception:
        return False

    # 対象とする報告書のみ抽出
    if len(df_doc_summary) >= 1:
        df_doc_summary = df_doc_summary.loc[df_doc_summary['docTypeCode'].isin(doc_type_codes)]
 
        # 書類を保存
        for _, doc in df_doc_summary.iterrows():
            if(doc['secCode'] == None):
                continue
        return df_doc_summary
     
    return df_doc_summary

def open_zip_file(company_name, doc_id, code, industry_path):
    save_path = industry_path + '/' + str(code) + '_' + company_name + '/有価証券報告書/'

    with zipfile.ZipFile(save_path + doc_id + '.zip') as zip_f:
        zip_f.extractall(save_path + doc_id)

def date_range(start_date: datetime, end_date: datetime):
    diff = (end_date - start_date).days + 1
    return (start_date + timedelta(i) for i in range(diff))

def Arelle(company_name, doc_id, code, industry_path):
    # zip形式でxbrlを保存
    download_document(company_name, doc_id, code, industry_path)

    # zipを解凍
    open_zip_file(company_name, doc_id, code, industry_path)
    
    #xbrl形式のデータを選出
    company_dir_name = str(code) + '_' + company_name
    xbrl_file_list_path = industry_path + '/' + company_dir_name + '/有価証券報告書/' + str(doc_id) + '/XBRL/PublicDoc/*.xbrl'
    xbrl_file = glob.glob(xbrl_file_list_path)[0]

    ctrl = Cntlr.Cntlr(logFileName='logToPrint')

    try:
        # XBRL ファイルを読み込みます。
        model_xbrl = ctrl.modelManager.load(xbrl_file)
        try:
            # ヘッダを決めます。
            head = [
                '名前空間',
                '日本語', '英語',
                '接頭辞', 'タグ', 'ファクトID',
                '値', '単位', '貸借',
                '開始日', '終了日', '時点(期末日)',
                'コンテキストID', 'シナリオ',
                ]

            # fact を入れるリストを作ります。
            fact_datas = [head]

            for fact in model_xbrl.facts:
                label_ja = fact.concept.label(preferredLabel=None, lang='ja', linkroleHint=None)

                label_en = fact.concept.label(preferredLabel=None, lang='en', linkroleHint=None)
                x_value = fact.xValue

                # (4/7) 単位を取得します。
                if fact.unit is None:
                    unit = None
                else:
                    unit = fact.unit.value

                if fact.context.startDatetime:
                    start_date = fact.context.startDatetime
                else:
                    start_date = None

                if fact.context.endDatetime:
                    end_date = fact.context.endDatetime
                else:
                    end_date = None

                if fact.context.instantDatetime:
                    instant_date = fact.context.instantDatetime
                else:
                    instant_date = None

                # (6/7) シナリオ (scenario) を取得します。
                scenario_datas = []
                for (dimension, dim_value) in fact.context.scenDimValues.items():
                    scenario_datas.append([
                        dimension.label(preferredLabel=None, lang='ja', linkroleHint=None),
                        dimension.id,
                        dim_value.member.label(preferredLabel=None, lang='ja', linkroleHint=None),
                        dim_value.member.id,
                        ])
                if len(scenario_datas) == 0:
                    scenario_datas = None

                # (7/7) リストに追加します。
                fact_datas.append([
                    fact.namespaceURI, # (例) 'http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2019-11-01/jppfs_cor'
                    label_ja, # (例) '売上高'
                    label_en, # (例) 'Net sales'
                    fact.prefix, # (例) 'jppfs_cor'
                    fact.localName, # (例) 'NetSales'
                    fact.id, # (例) 'IdFact1707927900' (id は footnoteLink を参照するときに使いました)
                    x_value, # (例) Decimal('58179890000') (値は Decimal, int, None, str 型など色々でした)
                    unit, # (例) 'JPY'
                    fact.concept.balance, # (例) 'credit'
                    start_date, # (例) datetime.datetime(2019, 6, 1, 0, 0)
                    end_date, # (例) datetime.datetime(2020, 6, 1, 0, 0) (1日加算された日付になっていました)
                    instant_date, # (例) datetime.datetime(2020, 8, 29, 0, 0) (1日加算された日付になっていました)
                    fact.contextID, # (例) 'CurrentYearDuration'
                    scenario_datas, # (例) "[[
                                    #   '連結個別',
                                    #   'jppfs_cor_ConsolidatedOrNonConsolidatedAxis',
                                    #   '非連結又は個別',
                                    #   'jppfs_cor_NonConsolidatedMember',
                                    #  ],
                                    #  [
                                    #   '事業セグメント',
                                    #   'jpcrp_cor_OperatingSegmentsAxis',
                                    #   '種苗事業',
                                    #   'jpcrp030000-asr_E00004-000_SeedsAndSeedlingsReportableSegmentsMember',
                                    #  ]]"
                ])
        finally:
            # modelXbrl を閉じます。
            # (出典) ModelManager.py
            ctrl.modelManager.close()
    finally:
        # Arelle のコントローラーを閉じます。
        ctrl.close()

    cols = fact_datas[0]
    df = pd.DataFrame(index=[], columns=cols)

    for fact_data in fact_datas[1:-1]:
      # fact_data からdf に1行ずつ追加
      
      df = df.append(dict(zip(cols, fact_data)), ignore_index=True)

    # 解凍したディレクトリ&zipを削除
    shutil.rmtree(industry_path + '/' + company_dir_name + '/有価証券報告書/' + doc_id)
    os.remove(industry_path + '/' + company_dir_name + '/有価証券報告書/' + doc_id + '.zip')

    return df

# 業界名のcsv一覧を取得
indestry_csv_list = os.listdir(INPUT_PATH)
for industry_csv in indestry_csv_list:
    industry = industry_csv.replace('.csv', '')
    print(industry + ': START!!')

    if(industry == '.DS_Store'):
        continue

    #探索済みの業界リスト
    skip_industry_list = [
        '非鉄金属',
        '金属製品',
        #'医薬品',
        #'保険',
        #'化学',
        #'証券、商品先物取引',
        #'食品',
        #'不動産',
        #'ゴム',
    ]
    if(industry in skip_industry_list):
        continue


    industry_path = OUTPUT_PAHT + industry

    # 企業リストを読み込み
    input_filename = INPUT_PATH + '/' + industry_csv
    df_company = pd.read_csv(input_filename, names=['code', 'name'], encoding="utf-8")

    # サマリーのcsvを取得
    df_company_summary = pd.read_csv(INPUT_SUMMARY_PATH, encoding="utf-8", index_col=0)

    for index, company in df_company.iterrows():
        target_company_name = company['name']

        target_code = company['code']
        target_sec_code = target_code * 10

        #if os.path.exists(industry_path + '/' + str(target_code) + '_' + target_company_name + '/有価証券報告書'):
            #continue

        print(target_company_name)

        df_target_company = df_company_summary[df_company_summary['secCode'] == target_sec_code]
        submit_time_str_list = df_target_company['submitDateTime'].to_list()

        # 5年以上前のデータをリストから削除
        for index, submit_time_str in enumerate(submit_time_str_list):
            submit_date_str = submit_time_str.split(' ')[0].replace(' ', '')
            if(submit_date_str < str(TODAY + timedelta(days=-365*5))):
                submit_time_str_list.pop(index)

        # 各日付のxbrlを取得し、値取得
        for i, submit_time_str in enumerate(submit_time_str_list):
            submit_date_str = submit_time_str.split(' ')[0].replace(' ', '')

            df_doc_summary = download_all_documents(submit_date_str)

            # 返り値がFalseの場合continue
            if(type(df_doc_summary) == bool):
                continue

            target_row = df_doc_summary[df_doc_summary['secCode'] == str(int(target_sec_code))]

            # 文書IDと提出日を取得
            target_doc_id = target_row['docID'].values[0]
            target_date = target_row['submitDateTime'].values[0][:10]
            target_company = target_row['filerName'].values[0]

            try:
                df = Arelle(target_company_name, target_doc_id, target_code, industry_path)
            except Exception:
                print('............Error: Arelle')
                continue

            save_path = industry_path + '/' + str(target_code) + '_' + target_company_name + '/有価証券報告書/' + str(target_date) + '.csv'
            df.to_csv(save_path, encoding="utf-8", index=False)

#df_doc_summary_all.to_csv(OUTPUT_PAHT + 'test0628.csv')
