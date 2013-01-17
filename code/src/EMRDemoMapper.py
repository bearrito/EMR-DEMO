#!/usr/bin/env python
# encoding: utf-8
import sys
import decimal


def some_function(sensor_record):

    numerical_record = []
    for record in sensor_record:
        scaled = decimal.Decimal(record).quantize(decimal.Decimal('.001'),rounding=decimal.ROUND_DOWN)
        numerical_record.append(scaled)



    return ''.join(map(lambda x: str(x) + ' ',numerical_record))

def record_cleaner(record):
    record = record.strip()
    (key,date,c1,c2,c3) = record.split('\t')
    values = [c1,c2,c3]
    return (key,values)

def process(count,record) :
    count += 1
    (key,values) =  record_cleaner(record)
    transformed_data = some_function(values)
    output = '%s\t%s:%s' % (key,count,transformed_data)
    print output

    return count


count = 0

for record in sys.stdin :
    count = process(count,record)




