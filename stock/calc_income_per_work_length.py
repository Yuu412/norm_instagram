import glob
import math
from operator import index
import os
from queue import PriorityQueue
from edinet_xbrl.edinet_xbrl_parser import EdinetXbrlParser
import sys
import pandas as pd
import numpy as np
from pandas import read_csv
sys.path.append(r'F:\project\kabu\Arelle')
from arelle import Cntlr
import function

# path管理
INPUT_PATH = '../../output_stock/original_data/'
PREFIX = "jpcrp_cor"
INPUT_PATH = '../../input/'
OUTPUT_PAHT = "../../output/"

# 企業情報一覧の取得
DF_DOC_SUMMARY_ALL = read_csv('../../output_stock/summary.csv', header=0)

SUMMAEY_COLS = ['証券コード', '企業名', '平均年収', '平均勤続年数']
COLS = ['証券コード', '企業名', '平均勤続年数', '平均年収']

def calc_deviation(value, average, standard_deviation):
    deviation = (value - average) / standard_deviation * 10 + 50
    return deviation

# 平均点のcsvを取得
df_average = pd.read_csv(OUTPUT_PAHT + 'average_score.csv', encoding="utf-8")

# 標準偏差のcsvを取得
df_standard_deviation = pd.read_csv(OUTPUT_PAHT + 'standard_deviation.csv', encoding="utf-8")

# 業界名のcsv一覧を取得
indestry_csv_list = os.listdir(INPUT_PATH)
for industry_csv in indestry_csv_list:
    industry = industry_csv.replace('.csv', '')
    print(industry + ': START!!')

    if(industry == '.DS_Store'):
        continue

    industry_path = OUTPUT_PAHT + industry

    # 企業リストを読み込み
    input_filename = INPUT_PATH + '/' + industry_csv
    df_company = pd.read_csv(input_filename, names=['code', 'name'], encoding="utf-8")

    df_output = pd.DataFrame(data=[], columns=COLS)

    for index, company in df_company.iterrows():
        df_company_info = pd.DataFrame(index=[], columns=COLS)
        target_company_name = company['name']

        target_code = company['code']
        target_sec_code = target_code * 10

        target_dir = industry_path + '/' + str(target_code) + '_' + target_company_name 

        #if(os.path.exists(target_dir + '/score.csv')):
            #continue

        try:
            df_company = pd.read_csv(target_dir + '/stock_data.csv', encoding="utf-8") 
        except Exception:
            continue

        # 平均年収・平均年齢を取得
        ave_income = df_company['平均年収_0'].values[0]
        #ave_age = df_company['平均年齢_0'].values[0]
        ave_length = df_company['平均勤続年数_0'].values[0]
        
        if((ave_income == False) or (ave_length == False)):
            continue

        if(math.isnan(ave_income) or math.isnan(ave_length)):
            continue

        ave_income_digit = round(int(ave_income) / 10000)

        if(ave_income_digit > 3000):
            continue

        #if(np.any(np.isnan(stability_score_list) == True) or np.any(np.isnan(growth_score_list) == True) or np.any(np.isnan(profitability_score_list) == True)):
            #continue

        output_list = [
            target_code,
            target_company_name,
            ave_length,
            ave_income_digit,
        ]
        df_output = df_output.append(dict(zip(COLS, output_list)), ignore_index=True)
    df_output.to_csv(industry_path + '/income_per_work_length.csv', header=COLS, encoding="utf-8", index=False)