#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import math
import docclass

cl = docclass.classifier( docclass.getwords )
docclass.sampletrain( cl )
print cl.weightedprob( 'money', 'good', cl.fprob )
docclass.sampletrain( cl )
print cl.weightedprob( 'money', 'good', cl.fprob )
