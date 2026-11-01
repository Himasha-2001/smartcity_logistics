"""Closest pair of hubs in 2D .
 
Each hub is shown as a point (x, y). Finding the two closest hubs helps identify
routes that are not being used much and could be combined. Checking every possible
pair takes more time, with a time complexity of O(n²). The Divide and Conquer 
method solves this faster, with a time complexity of O(n log n).
 
Algorithm
    1. Sort: Sort all points by their X coordinates and Y coordinates.
    2. Divide: Split the points into two halves using the middle point.
    3. Conquer: Find the closest pair in the left half and the closest pair in the right half. Select the smaller distance between them.
    4. Combine: Check whether there is an even closer pair across the two halves.
               - Consider only points that are close to the dividing line (within distance d).
               - Check these points in Y-coordinate order.
               - Each point needs to be compared with only the next few points.
               - This is because checking more points is unnecessary based on the distance between them.
    Final result: Return the pair of points with the smallest distance.
 
Recurrence
    T(n) = 2 T(n/2) + O(n),   so   T(n) = O(n log n)
 
    - Divide the points into two halves.
    - Solve each half recursively, giving us 2T(n/2).
    - Combine the results by checking the middle area, which takes O(n) time.

Therefore, the total time complexity is O(n log n).

Why do we sort only once?
    We sort the points by X and Y coordinates at the beginning.
    During each recursive call, we simply divide the already sorted points instead of sorting them again.
       - Sorting once saves time.
       - Re sorting in every recursive call would increase the complexity to O(n log² n).
 
Complexity
    Time  : O(n log n)   [Efficiently finds the closest pair.]
    Space : O(n)         [Requires extra memory to store and divide the points.]
 
"""

import math
import random
import time


def dist(a, b):
    """Euclidean distance between two points"""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def brute_force(points):
    """Check all pairs of points to find the closest pair.
       Used for small inputs (3 or fewer points) and to verify
       the results in tests and benchmarks.
    """
    best = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = dist(points[i], points[j])
            if best is None or d < best[0]:
                best = (d, (points[i], points[j]))
    return best


def _rec(px, py):
    """Find the closest pair of points using the divide and conquer method."""
    n = len(px)
    if n <= 3:      # base case: brute force
        return brute_force(px)
    mid = n // 2
    mid_x = px[mid][0]
    left_px, right_px = px[:mid], px[mid:]
    left_ids = {p[2] for p in left_px}          
    left_py = [p for p in py if p[2] in left_ids]     # keeps y order
    right_py = [p for p in py if p[2] not in left_ids]

    # Conquer: closest pair in each half and then keep the better one
    best = min(_rec(left_px, left_py), _rec(right_px, right_py), key=lambda r: r[0])
    d = best[0]

    # Combine: Check whether there are two points on opposite sides of the dividing line that are closer than the closest pair already found
    strip = [p for p in py if abs(p[0] - mid_x) < d]   
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 8, len(strip))):  
            dd = dist(strip[i], strip[j])
            if dd < d:
                d, best = dd, (dd, (strip[i], strip[j]))
    return best


def closest_pair(points):
    """Find the two closest points using the divide and conquer method """
    if len(points) < 2:
        return None
    tagged = [(p[0], p[1], i) for i, p in enumerate(points)]
    px = sorted(tagged)    # sort by x 
    py = sorted(tagged, key=lambda p: (p[1], p[0]))   # sort by y
    d, (a, b) = _rec(px, py)
    return d, ((a[0], a[1]), (b[0], b[1]))


def benchmark(sizes=(100, 1000), seed=1):
    """Compare the speed of brute force and divide and conquer algorithms.

    Generates random points and tests both algorithms with
    different input sizes and Measures their execution times
    and checks whether both find the same shortest distance.

    """
    rng = random.Random(seed)
    rows = []
    for n in sizes:
        pts = [(rng.uniform(0, 1000), rng.uniform(0, 1000)) for _ in range(n)]
        t = time.perf_counter(); bf = brute_force(pts); t_bf = time.perf_counter() - t
        t = time.perf_counter(); dc = closest_pair(pts); t_dc = time.perf_counter() - t
        rows.append((n, round(t_bf, 5), round(t_dc, 5), math.isclose(bf[0], dc[0])))
    return rows
