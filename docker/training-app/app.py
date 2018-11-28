import datetime
import os
import json
import sys
import time
from flask import Flask, render_template, redirect, url_for, request
from container import indexer, labeller, trainer, tester


app = Flask(__name__)


@app.route("/training/indexer/reindex", methods=['GET'])
def index():
    return indexer.prepare()


@app.route("/training/labeller/labels", methods=['GET'])
def labels():
    return labeller.prepare_labels()


@app.route("/training/labeller/search", methods=['GET'])
def search():
    return labeller.search(request.args.get('q'))


@app.route("/training/labeller/save", methods=['POST'])
def save_labels():
    
    return labeller.save(json.loads(request.data))

@app.route("/training/trainer/train", methods=['GET'])
def train():
    return trainer.train()

@app.route("/training/tester/test", methods=['GET'])
def test():
    return tester.test(request.args.get('q'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
