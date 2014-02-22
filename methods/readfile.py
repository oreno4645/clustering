#!/usr/bin/env python
# -*- coding: utf-8 -*-


def readfile(filename):

	# 最初の行は列のタイトル
	lines = [line for line in open(filename)]

	colnames = lines[0].strip().split('\t')[1:]
	rownames = []
	data = []
	
	for line in lines[1:]:

		p = line.strip().split('\t')
		# それぞれの行の最初の列は行の名前	
		rownames.append(p[0])
		print p[1:]
		data.append([float(x) for x in p[1:]])

	
	return rownames, colnames, data

print readfile( "file.txt" )
