#!/usr/bin/env python
# -*- coding: utf-8 -*-

import clusters

blognames,words,data=clusters.readfile( './../data/feed_list.csv' )

for k in range( 1, 10 ) :
	kclust = None
	kclust = clusters.kcluster(data, blognames, clusters.pearson, k)
	for k_id in range( len( kclust ) ): 
		print [blognames[r] for r in kclust[k_id]]
