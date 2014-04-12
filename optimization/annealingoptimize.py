#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def annealingoptimize( domain, costf, T = 10000.0, cool = 0.95, step = 1 ):
	
	# ランダムな値で解を初期化
	vector = [ float( random.randint( domain[i][0], domain[i][1] )) for i in range( len( domain ))]

	while T > 0.1:
		# インデックスを一つ選ぶ
		i = random.randint( 0, len( domain ) - 1 )

		# インデックスの値に加える変更の方向を選ぶ
		dir = random.randint( -step, step )

		# 値を変更したリスト（解）を生成
		vector_b = vector[:]
		vector_b[i] += dir
		if vector_b[i] < domain[i][0]: vector_b[i] = domain[i][0]
		elif vector_b[i] > domain[i][1]: vector_b[i] = domain[i][1]

		# 現在解と生成解のコストを算出
		ea = costf( vector )
		eb = costf( vector_b )
		p = pow( math.e, -abs( eb - ea ) / T )

		# 生成解がベター？または確率的に採用？
		if ( eb < ea or random.random() < p ):
			vector = vector_b

		# 温度を下げる
		T = T * cool
	
	return vector
