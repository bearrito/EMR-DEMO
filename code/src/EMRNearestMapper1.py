#!/usr/bin/env python
# encoding: utf-8
import sys
for record in sys.stdin :
     (key,value) = record.split('\t')
     print "%s\t%s:%s" % ('agg',key,value)