#!/usr/bin/env python
# -*- coding: utf-8 -*-


import clusters

blognames,words,data=clusters.readfile( './../data/banpaku_utf8.csv' )
clust=clusters.hcluster(data)

# CUIで結果を表示
#clusters.printclust( clust, labels=blognames)

# 画像で結果を表示
reload(clusters)
clusters.drawdendrogram(clust, blognames, jpeg="banpaku_reg.jpg")
