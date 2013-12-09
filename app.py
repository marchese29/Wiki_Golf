import flask
app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
	return flask.render_template('hello.html', name='World!')

if __name__ == '__main__':
	app.debug = True
	app.run(port=3000)