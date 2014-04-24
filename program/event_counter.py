import collections
import math


# Path to data input file
DATA_FILE = 'program/quake.txt'

# Degrees to radians constant
DEG2RAD = math.pi/180.0

# Approx. radius of the earth in miles
EARTH_RADIUS = 3960


def get_events(origin_latitude=None, origin_longitude=None, radius=None,
               start_latitude=None, start_longitude=None,
               end_latitude=None, end_longitude=None,
               start_year=None, end_year=None, threshold=None,
               circular_query=True):
  """Given some parameters, return a filtered table of earthquake events.

  Args:
    latitude: (float) Latitude of origin point for radius query.
    longitude: (float) Longitude of origin point for radius query.
    radius: (float) Radius in miles from origin.
    start_latitude: (float) Lower latitude bound for fixed query.
    start_longitude: (float) Lower longitude bound for fixed query.
    end_latitude: (float) Upper latitude bound for fixed query.
    end_longitude: (float) Upper longitude bound for fixed query.
    start: (int) Year to begin filtering from.
    end: (int) Year to stop filtering from.
    threshold: (float) Magnitude threshold to filter above.
    circular_query: Whether to use a circular or rectangular query.

  Returns:
    List of Event objects, sorted by time.
  """
  events = []

  with open(DATA_FILE) as fh:
    for line in fh:
      row = line.split()
      event = parse_row(row)
      exclude = False

      if circular_query:
        # Determine if event is within specified area for a radius query
        if all( (origin_latitude, origin_longitude, radius) ):
          if geo_distance(
              event.latitude, event.longitude, 
              origin_latitude, origin_longitude) > radius:
            exclude = True

      else:
        # Determine if event is within specified area for a rectangular query
        if (start_latitude is not None and event.latitude < start_latitude or
            start_longitude is not None and event.longitude < start_longitude or
            end_latitude is not None and event.latitude > end_latitude or
            end_longitude is not None and event.longitude > end_longitude):
          exclude = True

      # Determine if event is within specified time
      if start_year and event.year < start_year:
        exclude = True
      if end_year and event.year > end_year:
        exclude = True

      # Determine if event magnitude exceeds threshold
      if threshold is not None and event.magnitude < threshold:
        exclude = True

      # If the event wasn't filtered out, store it
      if not exclude:
        events.append(event)

  return events


# Data structure representing a single event
Event = collections.namedtuple(
    'Event', ('year', 'latitude', 'longitude', 'depth', 'magnitude'))


def parse_row(row):
  """Create an Event object from a data row

  Args:
    row: Tuple of input data.

  Returns:
    Event object.
  """
  # Ignore either 1 or 2 columns that preceed year
  if len(row) > 6:
    row = row[2:]
  else:
    row = row[1:]

  # Remove occasional 'r' or 'x' character prefix from year,
  # I'm not sure what these specify.
  year = row[0]
  if not year[0].isdigit():
    year = year[1:]

  return Event(year=int(year),
               latitude=float(row[1]),
               longitude=float(row[2]),
               depth=float(row[3]),
               magnitude=float(row[4]))


def geo_distance(lat1, lon1, lat2, lon2):
  """Calculate the distance in miles between two geo coordinates

  Args:
    lat1: Latitude of point A.
    lon1: Longitude of point A.
    lat2: Latitude of point B.
    lon2: Longitude of point B.

  Returns:
    Distance in miles.
  """
  # Convert coordinates to radians
  lat1 = (90.0 - lat1) * DEG2RAD
  lat2 = (90.0 - lat2) * DEG2RAD
  lon1 = lon1 * DEG2RAD
  lon2 = lon2 * DEG2RAD
      
  # Calculate the arc length between spherical coords
  arclen = math.acos(
      math.sin(lat1) * math.sin(lat2) * math.cos(lon1 - lon2) + 
      math.cos(lat1) * math.cos(lat2))

  # Multiply arc length by the radius of the earth to get miles
  return arclen * EARTH_RADIUS

