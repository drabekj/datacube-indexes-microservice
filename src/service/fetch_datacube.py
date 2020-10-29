import requests
import time
import json


class DatacubeService:
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.base_path = 'https://api.spaceknow.com/datacube'

    def _initiate_datapoints_request(self, project, algorithm, source, version, aoi, keep_duplicates=False):
        headers = {
            'authorization': f'Bearer {self.bearer_token}',
            'content-type': 'application/json;charset=utf-8'
        }

        data = json.dumps({
            "filters": [{
                "field": "project",
                "type": "value-list",
                "params": {
                    "values": [project]
                }
            }, {
                "field": "algorithm",
                "type": "value-list",
                "params": {
                    "values": [algorithm]
                }
            }, {
                "field": "source",
                "type": "value-list",
                "params": {
                    "values": [source]
                }
            }, {
                "field": "version",
                "type": "value-list",
                "params": {
                    "values": [version]
                }
            }, {
                "field": "aoi",
                "type": "geo-intersects",
                "params": {
                    "geometryLabel": aoi
                }
            }],
            "keepDuplicates": keep_duplicates
        })

        response = requests.post(f'{self.base_path}/datapoints/get/initiate',
                                 headers=headers,
                                 data=data)
        content = response.json()
        return content.get("pipelineId", None)

    def _retrieve_datacube_response(self, pipeline_id) -> str:
        url = f'{self.base_path}/datapoints/get/retrieve'

        payload = f"{{\n    \"pipelineId\": \"{pipeline_id}\"\n}}"
        headers = {
            'authorization': f'Bearer {self.bearer_token}',
            'content-type': 'application/json;charset=utf-8',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        content = response.json()

        retry_counter = 0
        while 'error' in content and retry_counter < 20:
            time.sleep(1)

            response = requests.request("POST", url, headers=headers, data=payload)
            content = response.json()
            retry_counter += 1

        return content.get('csvLink', None)

    def get_datapoints_data(self, project, algorithm, source, version, aoi, keep_duplicates=False):
        pipeline_id = self._initiate_datapoints_request(project, algorithm, source, version, aoi, keep_duplicates)
        data_csv_link = self._retrieve_datacube_response(pipeline_id)

        return data_csv_link

    def get_catalogue_data(self) -> dict:
        """
        Get full Datacube catalog.
        As dictionary, where indexes are grouped together in an dict array by algorithm (represented by the key).

        :return: Dictionary of index groups, key is the algorithm. Each group is an array of dicts for each index.
        """
        headers = {
            'authorization': f'Bearer {self.bearer_token}',
            'content-type': 'application/json;charset=utf-8'
        }

        response = requests.post(f'{self.base_path}/catalogue/get', headers=headers, data={})
        content = response.json()

        if 'error' in content:
            print(content)

        return content


if __name__ == '__main__':
    bearer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1URkdRVVZFUWpOQk1rUTRRamczT1RreFFqWXdSa016UmpWQ05FVTNOa1pHTmpnM05ESTRRdyJ9.eyJpc3MiOiJodHRwczovL3NwYWNla25vdy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDA4MjE0Mjc0MTAyNDA4NzgyNzIiLCJhdWQiOlsiaHR0cHM6Ly9zcGFjZWtub3cuYXV0aDAuY29tL2FwaS92Mi8iLCJodHRwczovL3NwYWNla25vdy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjAzOTc2OTE4LCJleHAiOjE2MDM5Nzg3MTgsImF6cCI6IkNQMmhyTkZJU3RsVkVKVUZBa3NmdzNodHF5OXF3c1A5Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCB1cGRhdGU6Y3VycmVudF91c2VyX21ldGFkYXRhIHJlYWQ6Y3VycmVudF91c2VyIG9mZmxpbmVfYWNjZXNzIn0.QnDjjO7FSggN9VzjyyITExXgQzpyr8BCZWYLYty3CcoY7l7av1lGtaRElg6TE7zvSyfuNI7vrXii8YleumN6CN66HubVabf4Sh_tZrf_l4x4ub3iwsdykydfrwQBhbv8S6Ax5gUR-PHgzQt1ACgNNZgJ8ujebdtY2AVCdxeO7vhaRSJIZmBVQxMKbF54AT-NVrY6iTu_hq3UeZOK_hsEr_Ddzkx1z9054gwFm8D_4c5y0fA-jDNFHCAQWrocld5PMyOY0L0X1ehCGHiWTVbd-39sAT7nJqT0zgm4MVNOwh_oKfdLL0LQiKfXf6C8wzPYlqTgZEn0txr3jBlXIkPeGw'
    DatacubeService(bearer).get_catalogue_data()
