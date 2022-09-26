#!/usr/bin/env python3
import requests
import json
import time
import urllib3
import datetime

urllib3.disable_warnings()
user={}
    
user["name"]='dht'
user["password"]="user1"
r=requests.post('https://flask:5000/api/login',data=json.dumps(user), verify='cert.pem')
TOKEN = json.loads(r.text)['token']
HEADER = {'Authorization' : f'{TOKEN}'}

while True:
           
    reading={}
    reading["temperature"]=30
    reading["humidity"]=55
    reading["timestamp"]=str(datetime.datetime.utcnow())
    print(reading)
    requests.post('https://flask:5000/api/dht', data=json.dumps(reading), headers=HEADER, verify='cert.pem')
    time.sleep(0.1)
