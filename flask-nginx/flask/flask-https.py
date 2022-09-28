from flask import Flask, request, json, jsonify
appFlask = Flask(__name__)
@appFlask.route('/home')
def home():
    return jsonify({'message' : 'Hello Suresh'})
if __name__ == "__main__":
    appFlask.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'key.pem'))
