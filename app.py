import flask
from flask import request
import json
import re
import requests

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
	req = requests.get(''.join([
		'http://en.wikipedia.org/w/api.php',
		'?action=query',
		'&prop=revisions',
		'&rvprop=content',
		'&format=json',
		'&titles=computing'
	]))

	matches = re.findall('\[\[(?!Category:)(?!File:)(?!Image:).*?\]\]', req.text)

	for match in matches:
		print match

	return ''.join(matches)

if __name__ == '__main__':
	app.debug = True
	app.run(port=3000)