#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
 
from program import cluster_detection
from program import event_counter


if __name__ == '__main__':
  events = [
    event_counter.Event(2000, 20, 30, 5, 5),
    event_counter.Event(2000, 30, 90, 5, 9),
    event_counter.Event(2002, 20, 30, 5, 5),
    event_counter.Event(1940, 12, 11, 5, 5),
    event_counter.Event(1945, 14, 18, 6, 5),
  ]
  print cluster_detection.get_k_clusters(events, 2)
