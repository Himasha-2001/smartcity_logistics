"""Merge sort for the package priority.
 
Packages arrive in random order and must be sorted by delivery deadline
before dispatch. 
 
Divide & Conquer structure
    Divide   : split the list into two halves around the middle index.
    Conquer  : sort each half by calling the same function recursively.
    Combine  : merge the two sorted halves in linear time.
 
Recurrence
    T(n) = 2 T(n/2) + O(n),   T(1) = O(1)
 
    The recursion tree has log2(n) levels, and every level does about n
    work in total while merging, so T(n) = O(n log n). 
 
Complexity
    Time  : O(n log n) in the best, average and worst case.
    Space : O(n) extra, because each merge builds a new list.
"""

import math
import random


def _merge(left, right, key, counter):
    """Combine step: merge two already sorted lists into one sorted list. """
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
    """Recursive divide and conquer step.
 
    Base case   : a list of 0 or 1 items is already sorted.
    Recursive   : sort each half, then merge the sorted halves.
    and then returns a new list.
    """
    if len(items) <= 1:               # base case           
        return list(items)
    mid = len(items) // 2
    left = _sort(items[:mid], key, counter)      # divide + conquer
    right = _sort(items[mid:], key, counter)
    return _merge(left, right, key, counter)    # combine


def merge_sort(items, key=None):
    """Return a new list with `items` sorted in ascending order."""
    return merge_sort_counted(items, key)[0]


def merge_sort_counted(items, key=None):
    """ count the comparisons made."""
    counter = {"comparisons": 0}
    result = _sort(list(items), key or (lambda x: x), counter)
    return result, counter["comparisons"]


def empirical_check(sizes=(100, 1000, 10000), seed=42):
    """Measure comparisons on random data to confirm O(n log n) growth.
    `seed` makes the random data.
    """
    rng = random.Random(seed)
    rows = []
    for n in sizes:
        data = [rng.randint(0, 10**6) for _ in range(n)]
        _, comps = merge_sort_counted(data)
        bound = n * math.log2(n)
        rows.append((n, comps, round(bound), round(comps / bound, 3)))
    return rows