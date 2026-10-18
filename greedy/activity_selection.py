"""Activity selection: maximise deliveries per driver.

Greedy choice: always take the compatible job that FINISHES earliest.
Exchange argument: take any optimal schedule; if its first job isn't the
earliest-finishing job g, swap it for g. g ends no later, so it can't
overlap anything that followed, and the schedule stays valid with the same
size. Repeating this on the remaining jobs shows greedy is optimal.
Time: O(n log n) for the sort + O(n) scan.
"""


def activity_selection(windows):
    """windows: list of (start, end). Returns chosen windows in time order.
    A job may start exactly when the previous one ends."""
    chosen, last_end = [], float("-inf")
    for start, end in sorted(windows, key=lambda w: (w[1], w[0])):
        if start >= last_end:
            chosen.append((start, end))
            last_end = end
    return chosen
