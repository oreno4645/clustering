#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw

##
# 与えられたクラスタの高さを決定する
# 与えられたクラスタ全体の高さの合計を知る場合や
# ノードを置く場所を決める場合に利用する
# クラスタが終端になる場合は高さは1になる
##

def getheight( clust ) :
	# 終端であれば高さは1にする
	if clust.left == None and clust.right == None: return 1

	# そうでなければ高さはそれぞれの枝の高さの合計
	return getheight( clust.left ) + getheight( clust.right )



##
# 枝の距離は左右の枝の深さの大きい方と自身の距離を足したもの
# ノードの深さはそれぞれの枝と深さの最大の数です
##

def getdepth( clust ) :
	# 終端への距離は0.0
	if clust.left == None and clust.right == None: return 0

	# 枝の距離は二つの方向の大きい方にそれ自身の距離を足したもの
	return max( getdepth( clust.left ), getdepth( clust.right) ) + clust.distance

##
# 画像のためにdrawオブジェクトを作り、ルートノードに対しdrawnodeを呼び出す。
# ルートノードは画像の左側、真ん中の高さに配置する
##

def drawdendrogram( clust, labels, jpeg='clusters.jpg' ) :
	# 高さと幅
	h = getheight( clusst ) * 20
	w = 1200
	depth = getdepth( clust )

	# 幅は固定されているため、適宜縮尺する
	scaling = float( w - 150 ) / depth

	# 白を背景とする新しい画像を作る
	img = Image.new( 'RGB', ( w, h ), ( 255, 255, 255 ) )
	draw = ImageDraw.Draw( img )
	draw.line( ( 0, h/2, 10, h/2 ), fill = ( 255, 0, 0 ) )

	# 最初のノードを書く
	drawnode( draw, clust, 10, h/2, scaling, labels )
	img.save( jpeg, 'JPEG' )


##
# 子ノードたちの高さを受け取り、それらがあるべき場所を計算し、それに対して
# 1本の長い垂直な直線と2本の水平な直線を書く。水平な直線の長さは、クラスタの深さによって決まる。
##

def drawnode( draw, clust, x, y, scaling, labels ) :
	if clust.id < 0 :
		left_height = getheight( clust.left ) * 20
		right_height = getheight( clust.right ) * 20

		top = y - ( left_height + right_
	
