#!/usr/bin/env python
# encoding: utf-8
import decimal
import math
import sys

def record_to_decimal(sensor_record):
    numerical_record = []
    for record in sensor_record:
        scaled = decimal.Decimal(record).quantize(decimal.Decimal('.001'),rounding=decimal.ROUND_DOWN)
        numerical_record.append(scaled)
    return numerical_record


def record_cleaner(record):
    #print(record)
    record = record.strip()
    (super_key,record_date,c1,c2,c3) = record.split('\t')
    key = super_key[super_key.index('Machine'):]
    values = [c1,c2,c3]
    #print(values)
    return (key,values)

def compute_distance(target,data):
    d0 = (target[0] - data[0])**2
    d1 = (target[1] - data[1])**2
    d2 = (target[2] - data[2])**2

    return math.sqrt(d0 + d1 + d2)

def process(target,record) :
    (key,values) =  record_cleaner(record)
    transformed_data = record_to_decimal(values)
    distance = compute_distance(target,transformed_data)
    output = '%s\t%s' % (key,distance)
    print output


target = (decimal.Decimal(-1.53),decimal.Decimal(0.144),decimal.Decimal(1.99))
for record in sys.stdin:
     process(target,record)