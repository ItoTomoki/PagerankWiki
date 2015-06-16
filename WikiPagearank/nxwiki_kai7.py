#coding: utf8
import mysql.connector
import MySQLdb
import numpy as np
import networkx as nx
import scipy.sparse.linalg
import scipy.sparse.linalg
from scipy.sparse import lil_matrix, csr_matrix

def get_pagerank(M, alpha=0.85, return_P=False):
    """
    calculate pagerank usding scipy.sparse.linalg
    Args:
        M: transition probability matrix
        alpha: damping factor
        return_P: whether to return P
    Returns:
        array of index in ascending order of PageRank
    """
    #n = len(M)
    #M = (np.ones([n, n]) * (1 - alpha) / n + alpha * M)
    la, v = scipy.sparse.linalg.eigs(M, k=1)
    P = v[:, 0]
    P /= P.sum()
    if return_P:
        return np.argsort(P)[-1::-1], P
    else:
        return np.argsort(P)[-1::-1]

#CREATE TABLE IdLink (Number_to INT,from_id INT, to_id INT, Number_from INT)ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
connector = MySQLdb.connect(host="localhost", db="wiki", user="root",passwd="", charset="utf8")
cursor = connector.cursor()

#sql = u"SELECT page_id FROM page  where page_namespace = 0 AND page_namespace = 0 AND page_counter > 0 ORDER BY page_counter Desc;"
sql = u"SELECT page_id FROM page  where page_namespace = 0 AND page_namespace = 0 ORDER BY page_counter Desc;"
#page_etsuransuu 大きい順
cursor.execute(sql)
Id_from = cursor.fetchall()
maxId  = len(Id_from) 
IdDict = {}
NumberDict = {}
Matrix = lil_matrix((maxId,maxId))
print maxId
j = 0
for id_from in Id_from:
	#print id_from[0]
	IdDict.update({id_from[0]:j}) #id からNumberを取得
	NumberDict.update({j:id_from[0]}) #Number からid を取得

	j = j + 1
j = 0
for id_from in Id_from:
	sql = "SELECT pl_title from pagelinks where pl_from =" + str(id_from[0]) + " AND pl_namespace = 0 AND pl_from_namespace = 0 ;"
	cursor.execute(sql)
	LinkNameList = cursor.fetchall()
	for i in LinkNameList:
		PageTitle =  str(i[0])
		PageTitle = PageTitle.replace('"','""')
		PageTitle = PageTitle.replace("'","''")
		if (PageTitle[-1] is "'\'"):
			PageTitle = PageTitle.replace("'\'","")
		sql = "SELECT page_id from page where page_title = " 
		sql += '"'
		sql +=  str(PageTitle) #str(i[0])
		sql += '"'  
		sql +=  " AND page_namespace = 0;"
				
		try:
			cursor.execute(sql)
			P = list(cursor.fetchall())
			if len(P) ==0:
				continue
			else:
				id_to = IdDict[P[0][0]]
				Matrix[id_to,id_from[0]] = 1.0/float(len(LinkNameList))
				
		except:
			continue
		
	j = j + 1
print j
#g.add_edge(IdDict[9462],IdDict[589960])
#g.add_edge(IdDict[295386],IdDict[21222])
"""
la, v = scipy.sparse.linalg.eigs(Matrix, k=1)
print 1
print v
"""
print "Rank | ID | p"
print "--get_pagerank--------------------"
r, p = get_pagerank(Matrix, alpha=0.85, return_P=True)
PageRankDict1 = {}
PageRankDict2 = {}
for i in range(len(r)):
	print "{0:4d} | {1:2d} | {2}".format(i+1, r[i]+1, p[r[i]])
	PageRankDict1.update({i:[NumberDict[r[i]],p[r[i]]]}) #ランク(0から):Id・ページランク
sql = ""
#PageRankのデータをデータベースに保存その１
#sql = 'Drop PageRankID'
#cursor.execute(sql)
#sql = 'CREATE TABLE PageRankID (rank INT,Id INT,pageRank FLOAT)ENGINE=InnoDB DEFAULT CHARSET=utf8 ;'
#cursor.execute(sql)
"""
for key in PageRankDict1.keys():
	kv = str(PageRankDict1[key][1]).replace('-0j','')
	rankNo = key + 1
	sql = 'Insert INTO PageRankID (Id,pageRank,rank) VALUES ('	
	sql += str(PageRankDict1[key][0])
	sql += ','
	sql += kv
	sql += ','
	sql += str(rankNo)
	sql += ');'
	cursor.execute(sql)
"""
#print PageRankDict1
#pr=nx.pagerank(g,alpha=0.85)
#prn=nx.pagerank_numpy(g,alpha=0.85)
#PageRankのデータをデータベースに保存その２
"""
sql = 'CREATE TABLE PageRankID2 (rank INT,Id INT,pageRank FLOAT)ENGINE=InnoDB DEFAULT CHARSET=utf8 ;'
cursor.execute(sql)
for key in PageRankDict2.keys():
	kv = str(PageRankDict2[key][1]).replace('-0j','')
	rankNo = key + 1
	sql = 'Insert INTO PageRankID2 (Id,pageRank,rank) VALUES ('	
	sql += str(PageRankDict2[key][0])
	sql += ','
	sql += kv
	sql += ','
	sql += str(rankNo)
	sql += ');'
	cursor.execute(sql)
"""
#namespace2のやつとかはlimkto しかなく、ネットワークには入っていないので除外してもよいと考えた
sql = 'select cl_from from categorylinks where cl_to = "存命人物"'
cursor.execute(sql)
HumanIdList = cursor.fetchall()
HumanIdlist = np.zeros([len(HumanIdList)])
k = 0
#人間の辞書作成
HumanNameDict = {}
HumanIdDict = {}
H = HumanIdlist[0]
for i in HumanIdList:
	i = i[0]
	sql = 'select page_title from page where page_id = '
	sql += (str(i))
	cursor.execute(sql)
	HumanName = cursor.fetchall()[0][0]
	HumanNameDict.update({i:HumanName})#HumanNameDict[id]で名前検索アンド人か判定
	HumanIdDict.update({HumanName:i}) #HumanIdDict[Name]で名前からidを求める
HumanRankingDict = {}
HumanRankingDict2 = {}

k = 1
for i in range(0,len(PageRankDict1)):
	try:
		HumanRankingDict.update({k:HumanNameDict[PageRankDict1[i][0]]})
		k = k + 1
	except:
		continue
#k = 151937
#課題２の結果の出力1
print "HUmanPageRanking Best10 by scipy.sparce:"
print "Ranking | Name"
print "--get_pagerank--------------------"
for i in range(1,11):
	print i,HumanRankingDict[i]

k = 1
#データベースに入れる.
#sql = 'CREATE TABLE HumanRankID (Id INT,Name VARCHAR, rank INT)ENGINE=InnoDB DEFAULT CHARSET=utf8 ;'
#cursor.execute(sql)
"""
for j in HumanRankingDict.keys():
	sql = 'Insert INTO HumanRankID (Id,Name,rank) VALUES ('
	sql += str(HumanIdDict[HumanRankingDict[j]])
	sql += ','
	sql += ('"' + str(HumanRankingDict[j]) + '"')
	sql += ','
	sql += str(j)
	sql += ');'
	#print sql
	cursor.execute(sql)	
"""
#connector.commit()
cursor.close()
connector.close()
