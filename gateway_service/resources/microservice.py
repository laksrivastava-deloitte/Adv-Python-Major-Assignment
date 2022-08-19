import json
import requests
import logging

def error_msg_log(e):
    print()
    return logging.error("------------>"+str(e))

class MicroService:
    def __init__(self):
        self.status_code=500
    
    def json(self):
        return {'message':"Microservice offline!!!, Please try again after sometime"}

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
            try:
                response = requests.request(request_type, url, headers=dict_header,data=payload)
            except Exception as e:
                error_msg_log(e)
                return MicroService()
        else:
            try:
                response = requests.request(request_type, url, headers=dict_header)
            except Exception as e:
                error_msg_log(e)
                return MicroService()
        return response

    @staticmethod
    def execute_get(url):
        try:
            response = requests.request("GET", url)
        except Exception as e:
                error_msg_log(e)
                return MicroService()
        return response

    @staticmethod
    def execute_post(url,data):
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.request("POST", url,headers=headers,data=json.dumps(data))
        except Exception as e:
                error_msg_log(e)
                return MicroService()
        return response

