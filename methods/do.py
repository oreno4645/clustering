#!/usr/bin/env python
# -*- coding: utf-8 -*-

import clusters

blognames,words,data=clusters.readfile( './../data/feed_list.csv' )
clust=clusters.hcluster(data)

# CUIで結果を表示
#clusters.printclust( clust, labels=blognames)

# 画像で結果を表示
reload(clusters)
clusters.drawdendrogram(clust, blognames, jpeg="blogclust.jpg")
