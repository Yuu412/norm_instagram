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
import const

# path管理
INPUT_PATH = '../../output_stock/original_data/'
PREFIX = "jpcrp_cor"
INPUT_PATH = '../../input'
OUTPUT_PAHT = "../../output/"

# 企業情報一覧の取得
DF_DOC_SUMMARY_ALL = read_csv('../../output_stock/summary.csv', header=0)

COLS = [
    '証券コード',
    '企業名',
    '提出日',
    '売上高_0',
    '売上高_1',
    '売上高_2',
    '売上高_3',
    '売上高_4',
    '利益_0',
    '利益_1',
    '利益_2',
    '利益_3',
    '利益_4',
    '当期純利益_0',
    '当期純利益_1',
    '当期純利益_2',
    '当期純利益_3',
    '当期純利益_4', 
    'ROE_0',
    'ROE_1',
    'ROE_2',
    'ROE_3',
    'ROE_4',
    '自己資本比率_0',
    '自己資本比率_1',
    '自己資本比率_2',
    '自己資本比率_3',
    '自己資本比率_4',
    'PER_0',
    'PER_1',
    'PER_2',
    'PER_3',
    'PER_4',
    'BPS_0',
    'BPS_1',
    'BPS_2',
    'BPS_3',
    'BPS_4',
    'EPS_0',
    'EPS_1',
    'EPS_2',
    'EPS_3',
    'EPS_4',
    '資産_0',
    '資産_1',
    '資産_2',
    '資産_3',
    '資産_4',
    '従業員数_0',
    '従業員数_1',
    '従業員数_2',
    '従業員数_3',
    '従業員数_4',
    '営業CF_0',
    '営業CF_1',
    '営業CF_2',
    '営業CF_3',
    '営業CF_4',
    '投資CF_0',
    '投資CF_1',
    '投資CF_2',
    '投資CF_3',
    '投資CF_4',
    '財務CF_0',
    '財務CF_1',
    '財務CF_2',
    '財務CF_3',
    '財務CF_4',
    '現金及び現金同等物の期末残高_0',
    '現金及び現金同等物の期末残高_1',
    '現金及び現金同等物の期末残高_2',
    '現金及び現金同等物の期末残高_3',
    '現金及び現金同等物の期末残高_4',
    '平均勤続年数_0',
    '平均勤続年数_1',
    '平均勤続年数_2',
    '平均勤続年数_3',
    '平均年収_0',
    '平均年収_1',
    '平均年収_2',
    '平均年収_3',
    '平均年齢_0',
    '平均年齢_1',
    '平均年齢_2',
    '平均年齢_3',
    '研究開発費_0',
    '研究開発費_1',
    '研究開発費_2',
    '研究開発費_3',
    '設備投資額_0',
    '設備投資額_1', 
    '設備投資額_2', 
    '設備投資額_3', 
]

def ret_value(df, tag_list, context_ref_list):
    ## データの取得
    for tag in tag_list:
        for context_ref in context_ref_list: 
            value = df[(df['タグ'] == tag) & (df['コンテキストID'] == context_ref)]

            if not value.empty:
                #print(value['値'].values[0])
                return value['値'].values[0]

    #print('nothing')
    return False

#企業情報をそれぞれdfから参照し辞書にして返す
def ret_compnay_info_dict(code, company, df_xbrl, df_xbrl_prior1, df_xbrl_prior2, df_xbrl_prior3):
    #提出日
    prior0_filing_date = ret_value(df_xbrl, const.FILING_DATE, const.CONTEXT_REF['現在']).split(' ')[0]

    #売上高
    prior0_net_sales = ret_value(df_xbrl, const.NET_SALES, const.CONTEXT_REF['現在'])
    prior1_net_sales = ret_value(df_xbrl, const.NET_SALES, const.CONTEXT_REF['1年前'])
    prior2_net_sales = ret_value(df_xbrl, const.NET_SALES, const.CONTEXT_REF['2年前'])
    prior3_net_sales = ret_value(df_xbrl, const.NET_SALES, const.CONTEXT_REF['3年前'])
    prior4_net_sales = ret_value(df_xbrl, const.NET_SALES, const.CONTEXT_REF['4年前'])

    #営業利益
    prior0_profit = ret_value(df_xbrl, const.PROFIT, const.CONTEXT_REF['現在'])
    prior1_profit = ret_value(df_xbrl, const.PROFIT, const.CONTEXT_REF['1年前'])
    prior2_profit = ret_value(df_xbrl, const.PROFIT, const.CONTEXT_REF['2年前'])
    prior3_profit = ret_value(df_xbrl, const.PROFIT, const.CONTEXT_REF['3年前'])
    prior4_profit = ret_value(df_xbrl, const.PROFIT, const.CONTEXT_REF['4年前'])

    #当期純利益
    prior0_net_income = ret_value(df_xbrl, const.NET_INCOME, const.CONTEXT_REF['現在'])
    prior1_net_income = ret_value(df_xbrl, const.NET_INCOME, const.CONTEXT_REF['1年前'])
    prior2_net_income = ret_value(df_xbrl, const.NET_INCOME, const.CONTEXT_REF['2年前'])
    prior3_net_income = ret_value(df_xbrl, const.NET_INCOME, const.CONTEXT_REF['3年前'])
    prior4_net_income = ret_value(df_xbrl, const.NET_INCOME, const.CONTEXT_REF['4年前'])

    #ROE(自己資本利益率)
    prior0_ROE = ret_value(df_xbrl, const.ROE, const.CONTEXT_REF['現在'])
    prior1_ROE = ret_value(df_xbrl, const.ROE, const.CONTEXT_REF['1年前'])
    prior2_ROE = ret_value(df_xbrl, const.ROE, const.CONTEXT_REF['2年前'])
    prior3_ROE = ret_value(df_xbrl, const.ROE, const.CONTEXT_REF['3年前'])
    prior4_ROE = ret_value(df_xbrl, const.ROE, const.CONTEXT_REF['4年前'])

    #自己資本比率
    prior0_capital_ratio = ret_value(df_xbrl, const.CAPITAL_RATIO, const.CONTEXT_REF['現在'])
    prior1_capital_ratio = ret_value(df_xbrl, const.CAPITAL_RATIO, const.CONTEXT_REF['1年前'])
    prior2_capital_ratio = ret_value(df_xbrl, const.CAPITAL_RATIO, const.CONTEXT_REF['2年前'])
    prior3_capital_ratio = ret_value(df_xbrl, const.CAPITAL_RATIO, const.CONTEXT_REF['3年前'])
    prior4_capital_ratio = ret_value(df_xbrl, const.CAPITAL_RATIO, const.CONTEXT_REF['4年前'])

    #PER(株価収益率)
    prior0_PER = ret_value(df_xbrl, const.PER, const.CONTEXT_REF['現在'])
    prior1_PER = ret_value(df_xbrl, const.PER, const.CONTEXT_REF['1年前'])
    prior2_PER = ret_value(df_xbrl, const.PER, const.CONTEXT_REF['2年前'])
    prior3_PER = ret_value(df_xbrl, const.PER, const.CONTEXT_REF['3年前'])
    prior4_PER = ret_value(df_xbrl, const.PER, const.CONTEXT_REF['4年前'])

    #BPS(１株当たり純資産)
    prior0_BPS = ret_value(df_xbrl, const.BPS, const.CONTEXT_REF['現在'])
    prior1_BPS = ret_value(df_xbrl, const.BPS, const.CONTEXT_REF['1年前'])
    prior2_BPS = ret_value(df_xbrl, const.BPS, const.CONTEXT_REF['2年前'])
    prior3_BPS = ret_value(df_xbrl, const.BPS, const.CONTEXT_REF['3年前'])
    prior4_BPS = ret_value(df_xbrl, const.BPS, const.CONTEXT_REF['4年前'])

    #EPS(１株当たり純利益)
    prior0_EPS = ret_value(df_xbrl, const.EPS, const.CONTEXT_REF['現在'])
    prior1_EPS = ret_value(df_xbrl, const.EPS, const.CONTEXT_REF['1年前'])
    prior2_EPS = ret_value(df_xbrl, const.EPS, const.CONTEXT_REF['2年前'])
    prior3_EPS = ret_value(df_xbrl, const.EPS, const.CONTEXT_REF['3年前'])
    prior4_EPS = ret_value(df_xbrl, const.EPS, const.CONTEXT_REF['4年前'])

    #資産
    prior0_asset = ret_value(df_xbrl, const.ASSET, const.CONTEXT_REF['現在'])
    prior1_asset = ret_value(df_xbrl, const.ASSET, const.CONTEXT_REF['1年前'])
    prior2_asset = ret_value(df_xbrl, const.ASSET, const.CONTEXT_REF['2年前'])
    prior3_asset = ret_value(df_xbrl, const.ASSET, const.CONTEXT_REF['3年前'])
    prior4_asset = ret_value(df_xbrl, const.ASSET, const.CONTEXT_REF['4年前'])

    #従業員数
    prior0_employees = ret_value(df_xbrl, const.EMPLOYEES, const.CONTEXT_REF['現在'])
    prior1_employees = ret_value(df_xbrl, const.EMPLOYEES, const.CONTEXT_REF['1年前'])
    prior2_employees = ret_value(df_xbrl, const.EMPLOYEES, const.CONTEXT_REF['2年前'])
    prior3_employees = ret_value(df_xbrl, const.EMPLOYEES, const.CONTEXT_REF['3年前'])
    prior4_employees = ret_value(df_xbrl, const.EMPLOYEES, const.CONTEXT_REF['4年前'])

    #営業CF
    prior0_CF_sales = ret_value(df_xbrl, const.CF_SALES, const.CONTEXT_REF['現在'])
    prior1_CF_sales = ret_value(df_xbrl, const.CF_SALES, const.CONTEXT_REF['1年前'])
    prior2_CF_sales = ret_value(df_xbrl, const.CF_SALES, const.CONTEXT_REF['2年前'])
    prior3_CF_sales = ret_value(df_xbrl, const.CF_SALES, const.CONTEXT_REF['3年前'])
    prior4_CF_sales = ret_value(df_xbrl, const.CF_SALES, const.CONTEXT_REF['4年前'])

    #投資CF
    prior0_CF_investment = ret_value(df_xbrl, const.CF_INVESTMENT, const.CONTEXT_REF['現在'])
    prior1_CF_investment = ret_value(df_xbrl, const.CF_INVESTMENT, const.CONTEXT_REF['1年前'])
    prior2_CF_investment = ret_value(df_xbrl, const.CF_INVESTMENT, const.CONTEXT_REF['2年前'])
    prior3_CF_investment = ret_value(df_xbrl, const.CF_INVESTMENT, const.CONTEXT_REF['3年前'])
    prior4_CF_investment = ret_value(df_xbrl, const.CF_INVESTMENT, const.CONTEXT_REF['4年前'])

    #財務CF
    prior0_CF_finance = ret_value(df_xbrl, const.CF_INVESTMENT, const.CONTEXT_REF['現在'])
    prior1_CF_finance = ret_value(df_xbrl, const.CF_INVESTMENT, const.CONTEXT_REF['1年前'])
    prior2_CF_finance = ret_value(df_xbrl, const.CF_INVESTMENT, const.CONTEXT_REF['2年前'])
    prior3_CF_finance = ret_value(df_xbrl, const.CF_INVESTMENT, const.CONTEXT_REF['3年前'])
    prior4_CF_finance = ret_value(df_xbrl, const.CF_INVESTMENT, const.CONTEXT_REF['4年前'])

    #現金及び現金同等物の期末残高
    prior0_cash_balance = ret_value(df_xbrl, const.CASH_BALANCE, const.CONTEXT_REF['現在'])
    prior1_cash_balance = ret_value(df_xbrl, const.CASH_BALANCE, const.CONTEXT_REF['1年前'])
    prior2_cash_balance = ret_value(df_xbrl, const.CASH_BALANCE, const.CONTEXT_REF['2年前'])
    prior3_cash_balance = ret_value(df_xbrl, const.CASH_BALANCE, const.CONTEXT_REF['3年前'])
    prior4_cash_balance = ret_value(df_xbrl, const.CASH_BALANCE, const.CONTEXT_REF['4年前'])

    #平均勤続年数
    prior0_ave_work_period = ret_value(df_xbrl, const.AVERAGE_WORK_PERIOD, const.CONTEXT_REF['現在'])
    prior1_ave_work_period = ret_value(df_xbrl_prior1, const.AVERAGE_WORK_PERIOD, const.CONTEXT_REF['現在'])
    prior2_ave_work_period = ret_value(df_xbrl_prior2, const.AVERAGE_WORK_PERIOD, const.CONTEXT_REF['現在'])
    prior3_ave_work_period = ret_value(df_xbrl_prior3, const.AVERAGE_WORK_PERIOD, const.CONTEXT_REF['現在'])
    
    #平均年収
    prior0_ave_salary = ret_value(df_xbrl, const.AVERAGE_SALARY, const.CONTEXT_REF['現在'])
    prior1_ave_salary = ret_value(df_xbrl_prior1, const.AVERAGE_SALARY, const.CONTEXT_REF['現在'])
    prior2_ave_salary = ret_value(df_xbrl_prior2, const.AVERAGE_SALARY, const.CONTEXT_REF['現在'])
    prior3_ave_salary = ret_value(df_xbrl_prior3, const.AVERAGE_SALARY, const.CONTEXT_REF['現在'])

    #平均年齢
    prior0_ave_age = ret_value(df_xbrl, const.AVERAGE_AGE, const.CONTEXT_REF['現在'])
    prior1_ave_age = ret_value(df_xbrl_prior1, const.AVERAGE_AGE, const.CONTEXT_REF['現在'])
    prior2_ave_age = ret_value(df_xbrl_prior2, const.AVERAGE_AGE, const.CONTEXT_REF['現在'])
    prior3_ave_age = ret_value(df_xbrl_prior3, const.AVERAGE_AGE, const.CONTEXT_REF['現在'])
    
    #研究開発費
    prior0_rd_cost = ret_value(df_xbrl, const.RD_COST, const.CONTEXT_REF['現在'])
    prior1_rd_cost = ret_value(df_xbrl_prior1, const.RD_COST, const.CONTEXT_REF['現在'])
    prior2_rd_cost = ret_value(df_xbrl_prior2, const.RD_COST, const.CONTEXT_REF['現在'])
    prior3_rd_cost = ret_value(df_xbrl_prior3, const.RD_COST, const.CONTEXT_REF['現在'])

    #設備投資額
    prior0_facility_cost = ret_value(df_xbrl, const.FACILITY_COST, const.CONTEXT_REF['現在'])
    prior1_facility_cost = ret_value(df_xbrl_prior1, const.FACILITY_COST, const.CONTEXT_REF['現在'])
    prior2_facility_cost = ret_value(df_xbrl_prior2, const.FACILITY_COST, const.CONTEXT_REF['現在'])
    prior3_facility_cost = ret_value(df_xbrl_prior3, const.FACILITY_COST, const.CONTEXT_REF['現在'])

    dic_graph_parameter = {
        '証券コード': code,
        '企業名': company,
        '提出日': prior0_filing_date,
        '売上高_0': prior0_net_sales,
        '売上高_1': prior1_net_sales,
        '売上高_2': prior2_net_sales,
        '売上高_3': prior3_net_sales,
        '売上高_4': prior4_net_sales,
        '利益_0': prior0_profit,
        '利益_1': prior1_profit,
        '利益_2': prior2_profit,
        '利益_3': prior3_profit,
        '利益_4': prior4_profit,
        '当期純利益_0': prior0_net_income,
        '当期純利益_1': prior1_net_income,
        '当期純利益_2': prior2_net_income,
        '当期純利益_3': prior3_net_income,
        '当期純利益_4': prior4_net_income,
        'ROE_0': prior0_ROE,
        'ROE_1': prior1_ROE,
        'ROE_2': prior2_ROE,
        'ROE_3': prior3_ROE,
        'ROE_4': prior4_ROE,
        '自己資本比率_0': prior0_capital_ratio,
        '自己資本比率_1': prior1_capital_ratio,
        '自己資本比率_2': prior2_capital_ratio,
        '自己資本比率_3': prior3_capital_ratio,
        '自己資本比率_4': prior4_capital_ratio,
        'PER_0': prior0_PER,
        'PER_1': prior1_PER,
        'PER_2': prior2_PER,
        'PER_3': prior3_PER,
        'PER_4': prior4_PER,
        'BPS_0': prior0_BPS,
        'BPS_1': prior1_BPS,
        'BPS_2': prior2_BPS,
        'BPS_3': prior3_BPS,
        'BPS_4': prior4_BPS,
        'EPS_0': prior0_EPS,
        'EPS_1': prior1_EPS,
        'EPS_2': prior2_EPS,
        'EPS_3': prior3_EPS,
        'EPS_4': prior4_EPS,
        '資産_0': prior0_asset,
        '資産_1': prior1_asset,
        '資産_2': prior2_asset,
        '資産_3': prior3_asset,
        '資産_4': prior4_asset,
        '従業員数_0': prior0_employees,
        '従業員数_1': prior1_employees,
        '従業員数_2': prior2_employees,
        '従業員数_3': prior3_employees,
        '従業員数_4': prior4_employees,
        '営業CF_0': prior0_CF_sales,
        '営業CF_1': prior1_CF_sales,
        '営業CF_2': prior2_CF_sales,
        '営業CF_3': prior3_CF_sales,
        '営業CF_4': prior4_CF_sales,
        '投資CF_0': prior0_CF_investment,
        '投資CF_1': prior1_CF_investment,
        '投資CF_2': prior2_CF_investment,
        '投資CF_3': prior3_CF_investment,
        '投資CF_4': prior4_CF_investment,
        '財務CF_0': prior0_CF_finance,
        '財務CF_1': prior1_CF_finance,
        '財務CF_2': prior2_CF_finance,
        '財務CF_3': prior3_CF_finance,
        '財務CF_4': prior4_CF_finance,
        '現金及び現金同等物の期末残高_0': prior0_cash_balance,
        '現金及び現金同等物の期末残高_1': prior1_cash_balance,
        '現金及び現金同等物の期末残高_2': prior2_cash_balance,
        '現金及び現金同等物の期末残高_3': prior3_cash_balance,
        '現金及び現金同等物の期末残高_4': prior4_cash_balance,
        '平均勤続年数_0': prior0_ave_work_period,
        '平均勤続年数_1': prior1_ave_work_period,
        '平均勤続年数_2': prior2_ave_work_period,
        '平均勤続年数_3': prior3_ave_work_period,
        '平均年収_0': prior0_ave_salary,
        '平均年収_1': prior1_ave_salary,
        '平均年収_2': prior2_ave_salary,
        '平均年収_3': prior3_ave_salary,
        '平均年齢_0': prior0_ave_age,
        '平均年齢_1': prior1_ave_age,
        '平均年齢_2': prior2_ave_age,
        '平均年齢_3': prior3_ave_age,
        '研究開発費_0': prior0_rd_cost,
        '研究開発費_1': prior1_rd_cost,
        '研究開発費_2': prior2_rd_cost,
        '研究開発費_3': prior3_rd_cost,
        '設備投資額_0': prior0_facility_cost,
        '設備投資額_1': prior1_facility_cost,
        '設備投資額_2': prior2_facility_cost,
        '設備投資額_3': prior3_facility_cost,
    }

    return dic_graph_parameter

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

    for index, company in df_company.iterrows():
        df_company_info = pd.DataFrame(index=[], columns=COLS)
        target_company_name = company['name']

        print(target_company_name)

        target_code = company['code']
        target_sec_code = target_code * 10

        # すでにstock_data.csvが存在していた場合
        #if(os.path.exists(industry_path + '/' + str(target_code) + '_' + target_company_name + '/stock_data.csv')):
            #continue

        company_data_path = industry_path + '/' + str(target_code) + '_' + target_company_name + '/有価証券報告書/'
        company_data_csv_list = glob.glob(company_data_path + '*.csv')

        if(len(company_data_csv_list) < 4):
            continue
        
        # 日付順にソート（降順）
        company_data_csv_list.sort()

        try:
            df_company = pd.read_csv(company_data_path + company_data_csv_list[-1].split('/')[-1].replace('.csv', '') + '.csv', encoding="utf-8") 
        except Exception:
            continue
        
        df_company_prior1 = pd.read_csv(company_data_path + company_data_csv_list[-1].split('/')[-1].replace('.csv', '') + '.csv', encoding="utf-8")
        df_company_prior2 = pd.read_csv(company_data_path + company_data_csv_list[-2].split('/')[-1].replace('.csv', '') + '.csv', encoding="utf-8")
        df_company_prior3 = pd.read_csv(company_data_path + company_data_csv_list[-3].split('/')[-1].replace('.csv', '') + '.csv', encoding="utf-8")

        dict_target_company_info = ret_compnay_info_dict(target_code, target_company_name, df_company, df_company_prior1, df_company_prior2, df_company_prior3)

        df_company_info = df_company_info.append(dict_target_company_info, ignore_index=True)
        df_company_info.to_csv(industry_path + '/' + str(target_code) + '_' + target_company_name + '/stock_data.csv', header=COLS, encoding="utf-8", index=False)