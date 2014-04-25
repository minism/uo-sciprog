"""Event cluster detection module."""

import collections
import random

import numpy
import scipy.spatial.distance


def get_k_clusters(events, k, limit=None):
  """Given a list of events, build a list of K clusters for the events.

  The clustering detection algorithm used here is an attempt to implement how I 
  think k-means works, but is completely made up and probably bullshit.  Expect
  this function to have terrible performance.

  The next level of complexity would be a parent algorithm which iterates
  through values of K to find the lowest value for K that produces the 
  lowest amount of variance among each cluster.

  Args:
    events: List of event_counter.Event objects.
    k: Number of clusters to evaluate.
    limit: (Optional) object limit for performance reasons.

  Returns:
    List of Cluster objects, sorted by time.
  """
  if limit and len(events) > limit:
    events = events[:limit]
  k = min(len(events), k)
  centroids = map(event_to_point, random.sample(events, k))
  last_centroids = None
  clusters = []
  while not last_centroids or (set((tuple(x) for x in centroids)) !=
                               set((tuple(x) for x in last_centroids))):
    last_centroids = centroids

    # Build clusters for all points based on current centroids
    clusters = [[] for _ in range(k)]
    for event in events:
      index = find_closest_centroid(event, centroids)
      clusters[index].append(event)

    # Determine new mean for each cluster
    centroids = []
    for cluster in clusters:
      centroids.append(numpy.mean(map(event_to_point, cluster), axis=0))

  result = []
  for i, cluster in enumerate(clusters):
    print len(cluster)
    result.append(Cluster(
        event_count=len(cluster),
        latitude=centroids[i][0],
        longitude=centroids[i][1],
        year=centroids[i][2],
        depth=1,
        magnitude=1
    ))
  return result


# Data structure representing a cluster
Cluster = collections.namedtuple(
    'Cluster', ('event_count', 'year', 'latitude',
                'longitude', 'depth', 'magnitude'))


def event_to_point(event):
  """Convert an event to a 3D point"""
  return (event.latitude, event.longitude, event.year)


def find_closest_centroid(event, centroids):
  """Given an Event and a set of centroids, find the closest.

  Returns the index from the centroids list.
  """
  origin = event_to_point(event)
  distances = scipy.spatial.distance.cdist([origin], centroids)[0]
  return distances.argmin()