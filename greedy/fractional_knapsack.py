"""Fractional knapsack: load a van with divisible cargo.

Greedy choice: highest value/weight ratio first. O(n log n).
Note: fails for 0/1 (indivisible) items because a high-ratio item can leave
unusable capacity behind (e.g. (w,v)=(10,60),(20,100),(30,120), cap 50:
greedy = 160, optimal = 220). Solved with DP in knapsack_01.py.
"""


def fractional_knapsack(items, capacity):
    """items: list of (name, weight, value). Returns (total_value, [(name, fraction)])."""
    if capacity < 0:
        raise ValueError("capacity must be >= 0")
    ranked = sorted(items, key=lambda it: (it[2] / it[1]) if it[1] > 0 else float("inf"),
                    reverse=True)
    total, taken, remaining = 0.0, [], capacity
    for name, weight, value in ranked:
        if remaining <= 0:
            break
        if weight <= remaining:
            taken.append((name, 1.0)); total += value; remaining -= weight
        else:
            frac = remaining / weight
            taken.append((name, frac)); total += value * frac; remaining = 0
    return total, taken
