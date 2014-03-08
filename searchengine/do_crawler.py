#!/usr/bin/env python
# -*- coding: utf-8 -*-

import crawler

pagelist = ['http://en.wikipedia.org/wiki/Main_Page']

crawler = crawler.crawler('')

crawler.crawl(pagelist)
