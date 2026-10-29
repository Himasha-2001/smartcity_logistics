def bellman_ford(edges, source):
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
