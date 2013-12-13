"""Wiki_Golf is made available under the MIT license.  For more details, please
see the file 'license.txt' in the root of the project.
"""
import flask
from flask import request
import json
import re
import requests

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
	return 'Hello, World!'

if __name__ == '__main__':
	app.debug = True
	app.run(port=3000)