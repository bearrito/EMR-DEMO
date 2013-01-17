#!/usr/bin/env python
# encoding: utf-8
import decimal
import sys

def process(min_machine,min_distance,record) :
    (key,value) = record.split("\t")
    data = decimal.Decimal(value).quantize(decimal.Decimal('.001'),rounding=decimal.ROUND_DOWN)
    if(min_machine == None) :
        min_machine = key
        min_distance = None

    if(min_machine != key) :
        print "%s\t%s" % (min_machine,min_distance)
        min_machine = key
        min_distance = None

    if(min_distance == None or data < min_distance) :
        min_distance = data

    return (min_machine,min_distance)


min_distance = None
min_machine = None
for record in sys.stdin :
    (min_machine,min_distance) = process(min_machine,min_distance,record)
print "%s\t%s" % (min_machine,min_distance)
