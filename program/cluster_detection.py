"""Event cluster detection module."""

import collections


def get_clusters(events):
  """Given a list of events, build a list of clusters for the events.

  The clustering detection algorithm used here is an attempt to implement how I 
  think k-means works, but is completely made up and probably bullshit.  Expect
  this function to have terrible performance.

  Args:
    events: List of event_counter.Event objects.

  Returns:
    List of Cluster objects, sorted by time.
  """
  clusters = []
  return events



def get_k_means(events, k):
  """Get a set of K [time, space] means for events"""
  pass


# Data structure representing a cluster
Cluster = collections.namedtuple(
    'Cluster', ('event_count', 'year', 'latitude',
                'longitude', 'depth', 'magnitude'))