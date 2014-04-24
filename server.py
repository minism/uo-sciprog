import flask

app = flask.Flask(__name__)


@app.route('/')
def home():
  return flask.redirect(flask.url_for('solution', index=1))


@app.route('/<int:index>/')
def solution(index):
  return 'hello %d' % index


if __name__ == '__main__':
  # TODO: no debug for production
  app.run(debug=True)