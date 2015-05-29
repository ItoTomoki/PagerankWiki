#coding: utf-8
#from nxwiki_kai import get_pagerank
import mysql.connector
import MySQLdb
import numpy as np
import codecs
import sys
#sys.stdout = codecs.getwriter("utf8")(sys.stdout)
#sys.stdin = codecs.getreader("sutf8")(sys.stdin)
connector = MySQLdb.connect(host="localhost", db="wiki", user="root",passwd="", charset="utf8")
cursor = connector.cursor()

def GetpageRank(ids):
	try:
	#print ids
		sql = "SELECT rank FROM PageRankID "
		sql += "where Id = "
		sql += str(ids)
		sql +=  ";"
		#print sql
		cursor.execute(sql)
		PageRank = cursor.fetchall()[0][0]
		return PageRank
	except:
		return 13617	
def GetPageTitle(ids):
	try:
		sql = u"SELECT page_title FROM page "
		sql +=u"where page_id = "
		sql += str(ids)
		sql += u";"
		cursor.execute(sql)
		return cursor.fetchall()[0][0]
	except:
		#print Error
		return "page_namespace が1でない、または閲覧数0のページ"

def GetpageRankAndGoodPage(x):
	try:
		sql = "SELECT page_id FROM page"
		sql +=' where page_title = "'
		sql += x
		sql +='" AND page_namespace = 0 '
		sql +=" ORDER BY page_counter Desc;"
		cursor.execute(sql)
		ID = cursor.fetchall()
		sql = u"SELECT to_id FROM IDLink"
		sql +=u" where from_id = "
		sql += str(ID[0][0])
		sql += ";"
		cursor.execute(sql)
		IDto = cursor.fetchall()
	#print str(ID[0][0])
	
		if len(IDto) == 0:
			print ("PageRankNumber is " + str(GetpageRank(ID[0][0])))
		elif len(IDto) < 5:
			for ids in IDto[0:5]:
				print ("PageRankNumber is " + str(GetpageRank(ID[0][0])))
				print ("リンク先のページタイトルは「" + str(GetPageTitle(ids[0])) + "(ページランク：" + GetpageRank(ids[0]) + ")」です")
		else:
			VArray = []
			for ids in IDto:
				V = GetpageRank(ids[0])
				VArray.append(V)
			B = np.argsort(VArray)
			print ("PageRankNumber is " + str(GetpageRank(ID[0][0])))
			for n in (B[0:5]):
				print IDto[n][0]
				print ("ページランクの高いリンク先のページタイトルは「" + GetPageTitle(IDto[n][0]) + "」です")
		print "If you want to reserach more, Print Another Words:"
		print "if you wan to quit, please 'quit'"
		X = raw_input().decode("utf-8")
		if X == "quit":
			print "Thank you"
		else:
			GetpageRankAndGoodPage()

	except:
		print "Error Print Another Words:"
		print "if you wan to quit, please 'quit'"
		X = raw_input().decode("utf-8")
		if X == "quit":
			print "Thank you"
		else:
			GetpageRankAndGoodPage(X)
	
def jikkou():
	print "Please Title:(if you want to quit, please input”やめる” )"
	x = raw_input().decode("utf-8")
	#x = sys.stdin.read()
	if x == "やめる":
		print "Bye"
	else:
		print x
		GetpageRankAndGoodPage(x)

jikkou()
cursor.close()
connector.close()