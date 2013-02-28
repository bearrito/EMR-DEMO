#!/usr/bin/env python
# encoding: utf-8
import boto
from boto.s3.key import Key
from boto.emr.step import StreamingStep
from boto.emr.bootstrap_action import BootstrapAction

root_path = '/home/me/Git/EMR-DEMO/code/'


s3 = boto.connect_s3()
emr_demo_bucket = s3.create_bucket('bearrito.demos.emr')
emr_demo_bucket.set_acl('private')



input_key = Key(emr_demo_bucket)
input_key.key = "input/0/mapper_input"
input_key.set_contents_from_filename(root_path + 'resources/mapper_input')

mapper_key = Key(emr_demo_bucket)


mapper_key.key = "scripts/bootstrap.sh"
mapper_key.set_contents_from_filename(root_path + 'src/BootStrap.sh')

bootstrap_step = BootstrapAction("bootstrap.sh",'s3://bearrito.demos.emr/scripts/bootstrap.sh',None)


mapper_key.key = "scripts/mapper_nearest_0.py"
mapper_key.set_contents_from_filename(root_path + 'src/EMRNearestMapper0.py')



mapper_key.key = "scripts/mapper_nearest_1.py"
mapper_key.set_contents_from_filename(root_path + 'src/EMRNearestMapper1.py')

reducer_key = Key(emr_demo_bucket)
reducer_key.key = "scripts/reducer_nearest_0.py"
reducer_key.set_contents_from_filename(root_path + 'src/EMRNearestReducer0.py')

reducer_key.key = "scripts/reducer_nearest_1.py"
reducer_key.set_contents_from_filename(root_path + 'src/EMRNearestReducer1.py')



nearest_0 = StreamingStep(name ='EMR First Phase'
    ,mapper='s3://bearrito.demos.emr/scripts/mapper_nearest_0.py'
    ,reducer='s3://bearrito.demos.emr/scripts/reducer_nearest_0.py'
    ,input='s3://bearrito.demos.emr/input/0'
    ,output='s3://bearrito.demos.emr/output/0')

nearest_1 = StreamingStep(name ='EMR Second Phase'
    ,mapper='s3://bearrito.demos.emr/scripts/mapper_nearest_1.py'
    ,reducer='s3://bearrito.demos.emr/scripts/reducer_nearest_1.py'
    ,input='s3://bearrito.demos.emr/output/0'
    ,output='s3://bearrito.demos.emr/output/1')

emr = boto.connect_emr()
jobid = emr.run_jobflow(name="EMR Two Phase"
                        ,log_uri='s3://bearrito.demos.logs'
                        ,steps = [nearest_0,nearest_1]
                        ,bootstrap_actions=[bootstrap_step])

status = emr.describe_jobflow(jobid)