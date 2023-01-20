#!/bin/python

import argparse
import requests
import json
import os
from flask import Flask, request
from pprint import pprint

URL_API = "https://api.digitalocean.com/v2/"
with open("/run/secrets/do_token", 'r') as f: DO_TOKEN = f.read().splitlines()[0]

app = Flask(__name__)

@app.route('/digitalocean/<data_type>')
def get_data(data_type):
    style = request.args.get('style')
    data = get_data(data_type)
    if style == "key/value":
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
        return output_json
    return data

def get_data(type_data):
    headers = {'content-type': 'application/json', 'Authorization': 'Bearer {0}'.format(DO_TOKEN)}
    req = requests.get(URL_API+"/"+type_data+"?per_page=500", headers=headers)
    response = req.json()
    return response
