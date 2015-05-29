#coding: utf8
import mysql.connector
import MySQLdb
import numpy as np
import networkx as nx
import scipy.sparse.linalg

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
    n = len(M)
    M += np.ones([n, n]) * alpha / n
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

sql = u"SELECT page_id FROM page  where page_namespace = 0 AND page_namespace = 0  ORDER BY page_counter Desc;"
#page_etsuransuu 大きい順
cursor.execute(sql)
Id_from = cursor.fetchall()
IdDict = {}
NumberDict = {}
#maxId  = 13617

j = 0
IDtoLenDict = {}
LinkToIDlist = {}
for id_from in Id_from:
	sql = "SELECT pagelinks.pl_from from pagelinks INNER JOIN page on pagelinks.pl_title = page.page_title "
	sql += "where page.page_id = "
	sql += str(id_from[0])
	sql += " AND page_namespace = 0;"
	try:
		cursor.execute(sql)
		LinkToIDList = cursor.fetchall()
		if len(LinkToIDList) > 100:
			IDtoLenDict.update({id_from[0]:LinkToIDlist})
			#print LinkToIDList
	except:
		continue
#データベースに入れる.
#sql = 'CREATE TABLE HumanRankID (Id INT,Name VARCHAR, rank INT)ENGINE=InnoDB DEFAULT CHARSET=utf8 ;'
#cursor.execute(sql)
	#50回以上リンクされていたら残す
	#id_from はリンク元のid
maxId  = len(IDtoLenDict.keys())
print maxId
Matrix = np.zeros([maxId,maxId])		
#print IDtoLenDict
g = nx.DiGraph()
number = 1
for k in IDtoLenDict.keys(): 
	IdDict.upload({number:k}) #number からid
	NumberDict.upload({k:number}) #id からNUmber
	g.add_node(number)
	number = number + 1
for k in IDtoLenDict.keys(): 
	for m in IDtoLenDict[k]:
		g.add_edge(NumberDict[m],NumberDict[k])
		Matrix[NumberDict[k]][NumberDict[m]]
print "OK"
Matrix = Matrix/np.sum(Matrix,axis = 0)

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
    n = len(M)
    M += np.ones([n, n]) * alpha / n
    la, v = scipy.sparse.linalg.eigs(M, k=1)
    P = v[:, 0]
    P /= np.sum(P,axis = 0)
    if return_P:
        return np.argsort(P)[-1::-1], P
    else:
        return np.argsort(P)[-1::-1]
print "Rank | ID | p"
print "--get_pagerank--------------------"
r, p = get_pagerank(Matrix, alpha=0.85, return_P=True)
PageRankDict1 = {}
for i in range(len(r)):
	print "{0:4d} | {1:2d} | {2}".format(i+1, r[i]+1, p[r[i]])
	PageRankDict1.update({i:[NumberDict[r[i]],p[r[i]]]})

"""
for key in PageRankDict1.keys():
	kv = str(PageRankDict1[key][1]).replace('-0j','')
	rankNo = key + 1
	sql = 'Insert INTO PageRankID2 (Id,pageRank,rank) VALUES ('	
	sql += str(PageRankDict1[key][0])
	sql += ','
	sql += kv
	sql += ','
	sql += str(rankNo)
	sql += ');'
	cursor.execute(sql)
"""

prc=nx.pagerank_scipy(g,alpha=0.85)
print 3
#print prc
PageRankDict2 = {}
n = 1
for k,v in sorted(prc.items(), key = lambda x:x[1]):
	PageRankDict2.update({n:[k,v]})
"""
for key in PageRankDict2.keys():
	kv = str(PageRankDict1[key][1]).replace('-0j','')
	rankNo = key + 1
	sql = 'Insert INTO PageRankID3 (Id,pageRank,rank) VALUES ('	
	sql += str(PageRankDict1[key][0])
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

k = 1
for i in range(0,len(PageRankDict1)):
	try:
		HumanRankingDict.update({k:HumanNameDict[PageRankDict1[i][0]]})
		k = k + 1
	except:
		continue
#k = 151937
for i in range(1,11):
	print i,HumanRankingDict[i]
#データベースに入れる.
sql = 'CREATE TABLE HumanRankID2 (Id INT,Name VARCHAR, rank INT)ENGINE=InnoDB DEFAULT CHARSET=utf8 ;'
cursor.execute(sql)
"""
for j in HumanRankingDict.keys():
	sql = 'Insert INTO HumanRankID2 (Id,Name,rank) VALUES ('
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
