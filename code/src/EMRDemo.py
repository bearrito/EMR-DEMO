import boto
from boto.s3.key import Key
from boto.emr.step import StreamingStep



root_path = '/home/me/Git/EMR-DEMO/code/'
s3 = boto.connect_s3()
emr_demo_bucket = s3.create_bucket('bearrito.demos.emr')
emr_demo_bucket.set_acl('private')


json_records = Key(emr_demo_bucket)
json_records.key = "input/hive/mapper_input"
json_records.set_contents_from_filename(root_path + 'resources/mapper_input')

input_key = Key(emr_demo_bucket)
input_key.key = "input/0/mapper_input"
input_key.set_contents_from_filename( root_path + 'resources/mapper_input')

mapper_key = Key(emr_demo_bucket)
mapper_key.key = "scripts/mapper_script.py"
mapper_key.set_contents_from_filename(root_path + 'src/EMRDemoMapper.py')

reducer_key = Key(emr_demo_bucket)
reducer_key.key = "scripts/reducer_script.py"
reducer_key.set_contents_from_filename( root_path +  'src/EMRDemoReducer.py')

demo_step = StreamingStep(name ='EMR Demo Example'
                    ,mapper='s3://bearrito.demos.emr/scripts/mapper_script.py'
                    ,reducer='s3://bearrito.demos.emr/scripts/reducer_script.py'
                    ,input='s3://bearrito.demos.emr/input/0'
                    ,output='s3://bearrito.demos.emr/output')

emr = boto.connect_emr()
jobid = emr.run_jobflow(name="EMR Example",log_uri='s3://bearrito.demos.logs',steps = [demo_step])

status = emr.describe_jobflow(jobid)
status = emr.describe_jobflow(jobid)
status = emr.describe_jobflow(jobid)