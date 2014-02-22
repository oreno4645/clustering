import clusters

blognames,words,data=clusters.readfile( './../data/feed_list.csv' )
clust=clusters.hcluster(data)
clusters.printclust( clust, labels=blognames)
