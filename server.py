import flask
import jinja2

from program import event_counter

app = flask.Flask(__name__)


# Default parameter values for solutions
DEFAULT_PARAMS = [
  # Solution 1: All events in 100 mile radius of Seattle, WA.
  {'origin_latitude': 47.6097, 'origin_longitude': -122.3331, 'radius': 100},
  # Solution 2: All events.
  {},
  # Solution 3: All events that occurred within the longtitude range -75 to -150
  {'start_longitude': -150, 'end_longitude': -75, 'circular_query': '0'},
  # Solution 3: All events of magnitude > 7.5
  {'threshold': 7.5},
  # Solution 5: All events in 100 mile radius of Seattle, WA.
  {'origin_latitude': 47.6097, 'origin_longitude': -122.3331, 'radius': 100},
]


def build_parameters(request_args, origin_latitude=None, origin_longitude=None, 
                     radius=None, start_latitude=None, start_longitude=None,
                     end_latitude=None, end_longitude=None,
                     start_year=None, end_year=None, threshold=None,
                     circular_query=True):
  """Build a dictionary of event counter parameters.

  Use provided defaults, overridden by any arguments present in the request.
  """
  return {
    'origin_latitude': request_args.get('olat', origin_latitude),
    'origin_longitude': request_args.get('olon', origin_longitude),
    'start_latitude': request_args.get('slat', start_latitude),
    'start_longitude': request_args.get('slon', start_longitude),
    'end_latitude': request_args.get('elat', end_latitude),
    'end_longitude': request_args.get('elon', end_longitude),
    'radius': request_args.get('r', radius),
    'start_year': request_args.get('s', start_year),
    'end_year': request_args.get('e', end_year),
    'threshold': request_args.get('m', threshold),
    'circular_query': request_args.get('cq', circular_query),
  }


def validate_parameters(params):
  """Validate event counter parameters and return an error, if any."""
  # Sanitize input to correct numeric types
  for key in ('start_year', 'end_year'):
    if params.get(key):
      try:
        params[key] = int(params[key])
      except ValueError:
        return "%s must be an integer" % key
    else:
      params[key] = None
  for key in ('origin_latitude', 'origin_longitude', 'start_latitude',
              'start_longitude', 'end_latitude', 'end_longitude', 
              'radius', 'threshold'):
    if params.get(key):
      try:
        params[key] = float(params[key])
      except ValueError:
        return "%s must be a number" % key
    else:
      params[key] = None
  params['circular_query'] = params['circular_query'] != '0'
  return None


@app.route('/')
def home():
  return flask.redirect(flask.url_for('solution', index=1))


@app.route('/<int:index>/')
def solution(index):
  params = build_parameters(flask.request.args, **DEFAULT_PARAMS[index - 1])
  error = validate_parameters(params)
  events = event_counter.get_events(**params) if not error else []

  # Load view for solution
  try:
    return flask.render_template(
      'solution%d.html' % index, events=events, params=params, error=error)
  except jinja2.exceptions.TemplateNotFound:
    return flask.abort(404)


if __name__ == '__main__':
  # TODO: no debug for production
  app.run(debug=True)
