#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from PIL import Image, ImageDraw
from math import sqrt

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


def kcluster( rows, labels, distance=pearson, k = 4 ) :

	# それぞれのポイントの最小値と最大値を決める
	ranges = [ ( min( row[i] for row in rows ), max( row[i] for row in rows ) )
	for i in range( len( rows[0] ) ) ]

	# 重心をランダムにk個配置する
	clusters = [[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range( len(rows[0]) ) ] for j in range(k)]

	lastmatches = None

	for t in range( 100 ):
		print 'Iteration %d' % t
		bestmatches=[[] for i in range(k)]

		# それぞれの行に対して、もっとも近い重心を探しだす
		for j in range( len(rows) ):
			row = rows[j]
			bestmatch=0
			for i in range(k):
				cluster_distance = distance( clusters[i], row )
				if cluster_distance < distance( clusters[bestmatch], row ): bestmatch = i
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


##
# アイテム間の距離と実際の距離をスケールダウンさせて調整する
##

def scaledown( data, distance=pearson, rate = 0.01 ) :
	data_num = len( data )
	print data_num

	# アイテムのすべての組の実際の距離
	realdist = [ [ distance( data[i], data[j] ) for j in range( data_num ) ] for i in range( 0, data_num ) ]
	outersum = 0.0

	# 2次元上にランダムに配置するように初期化する
	location = [ [ random.random(), random.random() ] for i in range( data_num ) ]
	fakedist = [ [ 0.0 for j in range( data_num ) ] for i in range( data_num ) ]

	lasterror = None
	for m in range( 0, 1000 ) :
		# 予測距離を測る
		for i in range( data_num ) :
			for j in range( data_num ) :
				fakedist[i][j] = sqrt( sum( [pow(location[i][x] - location[j][x], 2) for x in range( len( location[i] ) ) ] ) )
		
		# ポイントの移動
		grad = [ [ 0.0, 0.0 ] for i in range( data_num ) ]

		totalerror = 0
		for k in range( data_num ) :
			for j in range( data_num ) :
				if j == k : continue
				# 誤差は距離の差の百分率
				errorterm = ( fakedist[j][k] - realdist[j][k] ) / realdist[j][k]

				# 他のポイントへの誤差に比例してそれぞれのポイントを
				# 近づけたり遠ざけたりする必要がある
				grad[k][0] += ( ( location[k][0] - location[j][0] ) / fakedist[j][k] ) * errorterm
				grad[k][1] += ( ( location[k][1] - location[j][1] ) / fakedist[j][k] ) * errorterm

				# 誤差の合計を記録
				totalerror += abs( errorterm )
		print totalerror

		# ポイントを移動することで誤差が悪化したら終了
		if lasterror and lasterror < totalerror : break	
		lasterror = totalerror
	
		# 学習率と傾斜を掛けあわせてそれぞれのポイントを移動
		for k in range( data_num ) :
			location[k][0] -= rate * grad[k][0]
			location[k][1] -= rate * grad[k][1]

	return location	

##
# 二次元でアイテム間の距離を描写
##

def draw2d( data, labels, jpeg="mds2d.jpg" ) :
	image = Image.new( 'RGB', ( 2000, 2000 ), ( 255, 255, 255 ) )
	draw  = ImageDraw.Draw( image )
	for i in range( len( data ) ) :
		x = ( data[i][0] + 0.5 ) * 1000
		y = ( data[i][1] + 0.5 ) * 1000
		draw.text( ( x, y ), labels[i], ( 0, 0, 0 ) )
	image.save( jpeg, 'JPEG' ) 
