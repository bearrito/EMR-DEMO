#!/usr/bin/env python
# encoding: utf-8
import decimal
import sys


def process(min_machine,min,record) :
    try :

        (key,value) = record.split('\t')
        (machine,distance) = value.split(':')
        data = decimal.Decimal(distance).quantize(decimal.Decimal('.001'),rounding=decimal.ROUND_DOWN)

        if(min == None or data < min) :
            min = data
            min_machine = machine
    except :
        a = 1
    return (min_machine,min)


min = None
min_machine = None

for record in sys.stdin :
    if(record != None or record != ""):
        (min_machine,min) = process(min_machine,min,record)

print "%s\t%s" % (min_machine,min)