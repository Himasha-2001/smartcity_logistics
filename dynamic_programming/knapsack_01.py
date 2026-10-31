"""Find the maximum value of items that can fit into a truck
    using the 0/1 Knapsack dynamic programming method.

    Each item must be taken completely or left behind and items cannot be divided.

    The algorithm checks whether taking or skipping each item
    gives the highest total value without exceeding the capacity.

    Three versions are provided:
        knapsack_2d: Uses a full table to store results.
        knapsack_1d: Uses less memory with a single array.
        knapsack_bruteforce: Checks all possible combinations.

    Time Complexity:
        O(nW) for both DP versions.
        O(2^n) for brute force.

    Space Complexity:
        O(nW) for 2D DP.
        O(W) for 1D DP.
        O(n) auxiliary recursion space for brute force.

    Weights and capacity must be non-negative integers.
"""
import random
import time
import tracemalloc


def _check(capacity):
    if capacity < 0:
        raise ValueError("capacity must be >= 0")


def _check_items(items, capacity):
    """Weights and capacity must be non negative whole numbers and Item values can be any numbers. """
    _check(capacity)
    if not isinstance(capacity, int):
        raise ValueError("capacity must be an integer")
    for w, _ in items:
        if not isinstance(w, int) or w < 0:
            raise ValueError("item weights must be non-negative integers")


def knapsack_2d(items, capacity):
    """Find the maximum value of items that can fit within a given capacity using a 2D Dynamic Programming table.

    inputs:
        items: A list of items containing weight and value
        capacity: The maximum weight allowed.

    Returns:
        A tuple containing:
            best_value: The maximum total value.
            chosen_indices: The positions of selected items.
            table: The DP table containing the calculated values.

    Raises:
        ValueError: If capacity or any item weight is negative or is not an integer.


    Time Complexity: O(nW)
    Space Complexity: O(nW)
    """
    _check_items(items, capacity)
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = items[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]                         
            if w <= c:                                      
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)
    chosen, c = [], capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            chosen.append(i - 1)
            c -= items[i - 1][0]
    return dp[n][capacity], sorted(chosen), dp


def knapsack_1d(items, capacity):
    """Find the maximum value of items that can fit within a given capacity
    using a space optimized 1D Dynamic Programming approach.

    Only one array is used to store the calculated values.
    The capacity is updated backwards to make sure each item is selected at most once.

    Returns:
        The maximum total value that can be achieved.
        Selected item positions cannot be retrieved using this method.

    Time Complexity: O(nW)
    Space Complexity: O(W)
    """
    _check_items(items, capacity)
    dp = [0] * (capacity + 1)
    for w, v in items:
        for c in range(capacity, w - 1, -1):   
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def knapsack_bruteforce(items, capacity, i=0):
    """Find the maximum value of items that can fit within a given capacity using a recursive brute force approach.

    For each item, the algorithm checks two choices:
        1. Take the item.
        2. Skip the item.

    It checks all possible combinations and returns the highest value and this method is suitable only for small inputs.

    Returns: The maximum total value that can be achieved.

    Time Complexity: O(2^n)
    Space Complexity: O(n)
    """
    if i == len(items):
        return 0
    best = knapsack_bruteforce(items, capacity, i + 1)              
    w, v = items[i]
    if w <= capacity:
        best = max(best, v + knapsack_bruteforce(items, capacity - w, i + 1))  
    return best


def table_to_text(items, capacity):
    _, _, dp = knapsack_2d(items, capacity)
    width = max(len(str(x)) for row in dp for x in row) + 1
    header = "item\\cap " + "".join(f"{c:>{width}}" for c in range(capacity + 1))
    lines = [header]
    for i, row in enumerate(dp):
        label = "none" if i == 0 else f"{i}:{items[i - 1]}"
        lines.append(f"{label:<9}" + "".join(f"{x:>{width}}" for x in row))
    return "\n".join(lines)


def benchmark(sizes=(10, 15, 20, 22), capacity=100, seed=1):
    """Compare the execution times of Brute Force, 2D DP, and 1D DP using randomly generated items.

    The function measures how long each algorithm takes and checks whether all three methods return the same maximum value.

    Returns:
        A list containing:
            n: Number of items.
            brute_seconds: Brute force execution time.
            dp2d_seconds: 2D DP execution time.
            dp1d_seconds: 1D DP execution time.
            same_answer: Whether all methods return the same result.

    Brute Force becomes much slower as the number of items increases and Both DP methods are generally much faster.

    """
    rng = random.Random(seed)
    rows = []
    for n in sizes:
        items = [(rng.randint(1, 20), rng.randint(1, 100)) for _ in range(n)]
        t = time.perf_counter(); b = knapsack_bruteforce(items, capacity); tb = time.perf_counter() - t
        t = time.perf_counter(); d2 = knapsack_2d(items, capacity)[0]; t2 = time.perf_counter() - t
        t = time.perf_counter(); d1 = knapsack_1d(items, capacity); t1 = time.perf_counter() - t
        rows.append((n, round(tb, 5), round(t2, 5), round(t1, 5), b == d2 == d1))
    return rows


def memory_comparison(n=100, capacity=1000, seed=1):
    """Compare the peak memory usage of the 2D and 1D DP versions using tracemalloc module.

    The 2D version stores a complete table, while the 1D version uses only a single array.

    Returns:
        peak_2d_bytes: Peak memory used by the 2D version.
        peak_1d_bytes: Peak memory used by the 1D version.

    The 1D version should use much less memory because it stores fewer values. This comparison demonstrates the memory
    optimisation of the 1D approach.
    """
    rng = random.Random(seed)
    items = [(rng.randint(1, 50), rng.randint(1, 100)) for _ in range(n)]
    peaks = []
    for solver in (knapsack_2d, knapsack_1d):
        tracemalloc.start()
        solver(items, capacity)
        peaks.append(tracemalloc.get_traced_memory()[1])
        tracemalloc.stop()
    return tuple(peaks)