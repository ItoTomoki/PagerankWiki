#coding: utf8
import mysql.connector
import MySQLdb
import numpy as np
import networkx as nx
connector = MySQLdb.connect(host="localhost", db="wiki", user="root",passwd="", charset="utf8")
cursor = connector.cursor()

sql = u"SELECT page_id FROM page  where page_namespace = 0 AND page_namespace = 0 ORDER BY page_id ASC;"
#sql = u"SELECT page_id FROM page  where page_namespace = 0 AND page_namespace = 0 ORDER BY page_counter Desc;"
#sql = u"SELECT page_id FROM page  where page_namespace = 0 AND page_namespace = 0 AND page_counter > 0 ORDER BY page_counter Desc;"
#page_etsuransuu大きい順
cursor.execute(sql)
Id_from = cursor.fetchall()
maxId  = len(Id_from)
IdDict = {}

#maxId  = 1545324
#有向グラフのインスタンスを生成
g = nx.DiGraph()
for i in range(0,maxId):
	g.add_node(i)
#Matrix = np.zeros([maxId,maxId])

j = 0
for id_from in Id_from:
	#print id_from[0]
	IdDict.update({id_from[0]:j}) 
	j = j + 1
j = 0

#sql = "CREATE TABLE IdLink (Number_to INT,from_id INT, to_id INT, Number_from INT)ENGINE=InnoDB DEFAULT CHARSET=utf8 ;"
#cursor.execute(sql)
for id_from in Id_from[1545316:1545317]:
	#print j
	sql = "SELECT pl_title from pagelinks where pl_from =" + str(id_from[0]) + " AND pl_namespace = 0 AND pl_from_namespace = 0 ;"
	cursor.execute(sql)
	LinkNameList = cursor.fetchall()
	#print LinkNameList[0][0]
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
		"""

		#""で囲まれたものが文字列に入っているときはとりあえず無視.
		#"国鉄9550形蒸気機関車"(9462)から589960へのパスを入れる．
		#295386はメールアドレスのページつながっているのはスラッシュのページ(21222)
		"""
		
		cursor.execute(sql)
		P = list(cursor.fetchall())
		if len(P) ==0:
			continue
		else:
			id_to = IdDict[P[0][0]]
			Matrix[id_to][IdDict[id_from[0]]] = 1.0/len(LinkNameList)
			g.add_edge(int(IdDict[id_from[0]]),int(id_to))
			sql = "INSERT INTO IdLink (from_id,Number_from) VALUES("
			sql += str(id_from[0])
			sql += ","
			sql += str(P[0][0])
			sql += ") ;" 
			f = open("SQL/write.sql","a")
			f.write(sql + '\n')
			f.close()
			cursor.execute(sql)
			cursor.fetchall()
		
		try:
			cursor.execute(sql)
			P = list(cursor.fetchall())
			if len(P) ==0:
				continue
			else:
				id_to = IdDict[P[0][0]]
				g.add_edge(int(IdDict[id_from[0]]),int(id_to))
				sql = "INSERT INTO IdLink (Number_to, from_id, to_id, Number_from) VALUES("
				sql += str(id_to)
				sql += ","
				sql += str(id_from[0])
				sql += ","
				sql += str(P[0][0])
				sql += ","
				sql += str(IdDict[id_from[0]])
				sql += ") ;" 
				f = open("write2.sql","a")
				f.write(sql + '\n')
				f.close()
				cursor.execute(sql)
				#エッジをデータベースに入れるSQLファイルの作成
				#cursor.fetchall()
				#Matrix[id_to][id_from[0]] = 1.0/len(LinkNameList)
		except:
			print str(sql)
			print id_from[0]
			continue
		
	j = j + 1

g.add_edge(IdDict[9462],IdDict[589960])
#g.add_edge(IdDict[295386],IdDict[21222])
#connector.commit()
cursor.close()
connector.close()
