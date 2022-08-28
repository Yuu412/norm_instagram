#コンテクストID
CONTEXT_REF = {
    '現在': [
        'CurrentYearDuration',
        'CurrentYearInstant',
        'CurrentYearInstant_NonConsolidatedMember',
        'CurrentYearDuration_NonConsolidatedMember',
        'CurrentYearDuration_jpcrp030000-asr_E00678-000PersonalCareReportableSegmentMember',
        'FilingDateInstant',
    ],
    '1年前': [
        'Prior1YearDuration',
        'Prior1YearInstant',
        'Prior1YearDuration_NonConsolidatedMember',
        'Prior1YearInstant_NonConsolidatedMember',
    ],
    '2年前': [
        'Prior2YearDuration',
        'Prior2YearInstant',
        'Prior2YearDuration_NonConsolidatedMember',
        'Prior2YearInstant_NonConsolidatedMember',
    ],
    '3年前': [
        'Prior3YearDuration',
        'Prior3YearInstant',
        'Prior3YearDuration_NonConsolidatedMember',
        'Prior3YearInstant_NonConsolidatedMember',
    ],
    '4年前': [
        'Prior4YearDuration',
        'Prior4YearInstant',
        'Prior4YearDuration_NonConsolidatedMember',
        'Prior4YearInstant_NonConsolidatedMember',
    ],
}

#提出日
FILING_DATE = [
    'FilingDateCoverPage',
]

#売上高
NET_SALES = [
    #[売上高]
    'NetSales',
    'NetSalesSummaryOfBusinessResults',
    'OperatingRevenue1',
    'ShippingBusinessRevenueWAT',
    'ShippingBusinessRevenueAndOtherOperatingRevenueWAT',
    'ShippingBusinessRevenueAndOtherServiceRevenueWAT',
    'OperatingRevenueELE',
    'OperatingRevenueRWY',
    'OperatingRevenueSEC',
    'ContractsCompletedRevOA',
    'NetSalesNS',
    'PLJHFDAKJHGF',
    'SalesAllSegments',
    'SalesDetails',
    'TotalSales',
    'SalesAndOtherOperatingRevenueSummaryOfBusinessResults',
    'NetSalesAndOtherOperatingRevenueSummaryOfBusinessResults',
    'NetSalesAndServiceRevenueSummaryOfBusinessResults',
    'NetSalesAndOperatingRevenueSummaryOfBusinessResults',
    'NetSalesAndOperatingRevenue2SummaryOfBusinessResults',
    'NetSalesAndOperatingRevenue',
    #[製品売上高]
    'NetSalesOfFinishedGoodsRevOA',
    #[商品及び製品売上高]
    'NetSalesOfMerchandiseAndFinishedGoodsRevOA',
    #[売上高_USGAAP]
    'RevenuesUSGAAPSummaryOfBusinessResults',
    #[売上高_IFRS]
    'NetSalesIFRSSummaryOfBusinessResults',
    'TotalTradingTransactionIFRSSummaryOfBusinessResults',
    'TotalTradingTransactionsIFRSSummaryOfBusinessResults',
    #[売上収益_IFRS]
    'Revenue',
    'RevenueIFRSSummaryOfBusinessResults',
    'RevenueSummaryOfBusinessResults',
    #[営業収入]
    'OperatingRevenue2',
    'OperatingRevenue2SummaryOfBusinessResults',
    #[営業総収入]
    'GrossOperatingRevenue',
    'GrossOperatingRevenueSummaryOfBusinessResults',
    #[作業収入]
    'NetSalesRevOA',
    #[保険料等収入]
    'InsurancePremiumsAndOtherOIINS',
    'PremiumAndOtherIncomeSummaryOfBusinessResults',
    'InsurancePremiumsAndOtherIncomeSummaryOfBusinessResults',
    'InsurancePremiumsAndOthersSummaryOfBusinessResults',
    'InsurancePremiumsAndOtherSummaryOfBusinessResults',
    #[チェーン全店売上高]
    'WholeChainStoreSalesSummaryOfBusinessResults',
    #[完成工事高]
    'NetSalesOfCompletedConstructionContractsCNS',
    'NetSalesOfCompletedConstructionContractsSummaryOfBusinessResults',
    #[完成業務高]
    'ContractsCompletedSummaryOfBusinessResults',
    #[営業収益]
    'RentIncomeOfRealEstateRevOA',
    'OperatingRevenueSPF',
    'OperatingRevenueIVT',
    'OperatingRevenueCMD',
    'OperatingRevenueOILTelecommunications',
    'OperatingRevenue1SummaryOfBusinessResults',
    #[経常収益]
    'OrdinaryIncomeBNK',
    'OperatingIncomeINS',
    'OrdinaryIncomeSummaryOfBusinessResults',
    #[事業収益]
    'BusinessRevenues',
    'BusinessRevenue',
    'BusinessRevenueRevOA',
    'OperatingRevenue',
    'SummaryOfSalesBusinessResults',
    'OperatingRevenuesSummaryOfBusinessResults',
    'BusinessRevenueSummaryOfBusinessResults',
    'OperatingRevenueSummaryOfBusinessResults',
]

#利益
PROFIT = [
    #[事業利益]
    'BusinessProfitIFRSSummaryOfBusinessResults',
    #[売上総利益_IFRS]
    'GrossProfitLossIFRSSummaryOfBusinessResults',
    #[営業利益]
    'OperatingIncome',
    'ProfitLossFromOperatingActivities',
    'OperatingIncomeLoss',
    #[営業利益_USGAAP]
    'OperatingIncomeLossUSGAAPSummaryOfBusinessResults',
    #[営業利益_IFRS]
    'OperatingProfitLossIFRSSummaryOfBusinessResults',
    'OperatingProfitIFRSSummaryOfBusinessResults',
    'OperatingIncomeLossIFRSSummaryOfBusinessResults',
    'OperatingIncomeIFRSSummaryOfBusinessResults',
    #[経常利益]
    'OrdinaryIncome',
    'OrdinaryIncomeLossSummaryOfBusinessResults',
    #[税金等調整前純利益]
    'IncomeBeforeIncomeTaxes',
    #[税金等調整前純利益_USGAAP]
    'ProfitLossBeforeTaxUSGAAPSummaryOfBusinessResults',
    #[税引前利益_IFRS]
    'ProfitLossBeforeTaxIFRSSummaryOfBusinessResults',
    #[純利益]
    'NetIncome',
    'ProfitLoss',
    'NetIncomeLossSummaryOfBusinessResults',
    #[純剰余]
    'NetSurplus',
    #[利益_IFRS]
    'ProfitLossIFRSSummaryOfBusinessResults',
    #[親会社の所有者に帰属する利益]
    'ProfitLossAttributableToOwnersOfParent',
    'ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults',
    'ProfitLossAndAttributableToOwnersOfParent',
    #[当社株主に帰属する当期純利益_USGAAP]
    'NetIncomeLossAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
    #[親会社の所有者に帰属する利益_IFRS]
    'ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
    #[包括利益]
    'ComprehensiveIncome',
    'ComprehensiveIncomeSummaryOfBusinessResults',
    #[包括利益_USGAAP]
    'ComprehensiveIncomeUSGAAPSummaryOfBusinessResults',
    #[当社株主帰属包括利益_USGAAP]
    'ComprehensiveIncomeAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
    #[親会社株主に帰属する包括利益_IFRS]
    'ComprehensiveIncomeIFRSSummaryOfBusinessResults',
    'ComprehensiveIncomeAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
    #[事業収益]
    'BusinessRevenues',
    'BusinessRevenue',
    'BusinessRevenueRevOA',
    'OperatingRevenue',
    'SummaryOfSalesBusinessResults',
    'OperatingRevenuesSummaryOfBusinessResults',
    'BusinessRevenueSummaryOfBusinessResults',
    'OperatingRevenueSummaryOfBusinessResults',
]

#当期純利益
NET_INCOME = [
    'NetIncomeLossSummaryOfBusinessResults',
]

#資産
ASSET = [
    #[資産]
    'Assets',
    'TotalAssets',
    'TotalAssetsSummaryOfBusinessResults',
    #[資産_USGAAP]
    'TotalAssetsUSGAAPSummaryOfBusinessResults',
    #[資産_IFRS]
    'TotalAssetsIFRSSummaryOfBusinessResults',
    #[負債]
    'Liabilities',
    #[純資産]
    'NetAssets',
    'NetAssetsSummaryOfBusinessResults',
    #[純資産_USGAAP]
    'EquityIncludingPortionAttributableToNonControllingInterestUSGAAPSummaryOfBusinessResults',
    #[資本]
    'Equity',
    #[資本_IFRS]
    'TotalEquityIFRSSummaryOfBusinessResults',
    '[親会社の所有者に帰属する持分]',
    'EquityAttributableToOwnersOfParent',
    '[親会社の所有者に帰属する持分_IFRS]',
    'EquityAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
    #[流動資産]
    'CurrentAssets',
    #[固定資産]
    'NoncurrentAssets',
    #[流動負債]
    'CurrentLiabilities',
    #[固定負債]
    'NoncurrentLiabilities',
    #[資本金]
    'CapitalStock',
    'IssuedCapital',
    'CapitalStockSummaryOfBusinessResults',
    #[出資金]
    'CapitalStockShinkinBNK',
    #[基金]
    'FoundationFunds',
    #[資本剰余金]
    'CapitalSurplus',
    'SharePremium',
    #[利益剰余金]
    'RetainedEarnings',
    #[連結剰余金]
    'ConsolidatedSurplus',
    #[株主資本]
    'ShareholdersEquity',
    'EquityAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
    #[その他の包括利益累計額]
    'ValuationAndTranslationAdjustments',
]

#営業活動によるキャッシュ・フロー
CF_SALES = [
    #[営業CF]
    'NetCashProvidedByUsedInOperatingActivities',
    'CashFlowsFromUsedInOperatingActivities',
    'NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults',
    #[営業CF_USGAAP]
    'CashFlowsFromUsedInOperatingActivitiesUSGAAPSummaryOfBusinessResults',
    #[営業CF_IFRS]
    'CashFlowsFromUsedInOperatingActivitiesIFRSSummaryOfBusinessResults',
]

#投資活動によるキャッシュ・フロー
CF_INVESTMENT = [
    #[投資CF]
    'NetCashProvidedByUsedInInvestmentActivities',
    'CashFlowsFromUsedInInvestingActivities',
    'NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults',
    #[投資CF_USGAAP]
    'CashFlowsFromUsedInInvestingActivitiesUSGAAPSummaryOfBusinessResults',
    #[投資CF_IFRS]
    'CashFlowsFromUsedInInvestingActivitiesIFRSSummaryOfBusinessResults',
]

#現金及び現金同等物の期末残高
CASH_BALANCE = [
    #[現金及び現金同等物の期末残高]
    'CashAndCashEquivalents',
    'CashAndCashEquivalentsSummaryOfBusinessResults',
    #[現金及び現金同等物の期末残高_USGAAP]
    'CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults',
    #[現金及び現金同等物の期末残高_IFRS]
    'CashAndCashEquivalentsIFRSSummaryOfBusinessResults',
]

#発行済株式数
STOCK_NUMBER = [
    #[発行済株式総数]
    'TotalNumberOfIssuedSharesSummaryOfBusinessResults',
    #[AA型種類株式_発行済株式総数]
    'TotalNumberOfIssuedSharesModelAAClassSharesSummaryOfBusinessResults',
    #[大株主所有株式数]
    'NumberOfSharesHeld',
    #[大株主所有割合]
    'ShareholdingRatio',
]

#従業員数
EMPLOYEES = [
    'NumberOfEmployees',
    'NumberOfEmployeesIFRSSummaryOfBusinessResults',
]

#自己資本比率
CAPITAL_RATIO = [
    #[自己資本比率]
    'EquityToAssetRatioSummaryOfBusinessResults',
    #[株主資本比率_USGAAP]
    'EquityToAssetRatioUSGAAPSummaryOfBusinessResults',
    #[持分比率_IFRS]
    'RatioOfOwnersEquityToGrossAssetsIFRSSummaryOfBusinessResults',
]

#ROE(自己資本利益率)
ROE = [
    #[自己資本利益率]
    'RateOfReturnOnEquitySummaryOfBusinessResults',
    #[株主資本利益率_USGAAP]
    'RateOfReturnOnEquityUSGAAPSummaryOfBusinessResults',
    'NetIncomeToSalesBelongingToShareholdersSummaryOfBusinessResults',
    #[持分利益率_IFRS]
    'RateOfReturnOnEquityIFRSSummaryOfBusinessResults',    
]

#[平均臨時雇用者数]
#AverageNumberOfTemporaryWorkers
#AverageNumberOfTemporaryWorkersIFRSSummaryOfBusinessResults # 平均臨時雇用者数 E00518 RIZAPｸﾞﾙｰﾌﾟ株式会社

#EPS(１株当たり純利益)
EPS = [
    #[EPS]
    'BasicEarningsLossPerShareSummaryOfBusinessResults',
    #[EPS_USGAAP]
    'BasicEarningsLossPerShareUSGAAPSummaryOfBusinessResults',
    #[EPS_IFRS]
    'BasicEarningsLossPerShareIFRSSummaryOfBusinessResults', 
]

#PER(株価収益率)
PER = [
    #[PER]
    'PriceEarningsRatioSummaryOfBusinessResults',
    #[PER_USGAAP]
    'PriceEarningsRatioUSGAAPSummaryOfBusinessResults',
    #[PER_IFRS]
    'PriceEarningsRatioIFRSSummaryOfBusinessResults',
]

#BPS(１株当たり純資産)
BPS = [
    #[BPS]
    'NetAssetsPerShareSummaryOfBusinessResults',
    #[BPS_USGAAP]
    'EquityAttributableToOwnersOfParentPerShareUSGAAPSummaryOfBusinessResults',
    #[BPS_IFRS]
    'EquityToAssetRatioIFRSSummaryOfBusinessResults',
]

#平均年間給与
AVERAGE_SALARY = [
    'AverageAnnualSalaryInformationAboutReportingCompanyInformationAboutEmployees',
]

#平均勤続年数
AVERAGE_WORK_PERIOD = [
    'AverageLengthOfServiceYearsInformationAboutReportingCompanyInformationAboutEmployees',
]

#平均年齢
AVERAGE_AGE = [
    'AverageAgeYearsInformationAboutReportingCompanyInformationAboutEmployees',
]

#研究開発費
RD_COST = [
    'ResearchAndDevelopmentExpensesResearchAndDevelopmentActivities',
]

#設備投資額
FACILITY_COST = [
    'CapitalExpendituresOverviewOfCapitalExpendituresEtc',
]


# ===========================================
# ==== 以下メモ ==============================
# ===========================================

#キャッシュフロー
"""
CF = [
    #[財務CF]
    'NetCashProvidedByUsedInFinancingActivities',
    'CashFlowsFromUsedInFinancingActivities',
    'NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults',
    #[財務CF_USGAAP]
    'CashFlowsFromUsedInFinancingActivitiesUSGAAPSummaryOfBusinessResults',
    #[財務CF_IFRS]
    'CashFlowsFromUsedInFinancingActivitiesIFRSSummaryOfBusinessResults',

    #[利益剰余金]
    'RetainedEarnings',
    #[連結剰余金]
    'ConsolidatedSurplus',
    #[株主資本]
    'ShareholdersEquity',
    'EquityAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
    #[その他の包括利益累計額]
    'ValuationAndTranslationAdjustments',
]
"""


#潜在株式調整後ＥＰＳ
"""
[潜在株式調整後EPS]
DilutedEarningsPerShareSummaryOfBusinessResults # 潜在株式調整後１株当たり当期純利益 E00012 株式会社極洋
[希薄化後EPS_USGAAP]
DilutedEarningsLossPerShareUSGAAPSummaryOfBusinessResults # 希薄化後１株当たり当社株主に帰属する当期純利益 E00334 日本ﾊﾑ株式会社
[希薄化後EPS_IFRS]
DilutedEarningsLossPerShareIFRSSummaryOfBusinessResults # 希薄化後１株当たり当期利益 E01807 日本電波工業株式会社
"""

#１株当たり配当
"""
[1株当たり配当]
DividendPaidPerShareSummaryOfBusinessResults # １株当たり配当額 E00012 株式会社極洋 # 普通株式 E02144 ﾄﾖﾀ自動車株式会社
[AA型種類株式_1株当たり配当]
DividendPaidPerShareFirstSeriesModelAAClassSharesSummaryOfBusinessResults # １株当たり配当額 第１回ＡＡ型種類株式 E02144 ﾄﾖﾀ自動車株式会社
[1株当たり中間配当]
InterimDividendPaidPerShareSummaryOfBusinessResults # １株当たり中間配当額 E00012 株式会社極洋 # 普通株式 E02144 ﾄﾖﾀ自動車株式会社
[AA型種類株式_1株当たり中間配当]
InterimDividendPaidPerShareFirstSeriesModelAAClassSharesSummaryOfBusinessResults # １株当たり中間配当額 第１回ＡＡ型種類株式 E02144 ﾄﾖﾀ自動車株式会社
"""

