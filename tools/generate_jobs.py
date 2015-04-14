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
import json
import requests
import sys
from collections import defaultdict


def generate_jobs():
    if len(sys.argv) < 2:
        print "Usage: python generate_jobs.py " \
              "<input filename> [output filename] [delimiter]"
        sys.exit(1)

    input_file = sys.argv[1]
    delimiter = ','
    output_file = 'schedule.csv'
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    if len(sys.argv) > 3:
        delimiter = sys.argv[3]

    with open(output_file, 'w') as schedule_file:
        csv_input = open(input_file)
        reader = csv.reader(csv_input, delimiter=delimiter)
        created_jobs = {}
        for values in reader:
            if not values:
                continue
            nodes = values[1].strip().split(' ')
            action = values[2].strip()
            node_names = ', '.join(nodes)
            job = action + ' on ' + node_names

            if not created_jobs.get(job):
                data = defaultdict(dict)
                data['name'] = job
                data['actions'] = []
                action_data = defaultdict(dict)
                action_data['type'] = 'remote-command'
                action_data['targets'] = nodes
                action_data['parameters']['command'] = action
                data['actions'].append(action_data)
                resp = requests.post(
                    "http://localhost:8000/v1/test-tenant/jobs",
                    data=json.dumps(data),
                    headers={"Content-Type": "application/json"})
                if resp.status_code != 201:
                    print "Error code from job creation: " + resp.status_code

                else:
                    resp_data = json.loads(resp.content)
                    job_id = resp_data['job_id']
                    created_jobs[job] = job_id

            event = values[0] + ',' + created_jobs.get(job) + '\n'
            schedule_file.write(event)

generate_jobs()
