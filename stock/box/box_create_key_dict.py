import sys
import pandas as pd
sys.path.append(r'F:\project\kabu\Arelle')
from arelle import Cntlr

def main():
    #zip の中の『報告書インスタンス』のパスをくっつけます。
    xbrl_file = '/Users/yuu/develop/norm_automation/output_stock/original_data/2021-03-29/S100KUP1/XBRL/PublicDoc/jpcrp030000-asr-001_E00678-000_2020-12-31_01_2021-03-29.xbrl'

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
        # (出典) Cntlr.py
        ctrl.close()

    # あとは、作ったリストを csv や SQLite DB などに出力したり、
    # pandas.DataFrame などに変換したりして、分析していきます。

    cols = fact_datas[0]
    df = pd.DataFrame(index=[], columns=cols)

    for fact_data in fact_datas[1:-1]:
      # fact_data からdf に1行ずつ追加
      
      df = df.append(dict(zip(cols, fact_data)), ignore_index=True)

    df.to_csv('tmp.csv', header=cols, encoding="utf-8", index=False)

    return


if __name__ == '__main__':
    main()