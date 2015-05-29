#!/usr/bin/env python
# coding: utf-8

import cgi
from datetime import datetime
import mysql.connector
import MySQLdb
import numpy as np
connector = MySQLdb.connect(host="localhost", db="wiki", user="root",passwd="", charset="utf8")
cursor = connector.cursor()
maxId  = 1545324
Matrix = np.zeros([maxId,maxId])
sql = u"SELECT page_id FROM page  where page_namespace = 0 AND page_namespace = 0 ORDER BY page_id ASC;"
cursor.execute(sql)
Id_from = cursor.fetchall()
IdDict = {}
j = 0
for id_from in Id_from:
	#print id_from[0]
	IdDict.update({id_from[0]:j}) 
	j = j + 1
j = 0
for id_from in Id_from:
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
		cursor.execute(sql)
		P = list(cursor.fetchall())
		if len(P) ==0:
			continue
		else:
			id_to = IdDict[P[0][0]]
			Matrix[id_to][id_from[0]] = 1.0/len(LinkNameList)
		#""で囲まれたものが文字列に入っているときはとりあえず無視.
		#"国鉄9550形蒸気機関車"(9462)から589960へのパスを入れる．
		"""
		try:
			cursor.execute(sql)
			P = list(cursor.fetchall())
			if len(P) ==0:
				continue
			else:
				id_to = IdDict[P[0][0]]
				Matrix[id_to][IdDict[id_from[0]]] = 1.0/len(LinkNameList)
				#Matrix[id_to][id_from[0]] = 1.0/len(LinkNameList)
		except:
			print str(sql)
			print id_from[0]
			continue
		
			#print Matrix[id_to][id_from[0]], id_to, id_from[0]
		#print id_to, Matrix[id_to][id_from]
	#print Matrix[85381][5], Matrix[1171][id_from[0]]
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
	except:
		print j
		continue
#k = 151937
cursor.close()
connector.close()
