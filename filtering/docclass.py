#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import math

# サンプル教師データ
def sampletrain( cl ):
	cl.train( 'Nobody owns the water.', 'good' )
	cl.train( 'the quick rabbit jumps fences', 'good' )
	cl.train( 'buy pharmaceuticals now', 'bad' )
	cl.train( 'make quick money at the online casino', 'bad' )
	cl.train( 'the quick brown fox jumps', 'good' )

def getwords( doc ):
	splitter = re.compile( '\\W*' )

	# 単語を非アルファベットの文字で分割する
	words = [ s.lower() for s in splitter.split( doc ) if len(s) > 2 and len(s) < 20]

	# ユニークな単語のみの集合を返す
	return dict([(w,1) for w in words])

class classifier:
	def __init__( self, getfeatures, filename = None ):
		# 特徴/カテゴリのカウント
		self.fc={}
		# それぞれのカテゴリの中のドキュメント数
		self.cc = {}
		self.getfeatures = getfeatures

	# 特徴/カテゴリのカウントを増やす 
	def incf( self, f, cat ):
		self.fc.setdefault( f, {} )
		self.fc[f].setdefault( cat, 0 )
		self.fc[f][cat] += 1

	# カテゴリのカウントを増やす
	def incc( self, cat ):
		self.cc.setdefault( cat, 0 )
		self.cc[cat] += 1

	# あるカテゴリの中に特徴が現れた数
	def fcount( self, f, cat ):
		if f in self.fc and cat in self.fc[f]:
			return float( self.fc[f][cat] )
		return 0.0

	# あるカテゴリの中野アイテムたちの数
	def catcount( self, cat ):
		if cat in self.cc:
			return float( self.cc[cat] )
		return 0

	# アイテムたちの総数
	def totalcount( self ):
		return sum( self.cc.values() )

	# すべてのカテゴリたちのリスト
	def categories( self ):
		return self.cc.keys()

	# アイテムを特徴に分割する
	# infを呼び出してこのカテゴリの中の特徴たちのカウントを増やす
	# 最後にこのカテゴリのカウントを増やす
	def train( self, item, cat ):
		features = self.getfeatures( item )
		# このカテゴリ中の特徴たちのカウントを増やす
		for feature in features:
			self.incf( feature, cat )
		# このカテゴリのカウントを増やす
		self.incc( cat )

	# このカテゴリの中にあるこの特徴が出現する回数をこのカテゴリ中のアイテムの総数で割る
	def fprob( self, f, cat ):
		if self.catcount( cat ) == 0 : return 0
		# このカテゴリの中にこの特徴が出現する回数を、このカテゴリ中のアイテムの総数で割る
		return self.fcount( f, cat ) / self.catcount( cat )

	# 重み付きの確率を実例を元に算出した確率と仮の確率の平均に重みをつけて返す。
	def weightedprob( self, f, cat, prf, weight = 1.0, ap = 0.5 ):

		# 現在の確率を計算する
		basicprob = prf( f, cat )

		# この特徴がすべてのカテゴリ中に出現する数を数える
		totals = sum( [self.fcount( f, c ) for c in self.categories() ])

		# 重み付けした平均を計算
		bp = (( weight * ap ) + ( totals * basicprob )) / ( weight + totals )
		return bp
