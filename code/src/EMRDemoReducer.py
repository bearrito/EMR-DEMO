#!/usr/bin/env python
# encoding: utf-8

import decimal
import sys
import math






def record_cleaner(record):

    record = record.strip()
    split_record = record.split('\t')
    key = split_record[0]
    split_record = split_record[1].split(":")
    id = split_record[0]
    value = split_record[1]
    return (key,id,value)

def record_to_datatuple(record):
    split_record = record.split(" ")
    numerical_record = []
    for record in split_record:
        scaled = decimal.Decimal(record).quantize(decimal.Decimal('.001'),rounding=decimal.ROUND_DOWN)
        numerical_record.append(scaled)

    sum = reduce(lambda  x , acc : x + acc,numerical_record,0)
    return numerical_record

def compute_sum(running_sum,data_tuple):

    try:
        running_sum[0] += data_tuple[0]
        running_sum[1] += data_tuple[1]
        running_sum[2] += data_tuple[2]
    except :
        print >> sys.stderr, 'error in running sum with tuple %s' % data_tuple

    return running_sum

def estimate_parameters(record_count,running_sum):

    normal_estimate = running_sum[0] / record_count
    exponential_estimate = 1 / (running_sum[1] /record_count)

    log_sum = running_sum[2]

    log_u =  log_sum / record_count

    log_numerator =  log_sum*log_sum - log_sum*log_u + log_u*log_u
    log_sigma = log_numerator / record_count
    return (normal_estimate,exponential_estimate,log_u,log_sigma)

def process(record_count,running_sum,record):
    record_count += 1
    record = record_cleaner(record)
    data_tuple = record_to_datatuple(record[2])
    running_sum = compute_sum(running_sum,data_tuple)
    t = (record_count,running_sum)

    return t

machine_name = None
key = ''
machine = 'foo'
print >> sys.stderr, 'Starting'
for record in sys.stdin:
    if(record != None and record != '') :

        (k,i,v) = record_cleaner(record)

        if(machine_name == None):
            record_count = 0
            running_sum = [0,0,0]
            machine_name = k

        if(machine_name != k):

            estimates = estimate_parameters(record_count,running_sum)
            print '%s\t%s:%s:%s:%s' % (machine_name,estimates[0],estimates[1],estimates[2],estimates[3])

            machine_name = k
            #print >> sys.stderr, 'machine ' + machine_name
            record_count = 0
            running_sum = [0,0,0]
            (record_count,running_sum) = process(record_count,running_sum,record)
        else:
            #print >> sys.stderr, 'processing %s' % record
            (record_count,running_sum) = process(record_count,running_sum,record)



estimates = estimate_parameters(record_count,running_sum)
print '%s\t%s:%s:%s:%s' % (machine_name,estimates[0],estimates[1],estimates[2],estimates[3])

