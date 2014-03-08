#!/usr/bin/env python
# -*- coding: utf-8 -*-

import crawler

crawl = crawler.crawler( 'searchindex.db')

crawl.createindextables()

pages = ['http://en.wikipedia.org/wiki/Main_Page']

crawl.crawl(pages)
