"""Select the maximum number of non overlapping deliveries using
    the greedy method.

    Each delivery has a start and end time. Always select the
    delivery that finishes earliest, then select the next
    delivery that does not overlap with the previous one.

    This method helps a driver complete the maximum number
    of deliveries without time conflicts.

    Time Complexity:O(n log n) for sorting and O(n) for selecting deliveries.

    Space Complexity:O(n) for storing the sorted deliveries and results.
"""


def activity_selection(windows):
    """Select the maximum number of deliveries without overlapping.

    inputs:
        windows: A list of (start, end) delivery time windows.
                The original list is not changed.

    Returns:A list of selected delivery windows in time order.
            A delivery can start when the previous one ends.

    """
    chosen, last_end = [], float("-inf")
    # Greedy choice : earliest finish time.
    for start, end in sorted(windows, key=lambda w: (w[1], w[0])):
        if start >= last_end:          
            chosen.append((start, end))
            last_end = end
    return chosen