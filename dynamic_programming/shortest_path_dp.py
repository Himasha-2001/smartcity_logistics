"""Find the cheapest routes between locations in a city using the Bellman Ford Dynamic Programming algorithm.

The city is represented as a weighted graph:
    Nodes represent locations.
    Edges represent roads.
    Weights represent travel costs.

The algorithm repeatedly checks the roads and updates the
cheapest known cost to each location.

It uses one array to store the distances, reducing memory usage.

If a reachable negative cycle is found, a ValueError is raised
because a cheapest route cannot be determined.

Time Complexity: O(V * E)
Space Complexity: O(V)

The algorithm may stop early if no distances change.
"""


def bellman_ford(edges, source):
    """Find the cheapest costs from a starting node to all other nodes using the Bellman Ford algorithm.

    inputs:
        edges: A list of directed edges containing start, end and weight.
        source: The starting node.

    Returns:
        dist: cheapest cost to each node and Unreachable nodes have an infinite cost.
        pred: previous node in each cheapest path and None is used for the source and
          unreachable nodes.

    ValueError: If a negative cycle is reachable from the source.
    """
    nodes = {source}
    for u, v, _ in edges:
        nodes.update((u, v))
    dist = {n: float("inf") for n in nodes}
    pred = {n: None for n in nodes}
    dist[source] = 0
    for _ in range(len(nodes) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v], pred[v] = dist[u] + w, u
                updated = True
        if not updated:
            break
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            raise ValueError("negative cycle reachable from source")
    return dist, pred


def shortest_path(edges, source, target, directed=False):
    """Find the cheapest route between a starting node and a destination using the Bellman Ford algorithm.

    inputss:
        edges: A list of roads containing start, end and weight.
        source: The starting node.
        target: The destination node.
        directed: If True roads are one way.
              If False roads can be travelled in both directions.

    Returns:
        cost: The total cost of the cheapest route.
        path: A list of nodes showing the selected route.

    """
    if not directed:
        edges = list(edges) + [(v, u, w) for u, v, w in edges]
    dist, pred = bellman_ford(edges, source)
    if target not in dist or dist[target] == float("inf"):
        return float("inf"), []
    path, node = [], target
    while node is not None:
        path.append(node)
        node = pred[node]
    return dist[target], path[::-1]