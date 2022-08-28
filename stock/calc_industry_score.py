import glob
import math
from operator import index
import os
from queue import PriorityQueue
from re import I
from edinet_xbrl.edinet_xbrl_parser import EdinetXbrlParser
import sys
import numpy as np
import pandas as pd
from pandas import read_csv
sys.path.append(r'F:\project\kabu\Arelle')
from arelle import Cntlr
import const
import function

# path管理
PREFIX = "jpcrp_cor"
INPUT_PATH = '../../input'
OUTPUT_PATH = "../../output/"

# 企業情報一覧の取得
DF_DOC_SUMMARY_ALL = read_csv('../../output_stock/summary.csv', header=0)

COLS = ['業界名', '安定性_1', '安定性_2', '安定性_3', '成長性_1', '成長性_2', '成長性_3', '収益性_1', '収益性_2', '収益性_3']

# 差の２乗を返却
def ret_scuared_difference(value, ave):
    difference = value - ave
    return difference * difference

df_industry_score = pd.DataFrame(index=[], columns=COLS)

# 業界名のcsv一覧を取得
indestry_csv_list = os.listdir(INPUT_PATH)
for industry_csv in indestry_csv_list:
    industry = industry_csv.replace('.csv', '')
    print(industry + ': START!!')

    if(industry == '.DS_Store'):
        continue

    industry_path = OUTPUT_PATH + industry

    # 企業リストを読み込み
    input_filename = INPUT_PATH + '/' + industry_csv
    df_company = pd.read_csv(input_filename, names=['code', 'name'], encoding="utf-8")

    total_stability_score_1 = 0
    total_stability_score_2 = 0
    total_stability_score_3 = 0
    total_growth_score_1 = 0
    total_growth_score_2 = 0
    total_growth_score_3 = 0
    total_profitability_score_1 = 0
    total_profitability_score_2 = 0
    total_profitability_score_3 = 0

    company_num = 0
    for index, company in df_company.iterrows():
        target_company_name = company['name']
        target_code = company['code']
        target_dir = industry_path + '/' + str(target_code) + '_' + target_company_name 

        #if(os.path.exists(target_dir + '/score.csv')):
            #continue

        try:
            df_company = pd.read_csv(target_dir + '/stock_data.csv', encoding="utf-8") 
        except Exception:
            continue

        # 安定性・成長性・収益性を計算
        stability_score_list = function.calc_stability(df_company)
        growth_score_list = function.calc_growth(df_company)
        profitability_score_list = function.calc_profitability(df_company)

        if(isinstance(stability_score_list, bool) or isinstance(stability_score_list, bool) or isinstance(profitability_score_list, bool)):
            continue

        if(np.any(np.isnan(stability_score_list) == True) or np.any(np.isnan(growth_score_list) == True) or np.any(np.isnan(profitability_score_list) == True)):
            continue

        total_stability_score_1 += stability_score_list[0]
        total_stability_score_2 += stability_score_list[1]
        total_stability_score_3 += stability_score_list[2]

        total_growth_score_1 += growth_score_list[0]
        total_growth_score_2 += growth_score_list[1]
        total_growth_score_3 += growth_score_list[2]

        total_profitability_score_1 += profitability_score_list[0]
        total_profitability_score_2 += profitability_score_list[1]
        total_profitability_score_3 += profitability_score_list[2]

        company_num += 1

    if(company_num == 0):
        continue
    
    ave_stability_score_1 = total_stability_score_1 / company_num
    ave_stability_score_2 = total_stability_score_2 / company_num
    ave_stability_score_3 = total_stability_score_3 / company_num

    ave_growth_score_1 = total_growth_score_1 / company_num
    ave_growth_score_2 = total_growth_score_2 / company_num
    ave_growth_score_3 = total_growth_score_3 / company_num

    ave_profitability_score_1 = total_profitability_score_1 / company_num
    ave_profitability_score_2 = total_profitability_score_2 / company_num
    ave_profitability_score_3 = total_profitability_score_3 / company_num

    df_industry_score = df_industry_score.append(dict(zip(COLS, [
        industry, 
        ave_stability_score_1, ave_stability_score_2, ave_stability_score_3, 
        ave_growth_score_1, ave_growth_score_2, ave_growth_score_3, 
        ave_profitability_score_1, ave_profitability_score_2, ave_profitability_score_3
        ])), ignore_index=True)

df_industry_score.to_csv(OUTPUT_PATH + 'average_score.csv', header=COLS, encoding="utf-8", index=False)

# 業界ごとの標準偏差を
df_industry_standard_deviation = pd.DataFrame(index=[], columns=COLS)
# 業界名のcsv一覧を取得
for industry_csv in indestry_csv_list:
    industry = industry_csv.replace('.csv', '')
    print(industry + ': START!!')

    if(industry == '.DS_Store'):
        continue

    industry_path = OUTPUT_PATH + industry

    # 企業リストを読み込み
    input_filename = INPUT_PATH + '/' + industry_csv
    df_company = pd.read_csv(input_filename, names=['code', 'name'], encoding="utf-8")

    squared_difference_stability_score_1 = 0
    squared_difference_stability_score_2 = 0
    squared_difference_stability_score_3 = 0
    squared_difference_growth_score_1 = 0
    squared_difference_growth_score_2 = 0
    squared_difference_growth_score_3 = 0
    squared_difference_profitability_score_1 = 0
    squared_difference_profitability_score_2 = 0
    squared_difference_profitability_score_3 = 0

    for index, company in df_company.iterrows():
        target_company_name = company['name']
        target_code = company['code']
        target_dir = industry_path + '/' + str(target_code) + '_' + target_company_name 

        try:
            df_company = pd.read_csv(target_dir + '/stock_data.csv', encoding="utf-8") 
        except Exception:
            continue

        # 安定性・成長性・収益性を計算
        stability_score_list = function.calc_stability(df_company)
        growth_score_list = function.calc_growth(df_company)
        profitability_score_list = function.calc_profitability(df_company)

        if(isinstance(stability_score_list, bool) or isinstance(stability_score_list, bool) or isinstance(profitability_score_list, bool)):
            continue

        if(np.any(np.isnan(stability_score_list) == True) or np.any(np.isnan(growth_score_list) == True) or np.any(np.isnan(profitability_score_list) == True)):
            continue

        squared_difference_stability_score_1 += ret_scuared_difference(stability_score_list[0], ave_stability_score_1)
        squared_difference_stability_score_2 += ret_scuared_difference(stability_score_list[1], ave_stability_score_2)
        squared_difference_stability_score_3 += ret_scuared_difference(stability_score_list[2], ave_stability_score_3)
        squared_difference_growth_score_1 += ret_scuared_difference(growth_score_list[0], ave_growth_score_1)
        squared_difference_growth_score_2 += ret_scuared_difference(growth_score_list[1], ave_growth_score_2)
        squared_difference_growth_score_3 += ret_scuared_difference(growth_score_list[2], ave_growth_score_3)
        squared_difference_profitability_score_1 += ret_scuared_difference(profitability_score_list[0], ave_profitability_score_1)
        squared_difference_profitability_score_2 += ret_scuared_difference(profitability_score_list[1], ave_profitability_score_2)
        squared_difference_profitability_score_3 += ret_scuared_difference(profitability_score_list[2], ave_profitability_score_3)

        
    if(company_num == 0):
        continue

    # 標準偏差を求める
    standard_deviation_stability_score_1 = math.sqrt(squared_difference_stability_score_1)
    standard_deviation_stability_score_2 = math.sqrt(squared_difference_stability_score_2)
    standard_deviation_stability_score_3 = math.sqrt(squared_difference_stability_score_3)
    standard_deviation_growth_score_1 = math.sqrt(squared_difference_growth_score_1)
    standard_deviation_growth_score_2 = math.sqrt(squared_difference_growth_score_2)
    standard_deviation_growth_score_3 = math.sqrt(squared_difference_growth_score_3)
    standard_deviation_profitability_score_1 = math.sqrt(squared_difference_profitability_score_1)
    standard_deviation_profitability_score_2 = math.sqrt(squared_difference_profitability_score_2)
    standard_deviation_profitability_score_3 = math.sqrt(squared_difference_profitability_score_3)

    df_industry_standard_deviation = df_industry_standard_deviation.append(dict(zip(COLS, [
        industry, 
        standard_deviation_stability_score_1, standard_deviation_stability_score_2, standard_deviation_stability_score_3, 
        standard_deviation_growth_score_1, standard_deviation_growth_score_2, standard_deviation_growth_score_3, 
        standard_deviation_profitability_score_1, standard_deviation_profitability_score_2, standard_deviation_profitability_score_3
        ])), ignore_index=True)

df_industry_standard_deviation.to_csv(OUTPUT_PATH + 'standard_deviation.csv', header=COLS, encoding="utf-8", index=False)
