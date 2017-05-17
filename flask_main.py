#!/usr/bin/env python
import argparse
import random
import uuid
import time
from redis import StrictRedis
import json
from flask import Flask, request, jsonify, g

# CONFIG
app = Flask(__name__)
app.config.from_object(__name__)
redis_port=6379
redis_host="redis"

# document processor
def process_document(text, key):
    print("Working on document %s..." % key)
    time.sleep(random.randint(0,30))
    return "Example text recovered from document %s!" % key

@app.before_request
def redis_connect():
    g.redis = StrictRedis(redis_host, redis_port)

@app.route('/')
def index():
    return 'hello',200
@app.route("/pdfs", methods=["POST"])
def pdf_post():
    if request.method=="POST":
        doc_key = uuid.uuid4().hex
        message = json.dumps({'id':doc_key, 'data': request.data.decode()})
        g.redis.publish('pdfs', message.encode('utf-8'))
        g.redis.set(doc_key, json.dumps({'status': 'processing'}))
        return json.dumps({'id': doc_key}) ,200

@app.route("/pdfs/<unique_id>", methods=["GET"])
def runner(unique_id=None):
    if unique_id == None:
        return jsonify("BAD_REQUEST", 400)
    elif not g.redis.exists(unique_id):
        return jsonify("NOT_FOUND", 404)        
    return jsonify(json.loads(g.redis.get(unique_id).decode('utf-8'))), 200



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask-based site for ECD.")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("-p", "--port", default=5000, type=int)
    parser.add_argument("-r", "--redis_host", default="redis", type=str)
    parser.add_argument("-k", "--redis_port", default=6379, type=int)

    args = parser.parse_args()

    # launch app!
    app.run(host='0.0.0.0', debug=args.debug, port=args.port, threaded=True)
