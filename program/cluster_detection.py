"""Event cluster detection module."""

import collections
import random

import numpy
import scipy.spatial.distance


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


def events_to_points(events):
  """Convert a list of events to 3 dimensional points"""
  return [(e.latitude, e.longitude, e.year) for e in events]


def get_k_centers(points, k):
  """Find K three dimensional centers for events"""
  centers = random.sample(points, k)
  last_centers = None
  while not last_centers or set(centers) != set(last_centers):
    last_centers = centers

    # Build clusters for all points based on current centers
    clusters = [[] for _ in range(k)]
    for point in points:
      index = find_closest_point(point, centers)
      clusters.append(point)

    # Determine new mean for each cluster
    centers = []
    for cluster in clusters:
      centers.append(numpy.mean(cluster, axis=0))
  return centers


def find_closest_point(origin, targets):
  """Given a point and a set of targets, find the closest.

  Returns the index from the centers list.
  """
  distances = scipy.spatial.distance.cdist([origin], targets)[0]
  return distances.argmin()


# Data structure representing a cluster
Cluster = collections.namedtuple(
    'Cluster', ('event_count', 'year', 'latitude',
                'longitude', 'depth', 'magnitude'))