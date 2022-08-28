from queue import PriorityQueue
import random

# 古いバージョン
def ret_rank(value):
    if(value >= 60):
        rank = 'S+'
    elif((value >= 58) & (value < 60)):
        rank = 'S'
    elif((value >= 56) & (value < 58)):
        rank = 'S-'
    elif((value >= 54) & (value < 56)):
        rank = 'A+'
    elif((value >= 52) & (value < 54)):
        rank = 'A'
    elif((value >= 50) & (value < 52)):
        rank = 'A-'
    elif((value >= 48) & (value < 50)):
        rank = 'B+'
    elif((value >= 46) & (value < 48)):
        rank = 'B'
    elif((value >= 44) & (value < 46)):
        rank = 'B-'
    elif((value >= 42) & (value < 44)):
        rank = 'C+'
    elif((value >= 40) & (value < 42)):
        rank = 'C'
    elif((value >= 38) & (value < 40)):
        rank = 'C-'
    elif(value < 38):
        rank = 'D'
    else:
        return '-'
    return rank

RANK_LIST = ['C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+', 'S-']
def ret_rank_list(len_df):
    rank_element_num_list = [(len_df + i) // len(RANK_LIST) for i in range(len(RANK_LIST))]
    random.shuffle(rank_element_num_list)
        
    rank_list = []
    for count, num in enumerate(rank_element_num_list):
        for i in range(0, num):
            rank_list.append(RANK_LIST[count])

    return rank_list

def upper_cut(value, upper):
    if(value > upper):
        return upper
    return value

def lower_cut(value, lower):
    if(value < lower):
        return lower
    return value

def ret_growth_rate(before, after):
    growth_rate = (after-before)/before

    return growth_rate

def calc_stability(df):
    stability_score_list = []
    for ago in range(0, 3):
        total_captal_ratio = 0
        total_cf_sales = 0
        total_net_sales = 0

        length = 3
        for i in range(0+ago, 3+ago):
            captal_ratio = df['自己資本比率_' + str(i)].values[0]
            cf_sales = df['営業CF_' + str(i)].values[0]
            net_sals = df['売上高_' + str(i)].values[0]

            if(captal_ratio == 0 or cf_sales == 0 or net_sals == 0):
                length -= 1
                continue

            total_captal_ratio += captal_ratio
            total_cf_sales += cf_sales
            total_net_sales += net_sals

        if(length < 1):
            return False
        
        ave_capital_ratio = upper_cut(total_captal_ratio / length, 0.5)

        ave_cf_sales = total_cf_sales / length
        ave_net_sals = total_net_sales / length
        ave_cs_per_ns = upper_cut(ave_cf_sales / ave_net_sals, 0.5)

        stability_score = (ave_capital_ratio)*0.4 + (ave_cs_per_ns)*0.6
        stability_score_list.append(stability_score)

    return stability_score_list
    
def calc_growth(df):
    growth_score_list = []
    for ago in range(0, 3):
        total_net_sales_growth_ratio = 0
        total_asset_growth_ratio = 0
        total_cash_balance_growth_ratio = 0
        
        length = 3
        for i in range(0+ago, 3+ago):
            j = 2 - i + ago
            if(i == 2 + ago):
                break

            prior_net_sals = df['売上高_' + str(j)].values[0]
            net_sals = df['売上高_' + str(j-1)].values[0]

            prior_asset = df['資産_' + str(j)].values[0]
            asset = df['資産_' + str(j-1)].values[0]

            prior_cash_balance = df['現金及び現金同等物の期末残高_' + str(j)].values[0]
            cash_balance = df['現金及び現金同等物の期末残高_' + str(j-1)].values[0]

            if(prior_net_sals == 0 or prior_asset == 0 or prior_cash_balance == 0):
                length -= 1
                continue

            net_sales_growth_ratio = ret_growth_rate(prior_net_sals, net_sals)
            asset_growth_ratio = ret_growth_rate(prior_asset, asset)
            cash_balance_growth_ratio = ret_growth_rate(prior_cash_balance, cash_balance)

            total_net_sales_growth_ratio += net_sales_growth_ratio
            total_asset_growth_ratio += asset_growth_ratio
            total_cash_balance_growth_ratio += cash_balance_growth_ratio
        
        if(length < 1):
            return False
            
        ave_net_sales_growth_ratio = upper_cut(total_net_sales_growth_ratio / length, 0.5)
        ave_asset_growth_ratio = upper_cut(total_asset_growth_ratio / length, 0.2)
        ave_cash_balance_growth_ratio = upper_cut(total_cash_balance_growth_ratio / length, 2)
        
        total_cb_per_ns = 0
        for i in range(0+ago, 3+ago):
            net_sals = df['売上高_' + str(i)].values[0]
            cf_investment = df['投資CF_' + str(i)].values[0]

            if(cash_balance == 0 or cf_investment == 0):
                length -= 1
                continue

            cb_per_ns = cf_investment/net_sals * -1
            total_cb_per_ns += cb_per_ns

        if(length < 1):
            return False
        ave_cb_per_ns = total_cb_per_ns / length
        
        # 上限・下限の設定
        ave_cb_per_ns = lower_cut(ave_cb_per_ns, -0.2)
        ave_cb_per_ns = upper_cut(ave_cb_per_ns, 0)

        item_1 = ave_net_sales_growth_ratio * 0.3
        item_2 = ave_asset_growth_ratio * 0.2
        item_3 = ave_cash_balance_growth_ratio * 0.2
        item_4 = ave_cb_per_ns * -0.3

        growth_score = (item_1 + item_2 + item_3 + item_4) * 100

        growth_score_list.append(growth_score)

    return growth_score_list

def calc_profitability(df):
    profitability_score_list = []
    for ago in range(0, 3):
        total_roa = 0
        length = 3
        for i in range(0+ago, 3+ago):
            net_income = df['当期純利益_' + str(i)].values[0]
            asset = df['資産_' + str(i)].values[0]

            if(net_income == 0 or asset == 0):
                length -= 1
                continue

            roa = net_income/asset*100
            total_roa += roa

        if(length < 1):
            return False
        
        profitability_score = upper_cut(total_roa / length, 10)
        profitability_score_list.append(profitability_score)
    
    return profitability_score_list