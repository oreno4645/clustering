#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pdb

def kcluster( rows, distance=pearson, k = 4 ) :

	# それぞれのポイントの最小値と最大値を決める
	ranges = [ ( min( row[i] for row in rows ), max( row[i] for row in rows ) )
	for i in range( len( rows[0] ) ) ]

	# 重心をランダムにk個配置する
	clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range( len(rows[0]) ) ] for j in range(k)]

	lastmatches = None

	for t in range( 100 ):
		print 'Iteration %d' % t
		bestmatches=[[] for i in range(k)]

		# それぞれの行に対して、もっとも近い重心を探しだす
		for j in range( len(rows) ):
			row = rows[j]
			bestmatches=0
			for i in range(k):
				distance = distance( clusters[i], row )
				if distance < distance( clusters[bestmatch], row ): bestmatch = i
			bestmatches[bestmatch].append(j)

		# 結果が前回と同じであれば完了	
		if bestmatches == lastmatches: break
		lastmatches = bestmatches
	
		# 重心をそのメンバーの平均に移動する
		for i in range( k ):
			avgs = [0.0]*len(rows[0])
			if len( bestmatches[i] ) > 0:
				for rowid in bestmatches[i]:
					for m in range( len( rows[rowid] ) ):
						avgs[m] += rows[rowid][m]
				for j in range( len( avgs ) ):
					avgs[j] /= len( bestmatches[i] )
				clusters[i] = avgs
	
		return bestmatches
