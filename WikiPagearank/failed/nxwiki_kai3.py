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
maxId  = len(Id_from) 
IdDict = {}
NumberDict = {}
CounterDict = {}
#maxId  = 13617
#有向グラフのインスタンスを生成
#g = nx.DiGraph()
#for i in range(0,maxId):
	#g.add_node(i)
Matrix = np.zeros([maxId,maxId])
UseNumberList = []
j = 0
for id_from in Id_from:
	#print id_from[0]
	IdDict.update({id_from[0]:j}) #id からNumberを取得
	NumberDict.update({j:id_from[0]}) #Number からid を取得
	j = j + 1
j = 0
for id_from in Id_from:
	#print j
	sql = "SELECT pl_title from pagelinks where pl_from =" + str(id_from[0]) + " AND pl_namespace = 0 AND pl_from_namespace = 0 ;"
	cursor.execute(sql)
	LinkNameList = cursor.fetchall()
	#print LinkNameList[0][0]
	if len(LinkNameList) < 100000:
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
		#""で囲まれたものが文字列に入っているときはとりあえず無視.
		#"国鉄9550形蒸気機関車"(9462)から589960へのパスを入れる．
		#295386はメールアドレスのページつながっているのはスラッシュのページ(21222)
		
			try:
				cursor.execute(sql)
				P = list(cursor.fetchall())
				if len(P) ==0:
					continue
				else:
					id_to = IdDict[P[0][0]]
					Matrix[id_to][id_from[0]] = 1.0/len(LinkNameList)
					try:
						CounterDict[P[0][0]] += 1
					except:
						CounterDict.update({[P[0][0]]:1})
				#g.add_edge(int(IdDict[id_from[0]]),int(id_to))
			except:
				#print str(sql)
				#print id_from[0]
				continue
		else:
			continue
print max(CounterDict)
print len(UseNumberList)
	#j = j + 1
#Matrix[IdDict[9462]][IdDict[589960]]= 1.0

UseIDList = []
"""
for s in UseNumberList:
	UseIDList.append(NumberDict[s]) #IはsのID
print len(UseIDList)
#NewMatrix = Matrix[col_sum >= 1][col_sum >=1]
NewMatrix = Matrix[:,UseNumberList][UseNumberList]
#NewMatrix = NewMatrix/np.sum(NewMatrix, axis=0)
r, Vec = get_pagerank(NewMatrix, alpha=0, return_P=True)
for i in range[0:len(r)]:
	print i,UseList[r[i]],Vec[[i]]
#g.add_edge(IdDict[9462],IdDict[589960])
#g.add_edge(IdDict[295386],IdDict[21222])
"""
"""
pr=nx.pagerank(g,alpha=0.85)
prn=nx.pagerank_numpy(g,alpha=0.85)
prc=nx.pagerank_scipy(g,alpha=0.85)

print pr[0:10]

#namespace2のやつとかはlimkto しかなく、ネットワークには入っていないので除外してもよいと考えた
sql = 'select cl_from from categorylinks where cl_to = "存命人物"'
cursor.execute(sql)
HumanIdList = cursor.fetchall()
HumanIdlist = np.zeros([len(HumanIdList)])
k = 0
for j in HumanIdList:
	try:
		HumanIdlist[k] = IdDict[j[0]]
		k = k + 1
	except: #人間辞書にないやつはしょぼいやつ、あるいは関係ないやつなので考えない。
		print j
		continue
#k = 151937
"""
cursor.close()
connector.close()
