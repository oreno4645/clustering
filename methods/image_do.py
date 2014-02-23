#!/usr/bin/env python
# -*- coding: utf-8 -*-

import clusters

blognames,words,data = clusters.readfile( './../data/feed_list.csv' )

coords = clusters.scaledown(data)

clusters.draw2d(coords, blognames, jpeg="2d.jpg")
