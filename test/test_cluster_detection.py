#!/usr/bin/env python

from program import cluster_detection

if __name__ == '__main__':
  points = [(1,1,1), (1,2,3), (1,2,2), (9,9,10), (10,15,12)]
  print cluster_detection.get_k_centers(points, 1)
