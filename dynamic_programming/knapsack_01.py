def _check(capacity):
    if capacity < 0:
        raise ValueError("capacity must be >= 0")


def knapsack_2d(items, capacity):
    _check(capacity)
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
    _check(capacity)
    dp = [0] * (capacity + 1)
    for w, v in items:
        for c in range(capacity, w - 1, -1):    # downward => each item used once
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def knapsack_bruteforce(items, capacity, i=0):
    if i == len(items):
        return 0
    best = knapsack_bruteforce(items, capacity, i + 1)
    w, v = items[i]
    if w <= capacity:
        best = max(best, v + knapsack_bruteforce(items, capacity - w, i + 1))
    return best
