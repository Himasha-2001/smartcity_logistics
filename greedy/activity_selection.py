def activity_selection(windows):
    chosen, last_end = [], float("-inf")
    for start, end in sorted(windows, key=lambda w: (w[1], w[0])):
        if start >= last_end:
            chosen.append((start, end))
            last_end = end
    return chosen
