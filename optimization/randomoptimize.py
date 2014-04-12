#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def randomoptimize( domain, costf ):
	best = 999999999
	bestr = None

	for i in range( 1000 ):
		# 無作為解の生成
		r = [random.randint( domain[i][0], domain[i][1] ) for i in range( len( domain ))]
	
		# コストの取得
		cost = costf( r )
	
		# 最良解と比較
		if cost < best:
			best = cost
			bestr = r

	return r
