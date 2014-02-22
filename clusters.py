#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
	if clust.right != None: printclust(clust.left, labels = labels, n = n + 1)


		
		
