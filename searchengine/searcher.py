#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import nn
import sys
from pysqlite2 import dbapi2 as sqlite

class searcher:
	
	def __init__(self,dbname):

		self.con = sqlite.connect(dbname)

	def __del__( self ):

		self.con.close()

	def getmatchrows( self, q ):

		# クエリを作るための文字列
		fieldlist = 'w0.urlid'
		tablelist = ' '
		clauselist = ' '
		wordids = []

		# 空白で単語を分ける
		words = q.split(' ')
		tablenumber = 0
		print( words )

		for word in words:
			
			# 単語のIDを取得
			wordrow = self.con.execute(
				"select rowid from wordlist where word = '%s'" % word ).fetchone()
			
			if wordrow != None:
				wordid = wordrow[0]
				wordids.append( wordid ) 

				if tablenumber > 0:

					tablelist += ','
					clauselist += ' and '
					clauselist += 'w%d.urlid = w%d.urlid and ' % ( tablenumber - 1, tablenumber )

				fieldlist += ', w%d.location' % tablenumber
				tablelist += 'wordlocation w%d' % tablenumber
				clauselist += 'w%d.wordid = %d' % ( tablenumber, wordid )
				tablenumber += 1
					
		# 分割されたパーツからクエリを構築
		fullquery = 'select %s from %s where %s' % ( fieldlist, tablelist, clauselist )
		# print fullquery
		# sys.exit()
		cur = self.con.execute( fullquery )
		rows = [ row for row in cur]
			
		# print wordids
		return rows, wordids

	def getscoredlist( self, rows, wordids ):

		totalscores = dict([( row[0],0) for row in rows ])

		# ここには後ほどスコアリング関数を入れる
		weights = [ ( 1.0, self.frequencyscore( rows ) ), 1.5, self.locationscore( rows ) ]

		for ( weight, scores )  in weights:

			for url in totalscores:	

				totalscores[ url ] += weight

			return totalscores

	def geturlname( self, id ):

		return self.con.execute(
			"select url from urllist where rowid = %d" % id ).fetchone()[0]

	def query( self, q ):
	
		rows, wordids = self.getmatchrows( q )
		scores = self.getscoredlist( rows, wordids ) 
		print scores
		rankedscores = sorted([( score, url ) for ( url, score ) in scores.items() ], reverse = 1)

		for ( score, urlid ) in rankedscores[0:50]:
			
			print '%f\t%s' % ( score, self.geturlname( urlid )) 
			
	# 正規化		
	def normalizescores( self , scores, smallIsBetter = 0 ):

		vsmall = 0.0001 # 0で除算することによるエラーを回避する
		if smallIsBetter:
	
			minscore = min( scores.values() ) 
			return dict([( u, float( minscore ) / max ( vsmall, l )) for ( u, l ) in scores.items() ])

		else:

			maxscore = max( scores.values() )
			if maxscore == 0: maxscore = vsmall
			
			return dict([( u, float( c ) / maxscore ) for ( u, c ) in scores.items() ])


	# 単語の頻度
	def frequencyscore( self, rows ):

		counts = dict([( row[0], 0 ) for row in rows ])
		for row in rows: counts[ row[0] ] += 1
		return self.normalizescores( counts )

	# ドキュメント内での位置
	def locationscore( self, rows ):

		locations = dict([ (row[0], 1000000) for row in rows ])	
		for row in rows: 
			loc = sum( row[1:] )
			if loc < locations[ row[0] ] : locations[ row[0] ] = loc
		return self.normalizescores( locations, smallIsBetter = 1 )

 	# 単語間の距離
	def distancescore( self, rows ):

		# 単語がひとつしかない場合、全員が勝者
		if len( rows[0] ) <= 2: return dict([( row[0], 1.0 ) for row in rows ])

		# 大きな値でディクショナリを初期化する
		mindistance = dict([( row[0], 1000000 ) for row in rows ])

		for row in rows:
			dist = sum([ abs( row[i] -row[i - 1] ) for i in range(2, len( row ))])
			if dist < mindistance[ row[0] ]: mindistance[ row[0] ] = dist
		return self.normalizescores( mindistance, smallIsBetter = 1 )


	# リンクの数を数える
	def inboundlinkscore( self, rows ):
	
		uniqueurls =set([ row[0] for row in rows ])
		inboundcount = dict([( u, self.con.execute(
			'select count(*) from link where toid=%d' % u ).fetchone()[0] ) 
				for u in uniqueurls ])

		return self.normalizescores( inboundcount )


	# PageRank
	def calculatepagerank( self, iterations = 20 ):
		
		# 現在のPageRankのテーブルを削除
		self.con.execute( 'drop table if exists pagerank' )
		self.con.execute( 'create table pagerank( urlid primary key, score )' )
		
		# すべてのURLのPageRankを1で初期化する
		self.con.execute( 'insert into pagerank select rowid, 1.0 from urllist' )
		self.dbcommit()

		for i in range( iterations ):

			print "Iteration %d" % ( i )
			for ( urlid, ) in self.con.execute( 'select rowid from urllist' ):
			
				pr = 0.15

				# このページにリンクしているすべてのページをループする
				for ( linker, ) in self.con.execute(
					'select distinct fromid from link where toid = %d' % urlid ):

					# linkerのPageRankを取得する
					linkingpr = self.con.execute('select score from pagerank where urlid=%d' % linker).fetchone()[0]

					# linkerからのリンクの合計を取得する
					linkingcount =self.con.execute(
						'select count(*) from link where fromid = %d' % linker).fetchone()[0]
					pr += 0.85 * ( linkingpr / linkingcount )
				self.con.execute(
					'update pagerank set score = %f where urlid = %d' % ( pr, urlid ))
	
				self.dbcommit()


	def pagerankscore( self, rows ):
	
		pageranks = dict([( row[0], self.con.execute( 'select score from pagerank where urlid = %d' % row[0] ).fetchone()[0] ) for row in rows ])
		maxrank = max( pageranks.values() )
		normalizedscores = dict([( u, float(1) / maxrank ) for ( u, l ) in pageranks.items() ])
		return normalizedscores



	def linktextscore( self, rows, wordids ):

		linkscores = dict([( row[0], 0 ) for row in rows ])
		for wordid in wordids:	
			
			cur = self.con.execute( 'select link.fromid, link.toid from linkwords, link where wordid = %d and linkwords.linkid = link.rowid' % wordid)

			for ( fromid, toid ) in cur :
		
				if toid in linkscores:

					pr = self.con.execute( 'select score from pagerank where urlid = %d' % fromid ).fetchone()[0]
					linkscores[ toid ] += pr

				maxscore = max( linkscores.values() )
				normalizedscores = dict([( u, float(l) /maxscore ) for ( u, l ) in linkscores.items()])
				return normalizedscores


	def nnscore( self, rows, wordids ):

		# ユニークなURL　IDをソートされたリストとして取得する
		urlids = [ urlid for urlid in set( [ row[0] for row in rows ] ) ]
		nnres = mynet.getresult( wordids, urlids )
		scores = dict( [ ( urlids[ i ], nnres[ i ] ) for i in range( len( urlids ) ) ] )
		return self.normalizescores( scores )
