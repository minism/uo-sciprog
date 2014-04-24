import flask
import jinja2

app = flask.Flask(__name__)


@app.route('/')
def home():
  return flask.redirect(flask.url_for('solution', index=1))


@app.route('/<int:index>/')
def solution(index):
  try:
    return flask.render_template('solution%d.html' % index)
  except jinja2.exceptions.TemplateNotFound:
    return flask.abort(404)


if __name__ == '__main__':
  # TODO: no debug for production
  app.run(debug=True)
