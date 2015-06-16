
課題１,2のソースコード：nxwiki_kai.py, nxwiki_kai4.py
        scipy.sparceを利用したコード（全データを利用に修正版）：nxwiki_kai7.py
	データベース上に各ページのページランク,ページID,順位を保存（rank, Id, pageRank）
	データベース上にページID、名前、存命人物の順位を保存（Id,Name,rank）
	nx, scipy.sparce による上位10名の名前をコンソール上に出力
	結果（nxwiki_kai7.py）
	1 笹峯愛
	2 高杢禎彦
	3 枝松克幸
	4 MIN-NARAKEN
	5 マルクス・アルベック
	6 タイロン・ウッズ
	7 椎名誠
	8 稲垣吾郎
	9 名取裕子
	10 十朱幸代
	

課題3のソースコード：service.py
	sqlファイル内のsql ファイルをまずは実行してください。
	その後、nxwiki.pyを実行し、リンクのデータベースを作ってください。
	上のことを実行後、python service.py とコンソール上でコマンドを打つことでサービスを利用できます。
jawiki-20150512-pagelinks.sql
jawiki-20150512-categorylinks.sql 
jawiki-20150512-page.sql
をwikipediaの公式サイトからとってきて、mysql上で
source jawiki-20150512-pagelinks.sql
source jawiki-20150512-categorylinks.sql 
source jawiki-20150512-page.sql

をする必要があります。