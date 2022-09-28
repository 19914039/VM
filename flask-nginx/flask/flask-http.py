from flask import Flask, request, json, jsonify
from waitress import serve
appFlask = Flask(__name__)
@appFlask.route('/home')
def home():
    return jsonify({'message' : 'Hello Suresh'})
if __name__ == "__main__":
    serve(appFlask,host="0.0.0.0", port=5000, url_scheme='https')
