import json
import requests
class MicroService:
    @staticmethod
    def  execute(request_type,url,header,data=None):

        #header setup
        dict_header={}
        header=dict(header)
        header_keys=header.keys()
        if('Content-Type' in header_keys):
            dict_header['Content-Type']=header['Content-Type']
        if('X-Access-Token' in header_keys):
            dict_header['X-Access-Token']=header['X-Access-Token']

        if data:
            payload=json.dumps(data)
            response = requests.request(request_type, url, headers=dict_header,data=payload)
        else:
            response = requests.request(request_type, url, headers=dict_header)
        return response

    @staticmethod
    def execute_get(url):
        response = requests.request("GET", url)
        return response

    @staticmethod
    def execute_post(url,data):
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url,headers=headers,data=json.dumps(data))
        return response

