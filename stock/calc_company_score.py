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

SUMMAEY_COLS = ['証券コード', '企業名', '安定性_1', '安定性_2', '安定性_3', '成長性_1', '成長性_2', '成長性_3', '収益性_1', '収益性_2', '収益性_3', '安定性_順位', '成長性_順位', '収益性_順位']
COLS = ['安定性_1', '安定性_2', '安定性_3', '成長性_1', '成長性_2', '成長性_3', '収益性_1', '収益性_2', '収益性_3']
ITEM_LIST = ['安定性', '成長性', '収益性']

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

    df_summary_output = pd.DataFrame(data=[], columns=SUMMAEY_COLS)

    # 業界ごとの各平均値
    industry_stability_average_1 = df_average[df_average['業界名'] == industry]['安定性_1'].values[0]
    industry_stability_average_2 = df_average[df_average['業界名'] == industry]['安定性_2'].values[0]
    industry_stability_average_3 = df_average[df_average['業界名'] == industry]['安定性_3'].values[0]
    industry_growth_average_1 = df_average[df_average['業界名'] == industry]['成長性_1'].values[0]
    industry_growth_average_2 = df_average[df_average['業界名'] == industry]['成長性_2'].values[0]
    industry_growth_average_3 = df_average[df_average['業界名'] == industry]['成長性_3'].values[0]
    industry_profitability_average_1 = df_average[df_average['業界名'] == industry]['収益性_1'].values[0]
    industry_profitability_average_2 = df_average[df_average['業界名'] == industry]['収益性_2'].values[0]
    industry_profitability_average_3 = df_average[df_average['業界名'] == industry]['収益性_3'].values[0]

    # 業界ごとの各標準偏差
    industry_stability_standard_deviation_1 = df_standard_deviation[df_standard_deviation['業界名'] == industry]['安定性_1'].values[0]
    industry_stability_standard_deviation_2 = df_standard_deviation[df_standard_deviation['業界名'] == industry]['安定性_2'].values[0]
    industry_stability_standard_deviation_3 = df_standard_deviation[df_standard_deviation['業界名'] == industry]['安定性_3'].values[0]
    industry_growth_standard_deviation_1 = df_standard_deviation[df_standard_deviation['業界名'] == industry]['成長性_1'].values[0]
    industry_growth_standard_deviation_2 = df_standard_deviation[df_standard_deviation['業界名'] == industry]['成長性_2'].values[0]
    industry_growth_standard_deviation_3 = df_standard_deviation[df_standard_deviation['業界名'] == industry]['成長性_3'].values[0]
    industry_profitability_standard_deviation_1 = df_standard_deviation[df_standard_deviation['業界名'] == industry]['収益性_1'].values[0]
    industry_profitability_standard_deviation_2 = df_standard_deviation[df_standard_deviation['業界名'] == industry]['収益性_2'].values[0]
    industry_profitability_standard_deviation_3 = df_standard_deviation[df_standard_deviation['業界名'] == industry]['収益性_3'].values[0]

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

        # 安定性・成長性・収益性を計算
        stability_score_list = function.calc_stability(df_company)
        growth_score_list = function.calc_growth(df_company)
        profitability_score_list = function.calc_profitability(df_company)

        if(isinstance(stability_score_list, bool) or isinstance(stability_score_list, bool) or isinstance(profitability_score_list, bool)):
            continue

        if(np.any(np.isnan(stability_score_list) == True) or np.any(np.isnan(growth_score_list) == True) or np.any(np.isnan(profitability_score_list) == True)):
            continue

        # 偏差値の算出
        stability_deviation_1 = round(calc_deviation(stability_score_list[0], industry_stability_average_1 ,industry_stability_standard_deviation_1), 3)
        stability_deviation_2 = round(calc_deviation(stability_score_list[1], industry_stability_average_2 ,industry_stability_standard_deviation_2), 3)
        stability_deviation_3 = round(calc_deviation(stability_score_list[2], industry_stability_average_3 ,industry_stability_standard_deviation_3), 3)
        growth_deviation_1 = round(calc_deviation(growth_score_list[0], industry_growth_average_1 ,industry_growth_standard_deviation_1), 3)
        growth_deviation_2 = round(calc_deviation(growth_score_list[1], industry_growth_average_2 ,industry_growth_standard_deviation_2), 3)
        growth_deviation_3 = round(calc_deviation(growth_score_list[2], industry_growth_average_3 ,industry_growth_standard_deviation_3), 3)
        profitability_deviation_1 = round(calc_deviation(profitability_score_list[0], industry_profitability_average_1 ,industry_profitability_standard_deviation_1), 3)
        profitability_deviation_2 = round(calc_deviation(profitability_score_list[1], industry_profitability_average_2 ,industry_profitability_standard_deviation_2), 3)
        profitability_deviation_3 = round(calc_deviation(profitability_score_list[2], industry_profitability_average_3 ,industry_profitability_standard_deviation_3), 3)

        output_list = [
            str(stability_deviation_1),
            str(stability_deviation_2),
            str(stability_deviation_3),
            str(growth_deviation_1),
            str(growth_deviation_2),
            str(growth_deviation_3),
            str(profitability_deviation_1),
            str(profitability_deviation_2),
            str(profitability_deviation_3),
        ]
        
        df_output = pd.DataFrame(data=[output_list], columns=COLS)
        df_output.to_csv(target_dir + '/score.csv', header=COLS, encoding="utf-8", index=False)

        # ランクを同時表示（ランク：人為的閾値）
        summary_list = [
            target_code,
            target_company_name, 
            round(stability_deviation_1 + 4 * (stability_deviation_1 - 50) + 30, 3),
            round(stability_deviation_2 + 4 * (stability_deviation_2 - 50) + 30, 3),
            round(stability_deviation_3 + 4 * (stability_deviation_3 - 50) + 30, 3),
            round(growth_deviation_1 + 4 * (stability_deviation_1 - 50) + 30, 3),
            round(growth_deviation_2 + 4 * (stability_deviation_2 - 50) + 30, 3),
            round(growth_deviation_3 + 4 * (stability_deviation_3 - 50) + 30, 3),
            round(profitability_deviation_1 + 4 * (stability_deviation_1 - 50) + 30, 3),
            round(profitability_deviation_2 + 4 * (stability_deviation_2 - 50) + 30, 3),
            round(profitability_deviation_3 + 4 * (stability_deviation_3 - 50) + 30, 3),
            stability_deviation_1 + stability_deviation_2 + stability_deviation_3,
            growth_deviation_1 + growth_deviation_2 + growth_deviation_3,
            profitability_deviation_1 + profitability_deviation_2 + profitability_deviation_3
        ]
        df_summary_output = df_summary_output.append(dict(zip(SUMMAEY_COLS, summary_list)), ignore_index=True)

    # 1 ~ len(df)までの数字列を作成
    serial_num = pd.RangeIndex(start=1, stop=len(df_summary_output.index) + 1, step=1)
    for item in ITEM_LIST:
        df_summary_output = df_summary_output.sort_values(item + '_順位', ascending=False)
        df_summary_output[item + '_順位'] = serial_num
    
    df_summary_output.to_csv(industry_path + '/company_score.csv', header=SUMMAEY_COLS, encoding="utf-8", index=False)