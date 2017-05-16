#!/usr/bin/env python
import argparse
import random
import uuid
import time
from flask import Flask, request, jsonify

# CONFIG
app = Flask(__name__)
app.config.from_object(__name__)

# document processor
def process_document(text, key):
    print("Working on document %s..." % key)
    time.sleep(random.randint(0,30))
    return "Example text recovered from document %s!" % key


@app.route("/pdfs", methods=["POST"])
def runner():
    if request.method=="POST":
        doc_key = uuid.uuid4()
        return jsonify({"id": doc_key, "text": process_document(request.data, doc_key)}),201
    else:
        return jsonify("BAD_REQUEST"), 304


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask-based site for ECD.")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("-p", "--port", default=5000, type=int)

    args = parser.parse_args()

    # launch app!
    app.run(host='0.0.0.0', debug=args.debug, port=args.port, threaded=True)
