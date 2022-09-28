import requests
import json
import urllib3

urllib3.disable_warnings()

r=requests.get('https://flask:5000/home',verify='cert.pem')

print(r.json())
