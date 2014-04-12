#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import math

# 寮。それぞれ空きが二つある
dorms = [ 'Zeus', 'Athena', 'Hercules', 'Bucchus', 'Pluto',]

# 人。第一・第二希望を伴う
prefs = [ ( 'Toby', ( 'Bucchus', 'Hercules' ) ),
					( 'Steve', ( 'Zeus', 'Pluto' ) ),
					( 'Andrea', ( 'Athena', 'Zeus' ) ),
					( 'Sarah', ( 'Zeus', 'Pluto' ) ),
					( 'Dave', ( 'Athena',  'Bucchus' ) ),
					( 'Jeff', ( 'Hercules', 'Pluto' ) ),
					( 'Fred', ( 'Pluto'  'Athena' ) ),
					( 'Suzie', ( 'Bucchus', 'Hercules' ) ),
					( 'Laura', ( 'Bucchus', 'Hercules' ) ),
					( 'Neil', ( 'Hercules',  'Athena') )
				]
				
domain = [ ( 0, (len( dorms ) * 2 ) - i -1 ) for i in range( 0, len( dorms ) * 2 ) ]


def printsolution( vec ):

	slots = []

	# 各寮につきスロットを二つずつ生成
	for i in range( len( dorms ) ): slots += [ i , i ]

	for i in range( len( vec ) ):
		
		x = int( vec[ i ] )
		
		#　残ってるスロットからひとつ選ぶ
		dorm = dorms[ slots[ x ]]

		# 学生とその割当先の寮を表示
		print prefs[ i ][ 0 ], dorm
		
		# このスロットを削除
		del slots[ x ]


def dormcost( vec ):

	cost = 0

	# スロットのリストを生成
	slots = [0,0,1,1,2,2,3,3,4,4]

	# 学生にループをかける
	for i in range( len( vec ) ):

		x = int( vec[ i ] )
		dorm = dorms[ slots[ x ] ]
		pref = prefs[ i ][ 1 ]

		# 第一希望のコスト０、第二希望のコスト１
		if pref[ 0 ] == dorm: cost += 0
		elif pref[ 1 ] == dorm: cost += 1
		else: cost += 3

		# リストになければコスト３
		
		# 選択されたスロットの削除
		del slots[ x ]

	return cost



		
