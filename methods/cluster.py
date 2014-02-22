#!/usr/bin/env python
# -*- coding: utf-8 -*-

class bicluster:
	def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):

		self.left = left
		self.right = right
		self.vec = vec
		self.id = id
		self.distance = distance


# クラスタは最初は行たち 
def hcluster(rows):

	distances = {}
	currentclustid = -1

	clust = [bicluster(rows[i], id = i) for i in range(len(rows))]

	while len(clust) > 1:

		lowestpair = (0,1)
		closest = distance(clust[0].vec, clust[1].vec)

		# すべての組をループし、最も距離の近い組を探す
		for i in range(len(clust)):
			for J in range(i + 1, len(clust)):

				if (clust[i].id, clust[j].id) not in distances:
					distances[(clust[i].id, clust[j].id)] = distances[(clust[i].vec, clust[j].vec)]	
			
				d = distances[(clust[i].id, clust[j].id)]

				if d < closest:
					closest = d
					lowestpair = (i, j)
			
		# ２つのクラスタの平均を計算する
		mergevec = [
			(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0

			for i in range(len(clust[0].vec))]
		# 新たなクラスタを作る				
		newcluster = bicluster(mergevec, left = clust[lowstpair[0]],
					right = clust[lowestpair[1]],
					distane = closest, id = currentclustid)
	
		# 元のセットではないクラスタのIDは負にする
		currentclustid -= 1
		del clust[lowestpair[1]]
		del clust[lowestpair[0]]
		clust.append(newcluster)
	
	return clust[0]

			  
