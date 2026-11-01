import random
import unittest
from dynamic_programming.shortest_path_dp import bellman_ford, shortest_path

INF = float("inf")


def path_cost(edges, path, directed=True):
    total = 0
    for a, b in zip(path, path[1:]):
        options = [w for u, v, w in edges if (u, v) == (a, b)]
        if not directed:
            options += [w for u, v, w in edges if (u, v) == (b, a)]
        total += min(options)
    return total


def floyd_warshall(nodes, edges):
    d = {a: {b: (0 if a == b else INF) for b in nodes} for a in nodes}
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


class TestBasicRouting(unittest.TestCase):
    EDGES = [("S", "A", 4), ("S", "B", 2), ("B", "A", 1), ("A", "T", 5), ("B", "T", 8)]

    def test_cheapest_path_not_fewest_edges(self):
        cost, path = shortest_path(self.EDGES, "S", "T", directed=True)
        self.assertEqual(cost, 8)
        self.assertEqual(path, ["S", "B", "A", "T"])


class TestEdgeCases(unittest.TestCase):

    def test_unreachable_in_directed_graph(self):
        edges = [("S", "A", 1)]
        self.assertEqual(shortest_path(edges, "A", "S", directed=True), (INF, []))


class TestDirectedVsUndirected(unittest.TestCase):
    EDGES = [("A", "B", 3), ("B", "C", 4)]

    def test_undirected_allows_reverse_travel(self):
        self.assertEqual(shortest_path(self.EDGES, "C", "A"), (7, ["C", "B", "A"]))


class TestNegativeWeights(unittest.TestCase):

    def test_negative_edge_can_make_longer_path_cheaper(self):
        edges = [("S", "T", 4), ("S", "A", 6), ("A", "T", -3)]
        self.assertEqual(shortest_path(edges, "S", "T", directed=True), (3, ["S", "A", "T"]))

    def test_negative_cycle_raises(self):
        edges = [("S", "A", 1), ("A", "B", -3), ("B", "A", 1)]
        with self.assertRaises(ValueError):
            shortest_path(edges, "S", "B", directed=True)


class TestAgainstFloydWarshall(unittest.TestCase):
    def test_random_graphs_match_reference(self):
        rng = random.Random(11)
        nodes = list("ABCDEFGH")
        for _ in range(40):
            edges = [(rng.choice(nodes), rng.choice(nodes), rng.randint(0, 20))
                     for _ in range(rng.randint(0, 25))]
            ref = floyd_warshall(nodes, edges)
            src = rng.choice(nodes)
            for tgt in nodes:
                cost, path = shortest_path(edges, src, tgt, directed=True)
                self.assertEqual(cost, ref[src][tgt])
                if cost != INF:
                    self.assertEqual(path[0], src)
                    self.assertEqual(path[-1], tgt)
                    self.assertEqual(path_cost(edges, path), cost)


if __name__ == "__main__":
    unittest.main()