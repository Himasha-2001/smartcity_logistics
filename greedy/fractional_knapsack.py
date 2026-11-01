"""Load a van with the highest possible value using the greedy method.

Items can be divided, so we can take a full item or only
a part of it based on the available capacity.

Greedy Choice:
    Select items with the highest value per weight first.
    Take a fraction of an item if the remaining capacity
    is not enough for the whole item.
"""


def fractional_knapsack(items, capacity):
    """Load a van with items to get the highest possible total value.

    inputs:
        items: A list of (name, weight, value) for each item.
               The original list is not changed.
        capacity: The maximum weight the van can carry.

    Returns: The total value and a list of selected items with
             the fraction taken from each item.
             Zero-weight items are always included.

    Error: If the capacity is negative.

    """
    if capacity < 0:
        raise ValueError("capacity must be >= 0")
    # Greedy choice : highest value/weight ratio first.
    ranked = sorted(items, key=lambda it: (it[2] / it[1]) if it[1] > 0 else float("inf"),
                    reverse=True)
    total, taken, remaining = 0.0, [], capacity
    for name, weight, value in ranked:
        if weight <= remaining:                # fits completely (also true for weight 0)
            taken.append((name, 1.0))
            total += value
            remaining -= weight
        elif remaining > 0:                    # split the last item and stop filling
            frac = remaining / weight
            taken.append((name, frac))
            total += value * frac
            remaining = 0
    return total, taken