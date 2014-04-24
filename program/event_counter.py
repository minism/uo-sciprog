import collections


# Path to data input file
DATA_FILE = 'program/quake.txt'


def get_events(latitude=None, longitude=None, radius=None,
               start_year=None, end_year=None, threshold=None):
  """Given some parameters, return a filtered table of earthquake events.

  Args:
    latitude: (float) Latitude of origin point.
    longitude: (float) Longitude of origin point.
    radius: (float) Radius in miles from origin.
    start: (int) Year to begin filtering from.
    end: (int) Year to stop filtering from.
    threshold: (float) Magnitude threshold to filter above.

  Returns:
    List of Event objects, sorted by time.
  """
  events = []

  with open(DATA_FILE) as fh:
    for line in fh:
      row = line.split()
      event = parse_row(row)
      exclude = False

      # Determine if event is within specified area
      if latitude is not None and longitude is not None and radius is not None:
        if geo_distance(
            event.latitude, event.longitude, latitude, longitude) > radius:
          exclude = False

      # Determine if event is within specified time
      if start_year is not None and event.year < start_year:
        exclude = True
      if end_year is not None and event.year > end_year:
        exclude = True

      # Determine if event magnitude exceeds threshold
      if threshold is not None and event.magnitude < threshold:
        exclude = True

      # If the event wasn't filtered out, store it
      if not exclude:
        events.append(event)

  return events[:1000]


# Data structure representing a single event
Event = collections.namedtuple(
    'Event', ('year', 'latitude', 'longitude', 'depth', 'magnitude'))


def parse_row(row):
  """Create an Event object from a data row"""
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

  return Event(year=year,
               latitude=float(row[1]),
               longitude=float(row[2]),
               depth=float(row[3]),
               magnitude=float(row[4]))


def geo_distance(lat1, lon1, lat2, lon2):
  return 25

