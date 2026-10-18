"""Closest pair of hubs in 2D (Divide & Conquer).

Recurrence: T(n) = 2T(n/2) + O(n)  ->  O(n log n).
"""
import math
import random
import time


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def brute_force(points):
    """O(n^2). Returns (distance, (p, q)) or None if fewer than 2 points."""
    best = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = dist(points[i], points[j])
            if best is None or d < best[0]:
                best = (d, (points[i], points[j]))
    return best


def _rec(px, py):
    n = len(px)
    if n <= 3:
        return brute_force(px)
    mid = n // 2
    mid_x = px[mid][0]
    left_px, right_px = px[:mid], px[mid:]
    left_ids = {p[2] for p in left_px}          # ids make duplicates safe
    left_py = [p for p in py if p[2] in left_ids]
    right_py = [p for p in py if p[2] not in left_ids]

    best = min(_rec(left_px, left_py), _rec(right_px, right_py), key=lambda r: r[0])
    d = best[0]

    strip = [p for p in py if abs(p[0] - mid_x) < d]   # sorted by y
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 8, len(strip))):  # at most 7 neighbours
            dd = dist(strip[i], strip[j])
            if dd < d:
                d, best = dd, (dd, (strip[i], strip[j]))
    return best


def closest_pair(points):
    """Return (distance, (p, q)) or None if fewer than 2 points."""
    if len(points) < 2:
        return None
    tagged = [(p[0], p[1], i) for i, p in enumerate(points)]
    px = sorted(tagged)
    py = sorted(tagged, key=lambda p: (p[1], p[0]))
    d, (a, b) = _rec(px, py)
    return d, ((a[0], a[1]), (b[0], b[1]))


def benchmark(sizes=(100, 1000), seed=1):
    """Rows of (n, brute_seconds, dc_seconds, same_distance)."""
    rng = random.Random(seed)
    rows = []
    for n in sizes:
        pts = [(rng.uniform(0, 1000), rng.uniform(0, 1000)) for _ in range(n)]
        t = time.perf_counter(); bf = brute_force(pts); t_bf = time.perf_counter() - t
        t = time.perf_counter(); dc = closest_pair(pts); t_dc = time.perf_counter() - t
        rows.append((n, round(t_bf, 5), round(t_dc, 5), math.isclose(bf[0], dc[0])))
    return rows
