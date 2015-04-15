"""
Copyright 2015 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import csv
import requests
import sys
import time
from datetime import datetime
from threading import Timer


def execute_job(job):
    print "Executing {job} at {time}".format(
        job=job, time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    job_uri = "http://localhost:8000/v1/test-tenant/jobs/{uuid}".format(
        uuid=job)
    request = requests.head(job_uri)
    if request.status_code != 200:
        print "Error executing job: %s" % request.status_code

if len(sys.argv) < 2:
    print "Usage: basic_scheduler.py <filename>"
    sys.exit(1)

file_name = sys.argv[1]

max_time = 0

print "Start! ", datetime.now().strftime('%Y-%m-%d %H:%M:%S')
with open(file_name) as schedule_file:
    reader = csv.reader(schedule_file)
    for values in reader:
        delay = float(values[0].strip()) * 60
        uuid = values[1].strip()
        Timer(delay, execute_job, [uuid]).start()
        if delay > max_time:
            max_time = delay

print 'Will run for %s minutes.' % (max_time/60 + 1)
time.sleep(max_time + 60)
print "Stop! ", datetime.now().strftime('%Y-%m-%d %H:%M:%S')
