import glob
import math
from operator import index
import os
from queue import PriorityQueue
from edinet_xbrl.edinet_xbrl_parser import EdinetXbrlParser
import sys
import pandas as pd
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

INPUT_COLS = ['証券コード', '企業名', '安定性_1', '安定性_2', '安定性_3', '成長性_1', '成長性_2', '成長性_3', '収益性_1', '収益性_2', '収益性_3']
SUMMAEY_COLS = ['証券コード', '企業名', '安定性', '成長性', '収益性']
OUTPUT_COLS = ['証券コード', '企業名', '安定性_1', '安定性_2', '安定性_3', '成長性_1', '成長性_2', '成長性_3', '収益性_1', '収益性_2', '収益性_3', '安定性_1_ランク', '安定性_2_ランク', '安定性_3_ランク', '成長性_1_ランク', '成長性_2_ランク', '成長性_3_ランク', '収益性_1_ランク', '収益性_2_ランク', '収益性_3_ランク']
COLS = ['安定性', '成長性', '収益性']


# 業界名のcsv一覧を取得
indestry_csv_list = os.listdir(INPUT_PATH)
for industry_csv in indestry_csv_list:
    industry = industry_csv.replace('.csv', '')
    print(industry + ': START!!')

    if(industry == '.DS_Store'):
        continue

    input_filename = OUTPUT_PAHT + industry + '/company_score.csv'

    # スコアリストを読み込み
    df_score = pd.read_csv(input_filename, names=INPUT_COLS, encoding="utf-8", header=0)

    # データ数と同じランクが格納されたリスト
    rank_list = function.ret_rank_list(len(df_score))

    loop_cols = INPUT_COLS[2:]
    for col_name in loop_cols:
        df_score = df_score.sort_values(col_name)
        df_score[col_name + '_ランク'] = rank_list

    df_score.to_csv( OUTPUT_PAHT + industry + '/company_score_rank.csv', header=OUTPUT_COLS, encoding="utf-8", index=False)