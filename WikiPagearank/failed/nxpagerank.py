# -*- coding: utf-8 -*-
import networkx as nx

#有向グラフのインスタンスを生成
g = nx.DiGraph()

#ノードを追加する ※ソーシャルグラフなら人がノードになることが多い
g.add_node(1)
g.add_node(2)
g.add_node(3)                                                                                                                     
g.add_node(4)
g.add_node(5)
g.add_node(6)
#分かりやすいように敢えての羅列形式

#ノード間の矢印を加えていく ※ソーシャルグラフなら友達関係やフォロー、いいね！など
g.add_edge(1,2)
g.add_edge(1,3)
g.add_edge(1,4)
g.add_edge(2,3)
g.add_edge(3,4)
g.add_edge(3,5)
g.add_edge(2,6)
g.add_edge(5,6)
g.add_edge(1,6)
#分かりやすいように敢えての羅列形式

#pagerank値の計算
pr=nx.pagerank(g,alpha=0.85)

#pagerank値の計算(numpyを利用)
prn=nx.pagerank_numpy(g,alpha=0.85)

#pagerank値の計算(scipyを利用)
prc=nx.pagerank_scipy(g,alpha=0.85)
for k,v in sorted(prc.items(), key = lambda x:x[1]):
	print k, v
#計算結果表示
print("-----pagerank-----")
print(pr)

print("-----pagerank(numpy)-----")
print(prn)

print("-----pagerank(scipy)-----")
print(prc)