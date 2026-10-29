import math
import random


def _merge(left, right, key, counter):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        counter["comparisons"] += 1
        if key(left[i]) <= key(right[j]):      
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def _sort(items, key, counter):
    if len(items) <= 1:                         
        return list(items)
    mid = len(items) // 2
    left = _sort(items[:mid], key, counter)     
    right = _sort(items[mid:], key, counter)
    return _merge(left, right, key, counter)    


def merge_sort(items, key=None):
    return merge_sort_counted(items, key)[0]


def merge_sort_counted(items, key=None):
    counter = {"comparisons": 0}
    result = _sort(list(items), key or (lambda x: x), counter)
    return result, counter["comparisons"]


def empirical_check(sizes=(100, 1000, 10000), seed=42):
    rng = random.Random(seed)
    rows = []
    for n in sizes:
        data = [rng.randint(0, 10**6) for _ in range(n)]
        _, comps = merge_sort_counted(data)
        bound = n * math.log2(n)
        rows.append((n, comps, round(bound), round(comps / bound, 3)))
    return rows