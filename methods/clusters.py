#!/usr/bin/env python
# -*- coding: utf-8 -*-

class bicluster:
	def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):

		self.left = left
		self.right = right
		self.vec = vec
		self.id = id
		self.distance = distance




def readfile(filename):

	lines = [line for line in open(filename)]

	colnames = lines[0].strip().split('\t')[1:]
	rownames = []
	data = []
	
	for line in lines[1:]:

		p = line.strip().split('\t')
		
		rownames.append(p[0])
		data.append([float(x) for x in p[1:]])

		
	return rownames, colnames, data


from math import sqrt

def pearson(v1,v2):
	
	sum1 = sum(v1)
	sum2 = sum(v2) 

	sum1Sq = sum([pow(v,2) for v in v1])
	sum2Sq = sum([pow(v,2) for v in v2])

	pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

	num = pSum - (sum1 * sum2 / len(v1))
	den = sqrt((sum1Sq - pow(sum1,2) / len(v1)) * (sum2Sq - pow(sum2, 2)/len(v1)))
 
	if den == 0: return 0


	return 1.0 -num /den



def hcluster(rows, distance = pearson):
	
	distances = {}
	currentclustid = -1
	# クラスタは最初は行たち

	clust = [bicluster(rows[i], id = i) for i in range(len(rows))]

	while len(clust) > 1:

		lowestpair = (0,1)
		closest = distance(clust[0].vec, clust[1].vec)

		# すべての組をループし、最も距離の近い組を探す
		for i in range(len(clust)):
			for j in range(i + 1, len(clust)):
				if (clust[i].id, clust[j].id) not in distances:
					distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)	
			
				d = distances[(clust[i].id, clust[j].id)]

				if d < closest:
					closest = d
					lowestpair = (i, j)
			
		# ２つのクラスタの平均を計算する
		mergevec = [
			(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0

			for i in range(len(clust[0].vec))]
		# 新たなクラスタを作る				
		newcluster = bicluster(mergevec, left = clust[lowestpair[0]],
					right = clust[lowestpair[1]],
					distance = closest, id = currentclustid)
	
		# 元のセットではないクラスタのIDは負にする
		currentclustid -= 1
		del clust[lowestpair[1]]
		del clust[lowestpair[0]]
		clust.append(newcluster)
	
	return clust[0]



def printclust(clust, labels = None, n = 0):

	# 階層型のレイアウトにするためにインデントする
	for i in range(n): print ' ',
	if clust.id < 0:

		# 負のidはこれが枝であることを示している
		print '-'
	else:
		# 正のidはこれが終端であることを示している

		if labels == None: print clust.id
		else: print labels[clust.id]
	
	# 右と左の枝を表示する
	if clust.left != None: printclust(clust.left, labels = labels, n = n + 1)
	if clust.right != None: printclust(clust.right, labels = labels, n = n + 1)


		
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
	h = getheight( clust ) * 20
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
		left_height  = getheight( clust.left ) * 20
		right_height = getheight( clust.right ) * 20

		top    = y - ( left_height + right_height ) / 2
		bottom = y + ( left_height + right_height ) / 2

		# 直線の長さ
		line_length = clust.distance * scaling

		# クラスタから子への垂直な直線
		draw.line( ( x, top + left_height / 2, x, bottom - right_height / 2 ), fill=( 255, 0, 0 ) ) 	

		# 左側のアイテムへの水平な直線
		draw.line( ( x, top + left_height / 2, x + line_length, top + left_height / 2 ), fill = ( 255, 0, 0 ) )

		# 右側のアイテムへの水平な直線
		draw.line( ( x, bottom - right_height / 2, x + line_length, bottom - right_height / 2 ), fill = ( 255, 0, 0 ) )

		# 左右のノードたちを描く関数を呼び出す
		drawnode( draw,  clust.left, x + line_length,    top + left_height / 2,  scaling, labels )
		drawnode( draw, clust.right, x + line_length, bottom - right_height / 2, scaling, labels )

	else :
		# 終点であればアイテムのラベルを描く
		draw.text( ( x + 5, y - 7 ), labels[clust.id], ( 0, 0, 0 ) )	
