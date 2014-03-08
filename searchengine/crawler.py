#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from BeautifulSoup import *
from urlparse import urljoin
from pysqlite2 import dbapi2 as sqlite

class crawler:
	# データベースの名前でクローラを初期化する
	def __init__(self, dbname):
		self.con = sqlite.connect( dbname )

	def __del__(self):
		self.con.close()

	def dbcommit(self):
		self.con.commit()

	# エントリID を取得したり、それが存在しない場合には追加
	# するための補助関数
	def getentryid( self, table, field, value, createnew=True ):
		cur = self.con.execute(
			"select rowid from %s where %s = '%s'" % (table, field, value ) )
		res = cur.fetchone()
		if res == None:
			cur = self.con.execute(
				"insert into %s ( %s ) values ( '%s' )" % ( table, field, value ) )
			return cur.lastrowid
		else:
			return res[0]

	# 個々のページをインデックスする
	def addtoindex( self, url, soup ):
		if self.isindexed( url ): return
		print 'Indexing ' + url

		# 個々の単語を取得する
		text = self.gettextonly( soup )
		words = self.separatewords( text )

		# URL idを取得する
		urlid = self.getentryid( 'urllist', 'url', url )

		# それぞれの単語と、このurlのリンク
		for id in range( len( words ) ):
			word = words[id]
			if word in ignorewords: continue
			wordid = self.getentryid( 'wordlist', 'word', word )
			self.con.execute( "insert into wordlocation( urlid, wordid, location ) values ( %d, %d, %d )" % (urlid, wordid, id ) )

	# HTMLのページからタグのない状態でテキストを抽出する
	def gettextonly( self, soup ):
		value = soup.string
		if value == None:
			content = soup.contents
			resulttext = ''
			for text in content:
				subtext = self.gettextonly( text )
				resulttext += subtext + '\n'
			return resulttext
		else:
			return value.strip()

	# 空白以外の文字で単語で分割する
	def separatewords( self, text ):
		splitter = re.compile( '\\W*' )
		return [ splited_text.lower() for splited_text in splitter.split( text ) if splited_text != '' ]

	# URLが既にインデックスされていたらtrueを返す
	def isindexed( self, url ):
		fetch_url = self.con.execute(
			"select rowid from urllist where url = '%s'" % url ).fetchone()
		if fetch_url != None:
			# URLが実際にクロールされているかどうかチェック	
			value = self.con.execute(
				"select * from wordlocation where urlid = %d" % u[0] ).fetchone()
			if value != None: return True
		return False

	# 2つのページの間にリンクを付け加える
	def addlinkref( self, urlFrom, urlTo, linkText ):
		words = self.separatewords( linkText )
		fromid = self.getentryid( 'urllist', 'url', urlForm )
		toid = self.getentryid( 'urllist', 'url', urlTo )
		if fromid == toid: return
		cur = self.con.execute( "insert into link( fromid, toid ) values ( %d, %d )" % ( fromid, toid ) )
		linkid = cur.lastrowid
		for word in words:
			if word in ignorewords: continue
			wordid = self.getentryid( 'wordlist', 'word', word )
			self.con.execute( "insert into linkwords( linkid, wordid ) values ( %d, %d )" % ( linkid, wordid ) )

	# ページのリストを受け取り、与えられた深さで幅優先の検索を行い
	# ページをインデクシングする
	def crawl( self, pages, depth=2 ):
		for i in range( depth ):
			newpages = set()
			for page in pages:
				try:
					c = urllib2.urlopen( page )
				except:
					print "Could not open %s" % page
					continue
				soup = BeautifulSoup( c.read() )
				self.addtoindex( page, soup )

				links = soup( 'a' )
				for link in links:
					if ( 'href' in dict( link.attrs ) ):
						url = urljoin( page, link['href'] )
						if url.find( "'" ) != -1 : continue
						url = url.split( '#' )[0] # アンカーを取り除く
						if url[0:4] == 'http' and not self.isindexed( url ):
							newpages.add( url )
						linkText = self.gettextonly( link )
						self.addlinkref( page, url, linkText )

					self.dbcommit()

				pages = newpages

	# データベースのテーブルを作る
	def createindextables( self ):
		self.con.execute( 'create table urllist( url ) ')
		self.con.execute( 'create table wordlist( word ) ')
		self.con.execute( 'create table wordlocation( urlid, wordid, location ) ')
		self.con.execute( 'create table link( fromid integer, toid integer ) ')
		self.con.execute( 'create table linkwords( wordid, linkid ) ')
		self.con.execute( 'create index urlidx on urllist( url ) ')
		self.con.execute( 'create index wordidx on wordlist( word ) ')
		self.con.execute( 'create index wordurlidx on wordlocation( wordid ) ')
		self.con.execute( 'create index urltoidx on link( toid ) ')
		self.con.execute( 'create index urlfromidx on link ( fromid ) ')
		self.dbcommit()
