#!/usr/bin/env python
# -*- coding: utf-8 -*-

import crawler

crawl = crawler.crawler( 'searchindex.db')

# dbを作り直す場合はコメントアウトを削除
# crawl.createindextables()

pages = ['http://time.com/']

crawl.crawl(pages)
