from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
import os
import json
from classifier import Classifier

app = Flask(__name__, static_folder='static', static_url_path='')

try:
    os.environ['FLASK_DEBUG']
    app.debug = True
except KeyError:
    app.debug = False


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/classify', methods=['POST'])
def classify_api():
    if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
        if "message" in request.json:
            data = {"class" : cf.classify(request.json["message"])}
            return Response(json.dumps(data), status=200, mimetype='application/json')
        else:
            return Response(json.dumps({"error" : "Bad Request"}), status=400, mimetype='application/json')
    else:
        return Response(json.dumps({"error" : "Unsupported Media Type. Content-Type must be application/json."}), status=415, mimetype='application/json')
 

if __name__ == '__main__':
    cf = Classifier()
    app.run(host="0.0.0.0")