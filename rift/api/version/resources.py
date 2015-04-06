"""
Copyright 2013 Rackspace

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
import falcon

from rift.api.common.resources import ApiResource
from rift import version


class VersionResource(ApiResource):

    def get_version_dict(self):
        body = {
            'versions': {
                version.__version_api__: {
                    'build': version.__version__,
                    'status': 'current'
                }
            }
        }
        return body

    def on_get(self, req, resp):
        body = self.get_version_dict()

        resp.status = falcon.HTTP_200
        resp.body = self.format_response_body(body)
