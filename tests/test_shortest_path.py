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

    def test_path_cost_matches_reported_cost(self):
        cost, path = shortest_path(self.EDGES, "S", "T", directed=True)
        self.assertEqual(path_cost(self.EDGES, path), cost)

    def test_longer_route_beats_expensive_direct_edge(self):
        edges = [("A", "C", 100), ("A", "B", 1), ("B", "C", 1)]
        self.assertEqual(shortest_path(edges, "A", "C", directed=True), (2, ["A", "B", "C"]))

    def test_parallel_edges_use_cheaper_one(self):
        edges = [("A", "B", 9), ("A", "B", 2)]
        self.assertEqual(shortest_path(edges, "A", "B", directed=True), (2, ["A", "B"]))

    def test_zero_weight_edges(self):
        edges = [("A", "B", 0), ("B", "C", 0)]
        self.assertEqual(shortest_path(edges, "A", "C", directed=True), (0, ["A", "B", "C"]))

    def test_edges_given_in_reverse_order_need_multiple_rounds(self):
        edges = [("D", "E", 1), ("C", "D", 1), ("B", "C", 1), ("A", "B", 1)]
        self.assertEqual(shortest_path(edges, "A", "E", directed=True),
                         (4, ["A", "B", "C", "D", "E"]))

    def test_cycle_with_positive_weights_terminates(self):
        edges = [("A", "B", 1), ("B", "C", 1), ("C", "A", 1), ("C", "D", 1)]
        self.assertEqual(shortest_path(edges, "A", "D", directed=True),
                         (3, ["A", "B", "C", "D"]))

    def test_sample_city_map(self):
        edges = [("Depot", "A", 4), ("Depot", "B", 2), ("B", "A", 1), ("A", "C", 5),
                 ("B", "C", 8), ("B", "D", 10), ("C", "D", 2), ("C", "E", 3),
                 ("D", "F", 11), ("E", "D", 4), ("E", "F", 6), ("F", "Warehouse", 3),
                 ("D", "Warehouse", 9)]
        cost, path = shortest_path(edges, "Depot", "Warehouse")
        self.assertEqual(cost, 19)
        self.assertEqual(path[0], "Depot")
        self.assertEqual(path[-1], "Warehouse")


class TestEdgeCases(unittest.TestCase):
    def test_source_equals_target(self):
        self.assertEqual(shortest_path([("S", "A", 1)], "S", "S"), (0, ["S"]))

    def test_empty_graph_same_node(self):
        self.assertEqual(shortest_path([], "A", "A"), (0, ["A"]))

    def test_empty_graph_different_node(self):
        self.assertEqual(shortest_path([], "A", "B"), (INF, []))

    def test_unreachable_in_directed_graph(self):
        edges = [("S", "A", 1)]
        self.assertEqual(shortest_path(edges, "A", "S", directed=True), (INF, []))

    def test_disconnected_component(self):
        edges = [("A", "B", 1), ("X", "Y", 1)]
        self.assertEqual(shortest_path(edges, "A", "Y"), (INF, []))

    def test_target_not_in_graph(self):
        self.assertEqual(shortest_path([("A", "B", 1)], "A", "Z"), (INF, []))

    def test_source_not_in_edges_is_isolated(self):
        self.assertEqual(shortest_path([("A", "B", 1)], "Z", "A"), (INF, []))

    def test_self_loop_is_ignored(self):
        edges = [("A", "A", 5), ("A", "B", 2)]
        self.assertEqual(shortest_path(edges, "A", "B", directed=True), (2, ["A", "B"]))


class TestDirectedVsUndirected(unittest.TestCase):
    EDGES = [("A", "B", 3), ("B", "C", 4)]

    def test_directed_blocks_reverse_travel(self):
        self.assertEqual(shortest_path(self.EDGES, "C", "A", directed=True), (INF, []))

    def test_undirected_allows_reverse_travel(self):
        self.assertEqual(shortest_path(self.EDGES, "C", "A"), (7, ["C", "B", "A"]))

    def test_undirected_is_symmetric(self):
        forward = shortest_path(self.EDGES, "A", "C")[0]
        backward = shortest_path(self.EDGES, "C", "A")[0]
        self.assertEqual(forward, backward)


class TestNegativeWeights(unittest.TestCase):
    def test_negative_edge_without_cycle_is_fine(self):
        edges = [("S", "A", 5), ("A", "B", -3)]
        self.assertEqual(shortest_path(edges, "S", "B", directed=True), (2, ["S", "A", "B"]))

    def test_negative_edge_can_make_longer_path_cheaper(self):
        edges = [("S", "T", 4), ("S", "A", 6), ("A", "T", -3)]
        self.assertEqual(shortest_path(edges, "S", "T", directed=True), (3, ["S", "A", "T"]))

    def test_negative_cycle_raises(self):
        edges = [("S", "A", 1), ("A", "B", -3), ("B", "A", 1)]
        with self.assertRaises(ValueError):
            shortest_path(edges, "S", "B", directed=True)

    def test_negative_edge_in_undirected_graph_is_a_negative_cycle(self):
        with self.assertRaises(ValueError):
            shortest_path([("A", "B", -1)], "A", "B")

    def test_unreachable_negative_cycle_is_ignored(self):
        edges = [("S", "T", 1), ("X", "Y", -5), ("Y", "X", 1)]
        self.assertEqual(shortest_path(edges, "S", "T", directed=True), (1, ["S", "T"]))


class TestBellmanFordDirectly(unittest.TestCase):
    def test_distances_and_predecessors(self):
        edges = [("S", "A", 2), ("A", "B", 3), ("S", "B", 10)]
        dist, pred = bellman_ford(edges, "S")
        self.assertEqual(dist, {"S": 0, "A": 2, "B": 5})
        self.assertIsNone(pred["S"])
        self.assertEqual(pred["B"], "A")

    def test_unreachable_nodes_have_infinite_distance(self):
        dist, pred = bellman_ford([("S", "A", 1), ("X", "Y", 1)], "S")
        self.assertEqual(dist["X"], INF)
        self.assertIsNone(pred["X"])


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