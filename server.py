import flask
import jinja2

from program import event_counter

app = flask.Flask(__name__)


def build_event_counter_parameters(request_args, latitude=None, longitude=None,
                                   radius=None, start_year=None, end_year=None,
                                   threshold=None):
  """Build a dictionary of event counter parameters.

  Use provided defaults, overridden by any arguments present in the request.
  """
  return {
    'latitude': request_args.get('lat', latitude),
    'longitude': request_args.get('lon', longitude),
    'radius': request_args.get('r', radius),
    'start_year': request_args.get('s', start_year),
    'end_year': request_args.get('e', end_year),
    'threshold': request_args.get('m', threshold),
  }

@app.route('/')
def home():
  return flask.redirect(flask.url_for('solution1'))


@app.route('/1/')
def solution1():
  # Default input: All events in 100 mile radius of Seattle, WA.
  params = build_event_counter_parameters(
      flask.request.args, latitude=-47.6097, longitude=22.3331, radius=100)
  events = event_counter.get_events(**params)
  return flask.render_template('solution1.html', events=events, params=params)


@app.route('/<int:index>/')
def solution(index):
  try:
    return flask.render_template('solution%d.html' % index)
  except jinja2.exceptions.TemplateNotFound:
    return flask.abort(404)

if __name__ == '__main__':
  # TODO: no debug for production
  app.run(debug=True)
