import collections


# Path to data input file
DATA_FILE = 'program/quake.txt'

# Data structure representing a single event
Event = collections.namedtuple(
    'Event', ('year', 'latitude', 'longitude', 'depth', 'magnitude'))


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
      # Ignore either 1 or 2 columns that preceed year
      values = line.split()
      if len(values) > 6:
        values = values[2:]
      else:
        values = values[1:]

      # Unpack values
      year, latitude, longitude, depth, magnitude = values

      # Store the event
      events.append(Event(year, latitude, longitude, depth, magnitude))

  return events[:1000]
