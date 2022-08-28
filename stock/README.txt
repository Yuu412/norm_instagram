1. 過去◯年分のドキュメント概要を取得
　→　get_xbrl_summary.py

2. 以下のステップ
　① 1.で保存した○年分のドキュメント一覧から、企業ごとに企業に合致するドキュメント一覧を抽出
　②そのドキュメントの提出日に報告されたドキュメント一覧を取得
　③ ②のそれぞれのxbrl形式のドキュメントをcsv(dataframe)に整形して保存
　→　get_stock_data.py

3. 2.で取得したcsv(dataframe)データのうち最新データから必要な情報を抽出（従業員数など1ドキュメントから1年分しか取れないデータは5年分取得）
　→ get_extract_data.py

4. 3.で作成したcsvから、業界ごとに安定性・成長性・収益性の平均値を求める
　→ calc_industry_score.py

5. 3.で作成したcsvからと、4.の平均値から、安定性・成長性・収益性のランクを生成
　→ calc_company_score.py

6. 平均年齢と平均年収の散布図
　→ calc_income_per_age.py

7. 安全性・成長性・収益性のグラフ作成
　→ make_stock_status_graph

8. 平均勤続年数と平均年収の散布図
　→　calc_income_per_work_length.py

9. 平均勤続年数と平均年収の散布図のグラフ化
