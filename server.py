import flask
import jinja2

from program import event_counter

app = flask.Flask(__name__)


# Mapping of URL parameter names to event counter parameter names
PARAMETER_NAME_MAP = {
  'lat': 'latitude',
  'lon': 'longitude',
  'r': 'radius',
  's': 'start_year',
  'e': 'end_year',
  'm': 'threshold',
}


def build_parameters(request_args, **defaults):
  """Build a dictionary of event counter parameters.

  Use provided defaults, overridden by any arguments present in the request.
  """
  return {
      event_param: request_args.get(url_param, defaults.get(event_param))
      for url_param, event_param in PARAMETER_NAME_MAP.items()}


def validate_input(request_args):
  """Validate request args and return an error, if any."""
  for key in ('s', 'e'):
    if request_args.get(key):
      try:
        int(request_args[key])
      except ValueError:
        return "%s must be an integer" % PARAMETER_NAME_MAP[key]
  for key in ('lat', 'lon', 'r', 'm'):
    if request_args.get(key):
      try:
        float(request_args[key])
      except ValueError:
        return "%s must be a number" % PARAMETER_NAME_MAP[key]
  return None


@app.route('/')
def home():
  return flask.redirect(flask.url_for('solution1'))


@app.route('/1/')
def solution1():
  # Default input: All events in 100 mile radius of Seattle, WA.
  params = build_parameters(
      flask.request.args, latitude=-47.6097, longitude=22.3331, radius=100)

  # Validate input
  error = validate_input(flask.request.args)
  if not error:
    # Process events
    events = event_counter.get_events(**params)
  else:
    events = []

  return flask.render_template(
      'solution1.html', events=events, params=params, error=error)


@app.route('/<int:index>/')
def solution(index):
  try:
    return flask.render_template('solution%d.html' % index)
  except jinja2.exceptions.TemplateNotFound:
    return flask.abort(404)

if __name__ == '__main__':
  # TODO: no debug for production
  app.run(debug=True)
