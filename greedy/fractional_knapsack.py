def fractional_knapsack(items, capacity):
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
