#!/bin/python

import argparse
import requests
import json
import os
import datetime
from flask import Flask, request
from pprint import pprint

URL_API = "https://api.digitalocean.com/v2/"
with open("/run/secrets/do_token", 'r') as f: DO_TOKEN = f.read().splitlines()[0]

app = Flask(__name__)

@app.route('/digitalocean')
def main():
    return "Workflow Engine API for DigitalOcean"

@app.route('/digitalocean/<data_type>')
def get_data(data_type):
    if data_type not in ['regions','size','images']: 
        return "Workflow Engine API for DigitalOcean"
    style = request.args.get('style')
    reload = request.args.get('reload')
    if reload: reload = reload.lower() == 'true' or reload.lower() == '1'
    data = get_api_data(data_type)
    file_data = f"{data_type}_{style}.json" if style else f"{data_type}.json"
    
    if os.path.isfile(file_data):
        modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_data))
        if modification_time > (datetime.datetime.now()-datetime.timedelta(hours=24)) and not reload:
            with open(file_data, 'r') as file:
                return json.load(file)

    output_json = data
    if style == "rundeck":
        output_json = {}
        ord = 1
        for item in data.get(data_type):
            match data_type:
                case "sizes":
                    key = "{:02}".format(ord) + " - {description} | Mem: {memory} Mb ".format(**item) + \
                        "| CPUs: {vcpus} | Disk: {vcpus} Gb | Trans: {transfer} Tb/mo ".format(**item) + \
                        "| Price: {price_monthly} €/mo".format(**item)
                    value = item.get('slug')
                    ord += 1
                case "images":
                    key = "{:03}".format(ord) + " - {description}".format(**item)
                    value = item.get('slug')
                    ord += 1
                case "regions":
                    key = item.get('name')
                    value = item.get('slug')
            output_json[key] = value

    with open(file_data, 'w') as file:
        file.write(json.dumps(output_json))
        return output_json

def get_api_data(type_data):
    headers = {'content-type': 'application/json', 'Authorization': 'Bearer {0}'.format(DO_TOKEN)}
    req = requests.get(URL_API+"/"+type_data+"?per_page=500", headers=headers)
    response = req.json()
    return response
