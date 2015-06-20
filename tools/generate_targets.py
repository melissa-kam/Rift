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
from copy import deepcopy


target_template = {
    "name": "",
    "type": "cloud-server",
    "address": {
        "ip": {
            "port": 22,
            "address": ""
        }
    },
    "authentication": {
        "ssh": {
            "username": "",
            "private_key": ""
        }
    }
}


def generate_targets():
    if len(sys.argv) < 2:
        print "Usage: python generate_targets.py <input filename> [delimiter]"
        sys.exit(1)

    input_file = sys.argv[1]
    delimiter = ','
    if len(sys.argv) > 2:
        delimiter = sys.argv[2]

    csv_input = open(input_file)
    reader = csv.reader(csv_input, delimiter=delimiter)
    for values in reader:
        if not values:
            continue

        name = values[0].strip()
        ip = values[1].strip()
        username = values[2].strip()
        private_key_file_name = values[3].strip()
        target_data = deepcopy(target_template)
        target_data["name"] = name
        target_data["address"]["ip"]["address"] = ip
        target_data["authentication"]["ssh"]["username"] = username

        with open(private_key_file_name) as private_key_file:
            private_key_lines = private_key_file.readlines()
            private_key = ''.join(private_key_lines)
            target_data["authentication"]["ssh"]["private_key"] = private_key

        resp = requests.post(
            "http://localhost:8000/v1/test-tenant/targets",
            data=json.dumps(target_data),
            headers={"Content-Type": "application/json"})

        if resp.status_code != 201:
            print "Error code from target creation: %s" % resp.status_code

generate_targets()
