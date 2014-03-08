class crawler:
	# データベースの名前でクローラを初期化する
	def __init__(self, dbname):
		pass

	def __del__(self):
		pass

	def dbcommit(self):
		pass

	# エントリID を取得したり、それが存在しない場合には追加
	# するための補助関数
	def getentryid( self, table, field, value, createnew=True ):
		return None

	# 個々のページをインデックスする
	def addtoindex( self, url, soup ):
		print 'Indexing %s' % url

	# HTMLのページからタグのない状態でテキストを抽出する
	def gettextonly( self, soup ):
		return None

	# 空白以外の文字で単語で分割する
	def separatewords( self, text ):
		return None

	# URLが既にインデックスされていたらtrueを返す
	def isindexed( self, url ):
		return False

	# 2つのページの間にリンクを付け加える
	def addlinkref( self, urlFrom, urlTo, linkText ):
		pass

	# ページのリストを受け取り、与えられた深さで幅優先の検索を行い
	# ページをインデクシングする
	def crawl( self, pages, depth=2 ):
		pass

	# データベースのテーブルを作る
	def createindextables( self ):
		pass
