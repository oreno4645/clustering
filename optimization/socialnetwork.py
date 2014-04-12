#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

peaple=['Charlie','Augustus','Veruca','Violet','Mike','Joe','Willy','Miranda']

links = [('Augustus', 'Willy'),
				('Mike', 'Joe'),
				('Miranda', 'Mike'),
				('Violet', 'Augustus'),
				('Miranda', 'Willy'),
				('Charlie', 'Mike'),
				('Veruca', 'Joe'),
				('Miranda', 'Augustus'),
				('Willy', 'Augustus'),
				('Joe', 'Charlie'),
				('Veruca', 'Augustus'),
				('Miranda', 'Joe')]

def crosscount( value ):

	location = dict([( people[i], ( value[i*2], value[i*2 + 1])) for i in range( 0, len( people ))])
	total = 0

	# リンクのすべての組み合わせに対してループをかける
	for i in range( len( links ) ):
		for j in range( i + 1, len( links ) ):

			# 座標の取得
			( x1, y1 ), ( x2, y2 ) = location[links[i][0], location[i][1]]
			( x3, y3 ), ( x4, y4 ) = location[links[j][0], location[j][1]]
	
			den = ( y4 - y3 ) * ( x2 - x1 ) - ( x4 - x3 ) * ( y2 - y1 )
	
			# den == 0 なら線は平行
			if den == 0: continue
	
			# 他の場合uaとubは交点を各点の分点で表現したもの
			ua = (( x4 - x3 ) * ( y1 - y3 ) - ( y4 - y3 ) * ( x1 - x3 )) / den
			ub = (( x2 - x1 ) * ( y1 - y3 ) - ( y2 - y1 ) * ( x1 - x3 )) / den 
			
			# 両方の線で分点が0から1の間にあれば線は交差している
			if ua > 0 and ua < 1 and ub > 0 and ub < 1:
				total += 1;
	
	return total

def drawnetwork( sol ):
	# イメージ生成
	img = Image.new( 'RBG', ( 400, 400 ), ( 255, 255, 255 ) )
	draw = ImageDraw.Draw( img )

	# 座標ディクショナリの生成
	position = dixt([( people[i], (sol[i*2], sol[i*2+1])) for i in range( 0, len( people ) )])

	# リンクの描画
	for ( a, b ) in links:
		draw.link( ( position[a], position[b] ), fill = ( 255, 0, 0 ))

	# 人の描写
	for n,p in position.items():
		draw.text( p, n, ( 0, 0, 0 ) )

	img.show()
